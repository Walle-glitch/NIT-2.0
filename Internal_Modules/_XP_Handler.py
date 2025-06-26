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

import _Bot_Config  # type: ignore
from _logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

# Paths
MODULE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(MODULE_DIR, '..'))
JSON_DIR = os.path.join(PROJECT_ROOT, 'Json_Files')
os.makedirs(JSON_DIR, exist_ok=True)

# XP data file
XP_FILE = _Bot_Config._XP_File()
# Active users file used by late-night role manager
ACTIVE_USERS_FILE = os.path.join(JSON_DIR, 'active_users.json')
# Late night role and guild config
LATE_NIGHT_ROLE_ID = _Bot_Config._Late_Night_Role_ID()
GUILD_ID = _Bot_Config._Guild_ID()

# In-memory data
xp_data = {}
active_users = {}


def load_xp_data() -> dict:
    """Load XP data from JSON file."""
    try:
        with open(XP_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"Loaded XP data for {len(data)} users.")
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning(f"XP file missing or invalid: {XP_FILE}, initializing empty.")
        return {}


def save_xp_data(data: dict):
    """Persist XP data to JSON file."""
    try:
        with open(XP_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        logger.debug(f"Saved XP data for {len(data)} users.")
    except Exception as e:
        logger.error(f"Failed to save XP data: {e}")


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
        # Notify channel
        channel = member.guild.get_channel(xp_update_channel_id)
        if channel:
            await channel.send(f"{member.mention} leveled up to {user['level']}!")
        logger.info(f"{member} leveled up to {user['level']}")


# -----------------------------------
# Late-night role management
# -----------------------------------

def _load_active_users() -> dict:
    """Load last activity times for users."""
    try:
        with open(ACTIVE_USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_active_users(data: dict):
    """Save last activity times."""
    try:
        with open(ACTIVE_USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save active users: {e}")


def is_late_night() -> bool:
    """Return True if now is between 20:00 and 05:00."""
    now = datetime.now().time()
    return now >= datetime.strptime('20:00', '%H:%M').time() or now <= datetime.strptime('05:00', '%H:%M').time()

async def manage_late_night_role(member: discord.Member):
    """Assign or remove late-night role based on activity."""
    guild = member.guild
    role = guild.get_role(LATE_NIGHT_ROLE_ID)
    if not role:
        logger.warning(f"Late-night role ID {LATE_NIGHT_ROLE_ID} not found.")
        return
    # Load state
    global active_users
    active_users = _load_active_users()
    # Update last active timestamp
    active_users[str(member.id)] = datetime.now().isoformat()
    _save_active_users(active_users)
    # Assign role if late-night
    if is_late_night():
        if role not in member.roles:
            await member.add_roles(role)
            logger.info(f"Assigned late-night role to {member}")
    # Remove stale roles
    now = datetime.now()
    for uid, ts in list(active_users.items()):
        last = datetime.fromisoformat(ts)
        if now - last > timedelta(hours=24):
            m = guild.get_member(int(uid))
            if m and role in m.roles:
                await m.remove_roles(role)
                logger.info(f"Removed late-night role from {m}")
            active_users.pop(uid)
    _save_active_users(active_users)

# -----------------------------------
# Public interface
# -----------------------------------

async def handle_xp(message: discord.Message, xp_update_channel_id: int):
    """Call on incoming messages to award XP and manage roles."""
    global xp_data
    xp_data = load_xp_data()
    user = message.author
    uid = str(user.id)
    user_entry = xp_data.setdefault(uid, {'xp': 0, 'level': 1})
    # Add random XP
    user_entry['xp'] += random.randint(5, 15)
    save_xp_data(xp_data)
    # Manage late-night role
    await manage_late_night_role(user)
    # Check level up
    await check_level_up(user, xp_update_channel_id)

async def handle_reaction_xp(reaction_message: discord.Message, xp_update_channel_id: int):
    """Call on reaction add to award XP."""
    global xp_data
    xp_data = load_xp_data()
    user = reaction_message.author
    uid = str(user.id)
    user_entry = xp_data.setdefault(uid, {'xp': 0, 'level': 1})
    user_entry['xp'] += 10
    save_xp_data(xp_data)
    await manage_late_night_role(user)
    await check_level_up(user, xp_update_channel_id)