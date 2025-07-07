# main.py - Refactored for Modular Setup Functions

import os
import sys
import logging
import asyncio
from datetime import datetime
import discord
from discord.ext import commands, tasks

# Add Internal_Modules to path to allow for absolute imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'Internal_Modules'))

# Import all your custom modules
import _Bot_Config
import _Cisco_Study_Plans
import _Role_Management
import _XP_Handler
import _Member_Moderation
import _Game
import _Bot_Modul
import _Auction
import _Slash_Commands
import _Activity_Tracking
import _Ticket_System
from _logging_setup import setup_logging

# --- 1. Initial Setup ---
os.makedirs('logs', exist_ok=True)
os.makedirs('Json_Files', exist_ok=True)
logger = setup_logging()

# Bot intents and initialization
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=None, intents=intents) # No prefix needed for slash-only bot

# Load configuration
try:
    BOT_TOKEN = _Bot_Config._Bot_Token()
    XP_UPDATE_CHANNEL_ID = _Bot_Config._XP_Update_Channel_ID()
    LOG_CHANNEL_ID = _Bot_Config._Log_Channel_ID()
    JOB_CHANNEL_ID = _Bot_Config._Job_Channel_ID()
    CCNA_CHANNEL_ID = _Bot_Config._CCNA_Study_Channel_ID()
    CCNP_CHANNEL_ID = _Bot_Config._CCNP_Study_Channel_ID()
    CCIE_CHANNEL_ID = _Bot_Config._CCIE_Study_Channel_ID()
    VERSION_NR = "v2.3.0" # Version bump for setup() refactoring
except Exception as e:
    logger.critical(f"Could not load essential configuration from _Bot_Config.py. Error: {e}")
    sys.exit("Fatal: Configuration error.")


# --- 2. Module Setup ---
# A list of all modules that need initialization.
# Modules needing the 'bot' object are passed as a tuple.
ALL_MODULES = [
    _XP_Handler,
    _Activity_Tracking,
    _Role_Management,
    _Auction,
    _Bot_Modul,
    (_Slash_Commands, bot),
    (_Game, bot),
    (_Ticket_System, bot),
    (_Member_Moderation, bot)
]

def initialize_modules():
    """Calls the setup() function for all modules in the list."""
    logger.info("--- Initializing All Modules ---")
    for item in ALL_MODULES:
        try:
            if isinstance(item, tuple):
                module, bot_instance = item
                module_name = module.__name__
                module.setup(bot_instance)
            else:
                module = item
                module_name = module.__name__
                module.setup()
            logger.info(f"✅ Module '{module_name}' initialized successfully.")
        except Exception as e:
            logger.error(f"🔥 Failed to initialize module '{module_name}'. Error: {e}", exc_info=True)
    logger.info("--- All Modules Initialized ---")


# --- 3. Background Tasks & Events ---

@tasks.loop(minutes=5)
async def save_xp_data_loop():
    """Periodically saves the in-memory XP data to the JSON file."""
    await bot.wait_until_ready()
    try:
        _XP_Handler.save_xp_data(_XP_Handler.xp_data)
        logger.info("Periodic XP data save successful.")
    except Exception as e:
        logger.error(f"Error in periodic XP save loop: {e}")


@bot.event
async def on_ready():
    """Runs once when the bot is connected and ready."""
    print("-" * 30)
    logger.info(f"Bot logged in as {bot.user.name} ({bot.user.id})")
    print(f"Bot logged in as {bot.user.name}")
    print("-" * 30)

    # --- Centralized Module Initialization ---
    initialize_modules()

    # Safeguard to prevent data loss on XP loading error
    xp_file_path = _Bot_Config._XP_File()
    if not _XP_Handler.xp_data and os.path.exists(xp_file_path) and os.path.getsize(xp_file_path) > 10:
        fatal_error_msg = "FATAL ERROR: XP data loading returned empty, but the data file is not empty! To prevent data loss, the bot will now shut down."
        logger.critical(fatal_error_msg)
        # await log_to_channel(fatal_error_msg) # This function might not be ready
        await bot.close()
        return

    # Sync Slash Commands to Discord
    try:
        await bot.tree.sync()
        logger.info("Global slash commands synced.")
    except Exception as e:
        logger.error(f"Slash command sync failed: {e}")

    # Start all background tasks
    save_xp_data_loop.start()
    weekly_study_plan_CCNA.start()
    weekly_study_plan_CCNP.start()
    weekly_study_plan_CCIE.start()
    update_roles.start()
    job_posting_loop.start()

    await log_to_channel(f"✅ Bot is online and all tasks have started. Version: {VERSION_NR}")


