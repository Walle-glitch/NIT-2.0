import ipaddress
import random
import asyncio
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'Internal_Modules'))

import _Bot_Config

# Global variables to keep track of current game state
current_question = None
correct_answer = None
game_task = None

# Paths to JSON files
QUESTION_FILE = _Bot_Config._Question_File()
SCORE_FILE = _Bot_Config._User_Score_File()

def load_network_questions():
    """Loads network questions from the JSON file."""
    if os.path.exists(QUESTION_FILE):
        with open(QUESTION_FILE, "r") as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"{QUESTION_FILE} not found!")

def load_user_scores():
    """Loads user scores from the JSON file. Creates a new file if it doesn't exist."""
    if not os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "w") as f:
            json.dump({}, f)  # Create an empty JSON file
    with open(SCORE_FILE, "r") as f:
        return json.load(f)

def save_user_scores(scores):
    """Saves the updated user scores to the JSON file."""
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f, indent=4)

def generate_subnet_question():
    """Generates a random subnet-related question."""
    ip = ipaddress.IPv4Address(random.randint(0, 2**32 - 1))
    prefix_length = random.randint(16, 30)
    network = ipaddress.IPv4Network(f"{ip}/{prefix_length}", strict=False)
    
    question_type = random.choice(["network", "broadcast", "hosts"])
    
    if question_type == "network":
        question = f"What is the network address for {network}?"
        correct_answer = str(network.network_address)
    elif question_type == "broadcast":
        question = f"What is the broadcast address for {network}?"
        correct_answer = str(network.broadcast_address)
    else:  # hosts
        question = f"How many hosts can be in the subnet {network}?"
        correct_answer = str(network.num_addresses - 2)  # Subtracts network and broadcast addresses
    
    return question, correct_answer

def generate_network_question():
    """Generates a random network-related question from the loaded JSON file."""
    questions = load_network_questions()
    question = random.choice(questions)
    return question["question"], question["options"], question["correct_option_index"]

def check_subnet_answer(user_answer, correct_answer):
    """Checks if the user's answer for subnet question is correct."""
    return user_answer.strip() == correct_answer

def check_network_answer(selected_option_index, correct_option_index):
    """Checks if the selected answer for network question is correct."""
    return selected_option_index == correct_option_index

async def start_game(ctx, game_type):
    """Starts a game based on the selected game type."""
    global current_question, correct_answer, game_task

    if game_task and not game_task.done():
        await ctx.send("A game is already in progress. Please finish it first.")
        return

    if game_type == 'subnet':
        current_question, correct_answer = generate_subnet_question()
        await ctx.send(f"Subnet question: {current_question}")
    elif game_type == 'network':
        question, options, correct_index = generate_network_question()
        options_str = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
        current_question = f"{question}\n\n{options_str}"
        correct_answer = correct_index  # Store the correct answer index
        await ctx.send(f"Network question:\n{current_question}")
    
    game_task = asyncio.create_task(run_game_timer(ctx, 300))  # 5 minutes

async def run_game_timer(ctx, duration):
    """Runs a timer and ends the game when time is up."""
    await asyncio.sleep(duration)
    if game_task and not game_task.done():
        await ctx.send("Time is up! The game has ended.")
        reset_game()

def reset_game():
    """Resets the game state."""
    global current_question, correct_answer, game_task
    current_question = None
    correct_answer = None
    if game_task and not game_task.done():
        game_task.cancel()
        game_task = None

def update_user_score(user_id, points):
    """Updates the score for the user and saves it to a JSON file."""
    scores = load_user_scores()
    
    previous_score = scores.get(str(user_id), 0)
    
    # Update user's score
    scores[str(user_id)] = previous_score + points
    
    # Save the updated scores back to the file
    save_user_scores(scores)
    
    return previous_score, scores[str(user_id)]

async def show_score_comparison(ctx, user_id, new_points):
    """Shows the score comparison between the previous and current score."""
    previous_score, new_score = update_user_score(user_id, new_points)
    
    if previous_score == 0:
        await ctx.send(f"Your current score is {new_score} points. This is your first game!")
    else:
        await ctx.send(f"Your previous score was {previous_score} points, and now your score is {new_score} points.")

