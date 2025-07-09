# main.py - Corrected Module Initialization

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
import _Bot_Modul
import _Slash_Commands
import _Activity_Tracking
import _Gemini_Handler
from _logging_setup import setup_logging

# --- 1. Initial Setup ---
os.makedirs('logs', exist_ok=True)
os.makedirs('Json_Files', exist_ok=True)
logger = setup_logging()

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=None, intents=intents)

# Load configuration
try:
    BOT_TOKEN = _Bot_Config._Bot_Token()
    XP_UPDATE_CHANNEL_ID = _Bot_Config._XP_Update_Channel_ID()
    LOG_CHANNEL_ID = _Bot_Config._Log_Channel_ID()
    JOB_CHANNEL_ID = _Bot_Config._Job_Channel_ID()
    CCNA_CHANNEL_ID = _Bot_Config._CCNA_Study_Channel_ID()
    CCNP_CHANNEL_ID = _Bot_Config._CCNP_Study_Channel_ID()
    CCIE_CHANNEL_ID = _Bot_Config._CCIE_Study_Channel_ID()
    VERSION_NR = _Bot_Config._Version_Number()
except Exception as e:
    logger.critical(f"Could not load essential configuration from _Bot_Config.py. Error: {e}")
    sys.exit("Fatal: Configuration error.")


# --- 2. Module Setup ---
# This list now only contains modules that DO NOT register commands.
# Command-registering modules are handled by _Slash_Commands.setup()
MODULES_TO_SETUP = [
    _XP_Handler,
    _Activity_Tracking,
    _Role_Management,
    _Bot_Modul,
]

def initialize_modules():
    """Calls the setup() function for all modules."""
    logger.info("--- Initializing All Modules ---")
    
    # Setup non-command modules first
    for module in MODULES_TO_SETUP:
        try:
            module_name = module.__name__
            module.setup()
            logger.info(f"✅ Module '{module_name}' initialized successfully.")
        except Exception as e:
            logger.error(f"🔥 Failed to initialize module '{module_name}'. Error: {e}", exc_info=True)

    # Setup the main slash command handler, which will in turn set up other command modules.
    try:
        _Slash_Commands.setup(bot)
        logger.info("✅ Slash Command module and its sub-modules initialized successfully.")
    except Exception as e:
        logger.error(f"🔥 Failed to initialize _Slash_Commands. Error: {e}", exc_info=True)
        
    logger.info("--- All Modules Initialized ---")


# --- 3. Bot Events & Tasks ---
@bot.event
async def on_ready():
    print("-" * 30)
    logger.info(f"Bot logged in as {bot.user.name} ({bot.user.id})")
    print(f"Bot logged in as {bot.user.name}")
    print("-" * 30)

    initialize_modules()

    # Safeguard to prevent data loss
    xp_file_path = _Bot_Config._XP_File()
    if not _XP_Handler.xp_data and os.path.exists(xp_file_path) and os.path.getsize(xp_file_path) > 10:
        logger.critical("FATAL ERROR: XP data loading returned empty, but the data file is not empty! Shutting down to prevent data loss.")
        await bot.close()
        return

    # Sync Slash Commands
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


# ... (The rest of the main.py file, including tasks and events, remains the same)
@tasks.loop(minutes=5)
async def save_xp_data_loop():
    await bot.wait_until_ready()
    try:
        _XP_Handler.save_xp_data(_XP_Handler.xp_data)
        logger.debug("Periodic XP data save successful.") # Changed to debug to reduce log spam
    except Exception as e:
        logger.error(f"Error in periodic XP save loop: {e}")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot: return
    await _XP_Handler.handle_xp(message, XP_UPDATE_CHANNEL_ID)

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.user_id == bot.user.id: return
    channel = bot.get_channel(payload.channel_id)
    if not channel: return
    try:
        message = await channel.fetch_message(payload.message_id)
        if message.author.bot: return
        await _XP_Handler.handle_reaction_xp(message, XP_UPDATE_CHANNEL_ID)
    except discord.NotFound: return
    except Exception as e: logger.error(f"Error in on_raw_reaction_add: {e}")

async def log_to_channel(message: str):
    logger.info(message)
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(f"```{datetime.now():%Y-%m-%d %H:%M:%S} - {message}```")

def is_sunday(): return datetime.now().weekday() == 6

@tasks.loop(hours=24)
async def weekly_study_plan_CCNA():
    if is_sunday(): await _Cisco_Study_Plans._CCNA_Study_Plan.post_weekly_goal(bot, CCNA_CHANNEL_ID)

@tasks.loop(hours=24)
async def weekly_study_plan_CCNP():
    if is_sunday(): await _Cisco_Study_Plans._CCNP_Study_Plan.post_weekly_goal(bot, CCNP_CHANNEL_ID)

@tasks.loop(hours=24)
async def weekly_study_plan_CCIE():
    if is_sunday(): await _Cisco_Study_Plans._CCIE_Study_Plan.post_weekly_goal(bot, CCIE_CHANNEL_ID)

@tasks.loop(hours=1)
async def update_roles():
    await _Role_Management.fetch_and_save_roles(bot)

@tasks.loop(hours=24)
async def job_posting_loop():
    await _Bot_Modul.fetch_and_post_jobs(bot, JOB_CHANNEL_ID)

if __name__ == '__main__':
    if not BOT_TOKEN:
        logger.critical('FATAL: DISCORD_TOKEN is not set!')
    else:
        bot.run(BOT_TOKEN)