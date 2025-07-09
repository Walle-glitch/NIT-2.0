# Internal_Modules/_XP_Handler.py
"""
Module to handle XP gain, leveling, and late-night role management.
"""
import os
import json
import random
from datetime import datetime, timedelta
import logging
import discord

import _Bot_Config
from _logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

# In-memory data
xp_data = {}
active_users = {}

# This path is mainly for the active_users.json file now
JSON_DIR = "/app/Json_Files"
ACTIVE_USERS_FILE = os.path.join(JSON_DIR, 'active_users.json')

# --- Module Setup ---
def setup():
    """Initializes the XP module by loading data from file."""
    global xp_data
    xp_data = load_xp_data() # This will now produce better logs

# Lägg till denna funktion i Internal_Modules/_XP_Handler.py

def add_xp_for_history(user_id: int, user_name: str, amount: int):
    """
    A simplified function to add a bulk amount of XP to a user from history.
    This does NOT trigger a level-up check.
    """
    uid = str(user_id)
    user_entry = xp_data.setdefault(uid, {'xp': 0, 'level': 1, 'name': user_name})
    user_entry['name'] = user_name # Ensure username is up to date
    user_entry['xp'] += amount

# --- Data Loading and Saving with Enhanced Logging ---
def load_xp_data() -> dict:
    """Load XP data from JSON file."""
    # Get the absolute file path from the configuration
    xp_file_path = _Bot_Config._XP_File()
    
    logger.info(f"--- Attempting to load XP data from: '{xp_file_path}' ---")

    # 1. Check if the file exists
    if not os.path.exists(xp_file_path):
        logger.warning(f"XP file does NOT exist at the specified path. A new file will be created on next save. Initializing with empty data.")
        return {}
        
    # 2. Check if the file is practically empty
    if os.path.getsize(xp_file_path) < 5:
        logger.warning(f"XP file at '{xp_file_path}' is empty or too small. Initializing with empty data.")
        return {}

    # 3. Try to read and parse the file
    try:
        with open(xp_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"✅ Successfully loaded XP data for {len(data)} users from '{xp_file_path}'.")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"🔥 FAILED to parse JSON from '{xp_file_path}'. The file might be corrupt. Error: {e}")
        return {}
    except Exception as e:
        logger.error(f"🔥 An unexpected error occurred while reading '{xp_file_path}': {e}")
        return {}

def save_xp_data(data: dict):
    """Persist XP data to JSON file."""
    # Always get the correct, absolute path from config
    xp_file_path = _Bot_Config._XP_File()
    try:
        with open(xp_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        # Using debug here to avoid spamming logs on every save
        logger.debug(f"Saved XP data for {len(data)} users to '{xp_file_path}'.")
    except Exception as e:
        logger.error(f"Failed to save XP data to '{xp_file_path}': {e}")

# --- XP and Leveling Logic (Unchanged) ---
def xp_needed_for_level(level: int) -> int:
    """Calculate XP needed to level up."""
    if level < 11:
        return 1000
    if level < 101:
        return 10000
    return 20000

async def check_level_up(member: discord.Member, xp_update_channel_id: int):
    """Check and process level up for a member."""
    user_id = str(member.id)
    user = xp_data.get(user_id)
    if not user:
        return
        
    current_level = user.get('level', 1)
    xp_needed = xp_needed_for_level(current_level)
    
    if user.get('xp', 0) >= xp_needed:
        user['xp'] -= xp_needed
        user['level'] = current_level + 1
        save_xp_data(xp_data)
        
        channel = member.guild.get_channel(xp_update_channel_id)
        if channel:
            try:
                await channel.send(f"{member.mention} leveled up to {user['level']}!")
            except discord.Forbidden:
                logger.warning(f"Missing permissions to send level up message in channel {xp_update_channel_id}")
        logger.info(f"{member.display_name} leveled up to {user['level']}")

# --- Public Interface (Unchanged) ---
async def handle_xp(message: discord.Message, xp_update_channel_id: int):
    """Call on incoming messages to award XP."""
    if message.author.bot:
        return

    user = message.author
    uid = str(user.id)
    
    # Use setdefault to create a new user entry if it doesn't exist
    user_entry = xp_data.setdefault(uid, {'xp': 0, 'level': 1, 'name': user.name})
    
    # Update username if it has changed
    user_entry['name'] = user.name
    
    user_entry['xp'] += random.randint(5, 15)
    
    await check_level_up(user, xp_update_channel_id)

async def handle_reaction_xp(reaction_message: discord.Message, xp_update_channel_id: int):
    """Call on reaction add to award XP."""
    if reaction_message.author.bot:
        return
        
    user = reaction_message.author
    uid = str(user.id)
    
    user_entry = xp_data.setdefault(uid, {'xp': 0, 'level': 1, 'name': user.name})
    
    user_entry['name'] = user.name
    user_entry['xp'] += 10
    
    await check_level_up(user, xp_update_channel_id)

# Lägg till denna funktion i Internal_Modules/_XP_Handler.py

def recalculate_all_levels() -> tuple[int, int]:
    """
    Iterates through all users in xp_data and calculates their correct level
    based on their current XP. This is a batch operation.
    Returns the number of users updated and total levels gained.
    """
    users_updated = 0
    total_levels_gained = 0

    # Create a copy of the items to iterate over, as we might modify the dict
    for user_id, user_data in list(xp_data.items()):
        leveled_up = False
        # Use a while loop in case a user gained enough XP for multiple levels
        while user_data.get('xp', 0) >= xp_needed_for_level(user_data.get('level', 1)):
            current_level = user_data.get('level', 1)
            needed = xp_needed_for_level(current_level)
            
            user_data['xp'] -= needed
            user_data['level'] += 1
            total_levels_gained += 1
            leveled_up = True
            
            logger.info(f"User {user_data.get('name', user_id)} leveled up to {user_data['level']} during recalculation.")

        if leveled_up:
            users_updated += 1
            
    if total_levels_gained > 0:
        save_xp_data(xp_data)
        
    return users_updated, total_levels_gained


# Note: Late-night role management was removed from this file in a previous step
# as it was not being used by the main logic. It can be re-added if needed.