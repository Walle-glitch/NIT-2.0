# _Games.py

import ipaddress
import random
import asyncio

# Global variables to keep track of current game state
current_question = None
correct_answer = None
game_type = None
game_task = None

async def start_game(ctx, chosen_game):
    global current_question, correct_answer, game_type, game_task

    if game_task and not game_task.done():
        await ctx.send("A game is already in progress. Please use `./stop_game` to stop it first.")
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
    """
    if game_type == 'subnet':
        return generate_subnet_question()
    elif game_type == 'network':
        return generate_network_question()
    else:
        raise ValueError("Invalid game type")

def generate_subnet_question():
    """
    Generates a random IP address and CIDR and asks a subnet-related question.
    Returns a tuple with the question and the correct answer.
    """
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
    else:
        question = f"How many hosts can be in the subnet {network}?"
        correct_answer = str(network.num_addresses - 2)
    
    return question, correct_answer

def generate_network_question():
    """
    Generates a random network-related question (e.g., BGP configuration).
    """
    questions = [
        ("What is the default administrative distance for eBGP?", "20"),
        ("What command shows the BGP neighbors?", "show ip bgp summary"),
        ("Which protocol is used for routing between different ASes?", "eBGP"),
        # Add more questions as needed
    ]
    return random.choice(questions)

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

def check_answer(user_answer):
    """
    Compares the user's answer with the correct answer.
    Returns True if the answer is correct, otherwise False.
    """
    return user_answer.strip() == correct_answer