@bot.event
async def on_message(message: discord.Message):
    """Handles incoming messages for XP gain."""
    if message.author.bot:
        return
    try:
        await _XP_Handler.handle_xp(message, XP_UPDATE_CHANNEL_ID)
    except Exception as e:
        logger.error(f"Error in handle_xp on_message: {e}", exc_info=False)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """Handles incoming reactions for XP gain."""
    if payload.user_id == bot.user.id:
        return
    channel = bot.get_channel(payload.channel_id)
    if not channel: return
    try:
        message = await channel.fetch_message(payload.message_id)
        if message.author.bot: return
        await _XP_Handler.handle_reaction_xp(message, XP_UPDATE_CHANNEL_ID)
    except discord.NotFound:
        return
    except Exception as e:
        logger.error(f"Error in on_raw_reaction_add: {e}", exc_info=False)

async def log_to_channel(message: str):
    """Sends a log message to the designated Discord channel."""
    logger.info(message)
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        try:
            await log_channel.send(f"```{datetime.now():%Y-%m-%d %H:%M:%S} - {message}```")
        except Exception as e:
            logger.error(f"Failed to send log message to channel {LOG_CHANNEL_ID}: {e}")


# --- 4. Looping Tasks ---

def is_sunday():
    """Helper function to check if the current day is Sunday."""
    return datetime.now().weekday() == 6

@tasks.loop(hours=24)
async def weekly_study_plan_CCNA():
    """Posts the weekly CCNA study plan on Sundays."""
    if is_sunday():
        await _Cisco_Study_Plans._CCNA_Study_Plan.post_weekly_goal(bot, CCNA_CHANNEL_ID)

@tasks.loop(hours=24)
async def weekly_study_plan_CCNP():
    """Posts the weekly CCNP study plan on Sundays."""
    if is_sunday():
        await _Cisco_Study_Plans._CCNP_Study_Plan.post_weekly_goal(bot, CCNP_CHANNEL_ID)

@tasks.loop(hours=24)
async def weekly_study_plan_CCIE():
    """Posts the weekly CCIE study plan on Sundays."""
    if is_sunday():
        await _Cisco_Study_Plans._CCIE_Study_Plan.post_weekly_goal(bot, CCIE_CHANNEL_ID)

@tasks.loop(hours=1)
async def update_roles():
    """Periodically fetches and saves all server roles to a JSON file."""
    try:
        await _Role_Management.fetch_and_save_roles(bot)
    except Exception as e:
        logger.error(f"Role update task failed: {e}")

@tasks.loop(hours=24)
async def job_posting_loop():
    """Fetches and posts new job listings daily."""
    try:
        await _Bot_Modul.fetch_and_post_jobs(bot, JOB_CHANNEL_ID)
    except Exception as e:
        logger.error(f"Job posting task failed: {e}")


# --- 5. Run the Bot ---
if __name__ == '__main__':
    if not BOT_TOKEN:
        logger.critical('FATAL: DISCORD_TOKEN is not set!')
        raise RuntimeError('Missing DISCORD_TOKEN. The bot cannot start.')
    try:
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        logger.critical("FATAL: Login failed. The provided Discord token is invalid.")
    except Exception as e:
        logger.critical(f"FATAL: An unexpected error occurred during bot startup: {e}")