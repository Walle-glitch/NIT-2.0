import random
import json
import ipaddress
import asyncio
import logging
import _Bot_Config # type: ignore

# Game state variables
game_task = None
game_initiator = None     # Track the user who initiated the game
current_question = None
correct_answer = None
current_game_type = None  # Track the game type
game_active = False       # Flag to keep track of the game state
Net_questions = _Bot_Config._Question_File()

logger = logging.getLogger(__name__)

#### Helper Functions to Load Questions ###

def load_network_questions():
    """Loads network questions from the JSON file."""
    try:
        with open(Net_questions, "r") as f:
            logger.debug("Loaded network questions from JSON file.")
            return json.load(f)
    except FileNotFoundError as e:
        logger.error(f"Error loading questions: {e}")
        return []

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
    else:
        question = f"How many hosts can be in the subnet {network}?"
        correct_answer = str(network.num_addresses - 2)
    
    logger.debug(f"Generated subnet question: {question}, Correct answer: {correct_answer}")
    return question, correct_answer

def generate_network_question():
    """Generates a random network-related question from the loaded JSON file."""
    questions = load_network_questions()
    if questions:
        question_data = random.choice(questions)
        question = question_data["question"]
        options = question_data["options"]
        correct_index = question_data["correct_option_index"]
        logger.debug(f"Generated network question: {question}, Correct index: {correct_index}")
        return question, options, correct_index
    else:
        logger.warning("No network questions available in the JSON file.")
        return "No network questions found.", [], 0

# Game Logic
async def start_game(ctx, game_type, bot):
    """Starts a game based on the selected game type and continues until timeout or game stop."""
    global current_question, correct_answer, current_game_type, game_initiator, game_active
    
    if game_active:
        await ctx.send("A game is already in progress. Please finish it first.")
        return

    current_game_type = game_type
    game_initiator = ctx.author
    game_active = True

    await ctx.send(f"Game started by {game_initiator.mention}! Answer the questions or use !game_stop to end.")

    while game_active:
        await ask_next_question(ctx)
        def check(m):
            return m.author == game_initiator and m.channel == ctx.channel

        try:
            user_response = await bot.wait_for('message', check=check, timeout=300)  # 5 minutes timeout
            await process_answer(ctx, user_response)
        except asyncio.TimeoutError:
            await ctx.send(f"Time's up, {game_initiator.mention}! The game has ended due to inactivity.")
            reset_game()
            break

async def ask_next_question(ctx):
    """Generates and sends the next question based on the current game type."""
    global current_question, correct_answer, current_game_type

    if current_game_type == 'subnet':
        current_question, correct_answer = generate_subnet_question()
        await ctx.send(f"Subnet question: {current_question}")
    elif current_game_type == 'network':
        question, options, correct_index = generate_network_question()
        options_str = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
        current_question = f"{question}\n\n{options_str}"
        correct_answer = correct_index
        await ctx.send(f"Network question:\n{current_question}")

async def process_answer(ctx, message):
    """Processes the answer from the user."""
    global current_question, correct_answer, current_game_type

    user_answer = message.content.strip()
    logger.debug(f"Processing answer from {message.author}: {user_answer}")

    if current_game_type == 'subnet':
        if user_answer == correct_answer:
            await ctx.send(f"Correct! The answer was {correct_answer}.")
            logger.info(f"Correct answer by {message.author}")
        else:
            await ctx.send(f"Wrong answer. The correct answer is {correct_answer}.")
            logger.info(f"Wrong answer by {message.author}")
    elif current_game_type == 'network':
        try:
            selected_option = int(user_answer) - 1
            if selected_option == correct_answer:
                await ctx.send("Correct!")
                logger.info(f"Correct answer by {message.author}")
            else:
                await ctx.send(f"Wrong answer. The correct option was {correct_answer + 1}.")
                logger.info(f"Wrong answer by {message.author}")
        except ValueError:
            await ctx.send("Please respond with the option number (1, 2, 3, etc.).")
            logger.warning(f"Invalid input from {message.author}: {message.content}")

def reset_game():
    """Resets the game state."""
    global current_question, correct_answer, current_game_type, game_initiator, game_active
    current_question = None
    correct_answer = None
    current_game_type = None
    game_initiator = None
    game_active = False
    logger.info("Game state has been reset.")
