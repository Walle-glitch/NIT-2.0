import ipaddress
import random
import asyncio
import json
import os
import discord 
from discord import app_commands

# Global variables to keep track of current game state
current_question = None
correct_answer = None
game_type = None
game_task = None

# Path to the JSON file containing network questions
QUESTION_FILE = "./Json_Files/network_questions.json"

def load_network_questions():
    """
    Loads network questions from the JSON file.
    :return: A list of questions.
    """
    if os.path.exists(QUESTION_FILE):
        with open(QUESTION_FILE, "r") as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"{QUESTION_FILE} not found!")

async def start_game(ctx, chosen_game):
    global current_question, correct_answer, game_type, game_task

    # Check if a game is already in progress
    if game_task and not game_task.done():
        await ctx.send("A game is already in progress. Please use `/stop_game` to stop it first.")
        return

    game_type = chosen_game
    current_question, correct_answer = generate_question(chosen_game)

    intro_message = (
        "Welcome to the Network Game!\n\n"
        "Here's how to play:\n"
        "1. You will be asked a question related to IP subnets or network concepts.\n"
        "2. Please reply with your answer directly in this chat.\n"
        "3. The bot will check if your answer is correct and inform you accordingly.\n\n"
        "Good luck, and let's get started!\n\n"
        f"**Question:** {current_question}"
    )
    await ctx.send(intro_message)

    # Start the game timer
    game_task = asyncio.create_task(run_game_timer(ctx, 5 * 60))  # 5 minutes in seconds

def generate_question(game_type):
    """
    Generates a random question based on the chosen game type.
    :return: A tuple with the question and the correct answer.
    """
    if game_type == 'subnet':
        return generate_subnet_question()
    elif game_type == 'network':
        return generate_network_question()
    else:
        raise ValueError("Invalid game type")

################_Subnet_Questions_###################

def generate_subnet_question():
    """
    Generates a random IP address and CIDR and asks a subnet-related question.
    Returns a tuple with the question and the correct answer.
    """
    # Create a random IP address
    ip = ipaddress.IPv4Address(random.randint(0, 2**32 - 1))

    # Choose a random prefix length between /16 and /30
    prefix_length = random.randint(16, 30)

    # Create the network
    network = ipaddress.IPv4Network(f"{ip}/{prefix_length}", strict=False)

    # Choose a type of question
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

def check_answer(user_answer, correct_answer):
    """
    Compares the user's answer with the correct answer.
    Returns True if the answer is correct, otherwise False.
    """
    return user_answer.strip() == correct_answer

################_Network_Questions_###################

# Load network questions from the JSON file
questions = load_network_questions()

def generate_network_question():
    """
    Generates a random network-related question with options.
    :return: A tuple containing the question, options, and index of the correct answer.
    """
    question = random.choice(questions)
    return question["question"], question["options"], question["correct_option_index"]

def check_answer(selected_option_index, correct_option_index):
    """
    Checks if the selected answer is correct.
    :param selected_option_index: Index of the selected answer option.
    :param correct_option_index: Index of the correct answer option.
    :return: True if the selected option is correct, otherwise False.
    """
    return selected_option_index == correct_option_index

# Dictionary to keep track of scores for each user
user_scores = {}

def update_score(user_id, points):
    """
    Updates the score for the given user.
    :param user_id: ID of the user whose score is to be updated.
    :param points: Points to add to the user's score.
    """
    if user_id in user_scores:
        user_scores[user_id] += points
    else:
        user_scores[user_id] = points

def get_score(user_id):
    """
    Retrieves the score for the given user.
    :param user_id: ID of the user whose score is to be retrieved.
    :return: The score of the user.
    """
    return user_scores.get(user_id, 0)

async def run_game_timer(ctx, duration):
    """
    Runs a timer for the specified duration and stops the game when time is up.
    """
    await asyncio.sleep(duration)
    if game_task and not game_task.done():
        await ctx.send("Time is up! The game has ended.")
        reset_game()

def reset_game():
    global current_question, correct_answer, game_type, game_task
    current_question = None
    correct_answer = None
    game_type = None
    if game_task and not game_task.done():
        game_task.cancel()
        game_task = None
