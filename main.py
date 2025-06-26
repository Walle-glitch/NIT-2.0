# main.py - Refactored for Docker Compose setup

import os
import sys
import logging
from datetime import datetime
import subprocess
import asyncio

import discord
from discord.ext import commands, tasks
import openai

# Add Internal_Modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Internal_Modules'))

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

# Ensure required directories
os.makedirs('logs', exist_ok=True)
os.makedirs('Json_Files', exist_ok=True)

# Setup logging
logger = setup_logging()

# Bot intents and initialization
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load configuration
version_nr = getattr(_Bot_Config, '_Version', lambda: 'v1.0.0')()
XP_FILE = _Bot_Config._XP_File()
XP_UPDATE_CHANNEL_ID = _Bot_Config._XP_Update_Channel_ID()
LOG_CHANNEL_ID = _Bot_Config._Log_Channel_ID()

# Initialize external services
openai.api_key = _Bot_Config._Open_AI_Token()

# Setup modules
_Activity_Tracking.setup_file()
_Member_Moderation.setup(_Bot_Config._Admin_Channel_ID())
_Role_Management.setup(_Bot_Config._Role_Json_File())  # Ensure role file directory

# Load XP data
xp_data = _XP_Handler.load_xp_data()

async def log_to_channel(message: str):
    """Send logs to Discord and file."""
    logger.info(message)
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        try:
            await channel.send(message)
        except Exception as e:
            logger.error(f"Failed to send log: {e}")

@bot.event
async def on_ready():
    logger.info(f"Bot logged in as {bot.user}")
    await log_to_channel(f"✅ Logged in as {bot.user}")

    # Sync application commands
    try:
        await bot.tree.sync()
        await log_to_channel("Global commands synced.")
    except Exception as e:
        await log_to_channel(f"Sync failed: {e}")

    # Start background loops
    weekly_study_plan_CCNA.start()
    weekly_study_plan_CCNP.start()
    weekly_study_plan_CCIE.start()
    update_roles.start()
    job_posting_loop.start()
    # Start media posting loop if present
    media_loop = getattr(_Activity_Tracking, 'MediaPoster', None)
    if media_loop:
        media_loop(bot).start()

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # XP handling
    try:
        await _XP_Handler.handle_xp(message, XP_UPDATE_CHANNEL_ID)
    except Exception as e:
        logger.error(f"XP error: {e}")
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    try:
        await _XP_Handler.handle_reaction_xp(reaction.message, XP_UPDATE_CHANNEL_ID)
    except Exception as e:
        logger.error(f"Reaction XP error: {e}")
    # Activity tracking
    try:
        await _Activity_Tracking.track_activity(reaction.message.author, reaction.message.author, bot)
    except Exception:
        pass

# Setup slash commands
_Slash_Commands.setup(bot)
_Ticket_System.setup_ticketer(bot)

# Load auctions
_Auction.load_auctions()

# Basic text commands
@bot.command()
async def ping(ctx, ip: str = '8.8.8.8'):
    result = subprocess.run(['ping', '-c', '4', ip], capture_output=True, text=True)
    await ctx.send(f"```\n{result.stdout}\n```")

@bot.command()
async def version(ctx):
    """Show current bot version."""
    await ctx.send(version_nr)

# Role assignment commands
@bot.command(name='addrole')
async def addrole(ctx, *, role_name: str = None):
    """Assign a role via buttons or by name."""
    if not role_name:
        view = _Role_Management.create_role_buttons_view()
        await ctx.send("Select a role to assign:", view=view)
    else:
        await _Role_Management.assign_role(ctx, role_name)

@bot.command(name='removerole')
async def removerole(ctx, *, role_name: str = None):
    """Remove a role by name."""
    if not role_name:
        roles = _Role_Management.load_roles().keys()
        embed = discord.Embed(title="Available Roles for Removal", color=discord.Color.blue())
        for r in roles:
            if r not in _Bot_Config._Excluded_Roles():
                embed.add_field(name=r, value=f"Use `/removerole {r}`", inline=False)
        await ctx.send(embed=embed)
    else:
        await _Role_Management.remove_role(ctx, role_name)

# Admin reload modules
@bot.command()
@commands.has_role(_Bot_Config._Bot_Admin_Role_Name())
async def reload_module(ctx, module_name: str = None):
    modules = {
        'Role_Management': _Role_Management,
        'XP_Handler': _XP_Handler,
        'Auction': _Auction,
        'Game': _Game,
        'Moderation': _Member_Moderation,
    }
    if not module_name:
        await ctx.send(f"Modules: {', '.join(modules.keys())}")
        return
    mod = modules.get(module_name)
    if not mod:
        await ctx.send(f"Module not found: {module_name}")
        return
    try:
        import importlib; importlib.reload(mod)
        await ctx.send(f"Reloaded {module_name}")
    except Exception as e:
        await ctx.send(f"Reload failed: {e}")

# Study plan loops
def is_sunday():
    return datetime.now().weekday() == 6

@tasks.loop(hours=24)
async def weekly_study_plan_CCNA():
    if is_sunday():
        await _Cisco_Study_Plans._CCNA_Study_Plan.post_weekly_goal(bot, _Bot_Config._CCNA_Study_Channel_ID())

@tasks.loop(hours=24)
async def weekly_study_plan_CCNP():
    if is_sunday():
        await _Cisco_Study_Plans._CCNP_Study_Plan.post_weekly_goal(bot, _Bot_Config._CCNP_Study_Channel_ID())

@tasks.loop(hours=24)
async def weekly_study_plan_CCIE():
    if is_sunday():
        await _Cisco_Study_Plans._CCIE_Study_Plan.post_weekly_goal(bot, _Bot_Config._CCIE_Study_Channel_ID())

@tasks.loop(hours=1)
async def update_roles():
    try:
        await _Role_Management.fetch_and_save_roles(bot)
    except Exception as e:
        logger.error(f"Role update error: {e}")

@tasks.loop(hours=24)
async def job_posting_loop():
    try:
        await _Bot_Modul.fetch_and_post_jobs(bot, _Bot_Config._Job_Channel_ID())
    except Exception as e:
        logger.error(f"Job post error: {e}")

# Run
if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error('DISCORD_TOKEN not set')
        raise RuntimeError('Missing DISCORD_TOKEN')
    bot.run(token)