import os
import json
from datetime import datetime, timedelta
import logging
import sys

import discord

import _Bot_Config  # type: ignore
import _Bot_Modul

# File paths and constants
ACTIVE_USERS_FILE = "/home/bot/NIT-2.0/bot/Json_Files/active_users.json"
GUILD_ID = _Bot_Config._GUILD_ID()
LATE_NIGHT_ROLE_ID = _Bot_Config._LATE_NIGHT_ROLE_ID()
get_server_time = _Bot_Modul._get_server_time()

# Setup logging
logger = logging.getLogger(__name__)

def setup_file():
    if not os.path.exists("/home/bot/NIT-2.0/bot/Json_Files"):
        os.makedirs("/home/bot/NIT-2.0/bot/Json_Files")
    
    if not os.path.isfile(ACTIVE_USERS_FILE):
        with open(ACTIVE_USERS_FILE, 'w') as file:
            json.dump({}, file)

def is_late_night():
    """Checks if the current time is between 00:01 and 05:00."""
    current_time = get_server_time()
    return current_time >= datetime.strptime("00:01", "%H:%M").time() and current_time <= datetime.strptime("05:00", "%H:%M").time()

def load_active_users():
    """Loads active users from the JSON file."""
    with open(ACTIVE_USERS_FILE, 'r') as file:
        return json.load(file)

def save_active_users(active_users):
    """Saves active users to the JSON file."""
    with open(ACTIVE_USERS_FILE, 'w') as file:
        json.dump(active_users, file)

async def add_role(member, role):
    """Assigns the LateNightCrew role to the member."""
    if role not in member.roles:
        await member.add_roles(role)
        logger.info(f"{get_server_time()} Assigned LateNightCrew role to {member.name}")

async def remove_role(member, role):
    """Removes the LateNightCrew role from the member."""
    if role in member.roles:
        await member.remove_roles(role)
        logger.info(f"{get_server_time()} Removed LateNightCrew role from {member.name}")

async def track_activity(message, bot):
    """Tracks user activity and manages roles based on activity."""
    if message.author.bot:
        return

    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(LATE_NIGHT_ROLE_ID)
    active_users = load_active_users()
    current_time = datetime.now()

    # Update activity
    active_users[message.author.id] = current_time.isoformat()
    save_active_users(active_users)

    # Handle LateNightCrew role
    if is_late_night():
        await add_role(message.author, role)

    # Remove role if inactive for more than 14 hours
    for user_id, last_active_str in list(active_users.items()):
        last_active = datetime.fromisoformat(last_active_str)
        member = guild.get_member(int(user_id))
        if member and (current_time - last_active) > timedelta(hours=14):
            await remove_role(member, role)
            del active_users[user_id]

    # Update JSON file
    save_active_users(active_users)

    # Clear the file after 05:00
    if not is_late_night():
        with open(ACTIVE_USERS_FILE, 'w') as file:
            json.dump({}, file)
