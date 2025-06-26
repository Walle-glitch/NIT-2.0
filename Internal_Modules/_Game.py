# Internal_Modules/_Game.py
"""
Module for interactive subnet and network Q&A game in Discord.
Supports dynamic question generation, answer processing, and session management.
"""
import os
import json
import random
import asyncio
import ipaddress
import logging

import discord
from discord.ext import tasks

import _Bot_Config  # type: ignore
from _logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

# Path to network questions file
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JSON_DIR = os.path.join(PROJECT_ROOT, 'Json_Files')
os.makedirs(JSON_DIR, exist_ok=True)
QUESTIONS_FILE = _Bot_Config._Question_File()

# Game session state
game_active = False
game_initiator = None
current_game_type = None
current_question = None
correct_answer = None


def load_network_questions() -> list:
    """Load network Q&A questions from JSON file."""
    try:
        with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"Loaded {len(data)} network questions.")
        return data
    except FileNotFoundError:
        logger.error(f"Questions file not found: {QUESTIONS_FILE}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in questions file: {QUESTIONS_FILE}")
    return []


def generate_subnet_question() -> tuple:
    """Generate a random subnet question and return (question, answer)."""
    ip = ipaddress.IPv4Address(random.randint(0, 2**32 - 1))
    prefix = random.randint(16, 30)
    network = ipaddress.IPv4Network(f"{ip}/{prefix}", strict=False)
    qtype = random.choice(['network', 'broadcast', 'hosts'])
    if qtype == 'network':
        question = f"What is the network address for {network}?"
        answer = str(network.network_address)
    elif qtype == 'broadcast':
        question = f"What is the broadcast address for {network}?"
        answer = str(network.broadcast_address)
    else:
        question = f"How many usable hosts are in the subnet {network}?"
        answer = str(network.num_addresses - 2)
    logger.debug(f"Subnet Q: {question} | A: {answer}")
    return question, answer


def generate_network_question() -> tuple:
    """Select a random multiple-choice network question."""
    questions = load_network_questions()
    if not questions:
        return None, [], None
    q = random.choice(questions)
    question = q.get('question', '')
    options = q.get('options', [])
    correct_index = q.get('correct_option_index', 0)
    logger.debug(f"Network Q: {question} | Options: {options} | Correct: {correct_index}")
    return question, options, correct_index


async def start_game(ctx, game_type: str, Bot):
    """Begin Q&A game session of specified type."""
    global game_active, game_initiator, current_game_type
    if game_active:
        await ctx.send("A game is already in progress.")
        return
    game_active = True
    game_initiator = ctx.author
    current_game_type = game_type
    await ctx.send(f"Game started: {game_type}. Respond to questions or use !game_stop to end.")
    await next_question(ctx, bot)


async def next_question(ctx, Bot):
    """Ask the next question based on game type."""
    global current_question, correct_answer
    if current_game_type == 'subnet':
        q, a = generate_subnet_question()
        current_question, correct_answer = q, a
        await ctx.send(f"**Subnet:** {q}")
    else:  # network
        q, options, idx = generate_network_question()
        if q is None:
            await ctx.send("No network questions available.")
            return
        current_question = q
        correct_answer = idx
        opts = '\n'.join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
        await ctx.send(f"**Network:** {q}\n{opts}")
    # Wait for answer or timeout
    try:
        msg = await bot.wait_for(
            'message',
            check=lambda m: m.author == game_initiator and m.channel == ctx.channel,
            timeout=300
        )
        await process_answer(ctx, msg)
    except asyncio.TimeoutError:
        await ctx.send("Time's up! Game ended.")
        reset_game()


async def process_answer(ctx, message: discord.Message):
    """Check user's answer and respond, then ask next question."""
    global current_question, correct_answer
    ans = message.content.strip()
    if current_game_type == 'subnet':
        if ans == correct_answer:
            await ctx.send(f"Correct! {correct_answer}")
        else:
            await ctx.send(f"Incorrect. The answer was {correct_answer}.")
    else:
        try:
            choice = int(ans) - 1
            if choice == correct_answer:
                await ctx.send("Correct!")
            else:
                await ctx.send(f"Wrong. Option {correct_answer+1} was correct.")
        except ValueError:
            await ctx.send("Please reply with the option number.")
    # Continue game if still active
    if game_active:
        await next_question(ctx, ctx.bot)


def reset_game():
    """Reset all game state variables."""
    global game_active, game_initiator, current_game_type, current_question, correct_answer
    game_active = False
    game_initiator = None
    current_game_type = None
    current_question = None
    correct_answer = None
    logger.info("Game state reset.")


async def stop_game(ctx):
    """Command to manually stop the game."""
    if not game_active:
        await ctx.send("No game is currently running.")
    elif ctx.author != game_initiator:
        await ctx.send("Only the game initiator can stop the game.")
    else:
        reset_game()
        await ctx.send("Game has been stopped.")

# Optional: register tasks if needed

