import os
import json
import random
from datetime import datetime, timedelta
import discord
import _Bot_Config  # type: ignore

XP_FILE = _Bot_Config._XP_File()  # XP file location
LATE_NIGHT_ROLE_ID = _Bot_Config._LATE_NIGHT_ROLE_ID()
GUILD_ID = _Bot_Config._GUILD_ID()
ACTIVE_USERS_FILE = "/home/bot/NIT-2.0/bot/Json_Files/active_users.json"

# Load XP data globally
xp_data = {}

def load_xp_data():
    """Load XP data from a JSON file."""
    if os.path.exists(XP_FILE):
        try:
            with open(XP_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {XP_FILE} is empty or contains invalid JSON. Initializing an empty XP data structure.")
            return {}
    return {}

def save_xp_data(data):
    """Save XP data to a JSON file."""
    try:
        with open(XP_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving XP data: {str(e)}")

def xp_needed_for_level(level):
    """Determine the amount of XP needed to level up."""
    if level < 11:
        return 1000
    elif level < 101:
        return 10000
    else:
        return 20000

async def check_level_up(user, xp_update_channel_id, send_notifications=True):
    """Check if a user has leveled up based on their current XP."""
    user_id = str(user.id)
    user_data = xp_data.get(user_id, {})
    current_level = user_data.get("level", 1)
    xp_needed = xp_needed_for_level(current_level)

    if user_data["xp"] >= xp_needed:
        # Level up the user
        user_data["level"] += 1
        user_data["xp"] -= xp_needed  # Remove XP needed for the level up
        save_xp_data(xp_data)  # Save the updated XP data

        if send_notifications:
            # Notify the user in the appropriate channel
            channel = user.guild.get_channel(xp_update_channel_id)
            if channel:
                await channel.send(f"{user.mention} has leveled up to level {user_data['level']}!")

async def handle_xp(message, xp_update_channel_id, send_notifications=True):
    """Handle XP logic when a message is sent."""
    user = message.author
    user_id = str(user.id)

    # Initialize XP data for new users
    if user_id not in xp_data:
        xp_data[user_id] = {"xp": 0, "level": 1}

    # Add random XP
    xp_data[user_id]["xp"] += random.randint(5, 15)
    save_xp_data(xp_data)

    # Handle role management based on LateNightCrew activity
    await manage_late_night_role(user)

    # Check for level up
    await check_level_up(user, xp_update_channel_id, send_notifications)

def is_late_night():
    """Checks if the current time is between 22:00 and 05:00."""
    current_time = datetime.now().time()
    return current_time >= datetime.strptime("20:00", "%H:%M").time() or current_time <= datetime.strptime("05:00", "%H:%M").time()

def load_active_users():
    """Loads active users from the JSON file."""
    try:
        with open(ACTIVE_USERS_FILE, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading active users: {str(e)}")
        return {}

def save_active_users(active_users):
    """Saves active users to the JSON file."""
    try:
        with open(ACTIVE_USERS_FILE, 'w') as file:
            json.dump(active_users, file)
    except Exception as e:
        print(f"Error saving active users: {str(e)}")

async def add_late_night_role(member, role):
    """Assigns the LateNightCrew role to the member."""
    if role not in member.roles:
        await member.add_roles(role)
        print(f"Assigned LateNightCrew role to {member.name}")

async def remove_late_night_role(member, role):
    """Removes the LateNightCrew role from the member."""
    if role in member.roles:
        await member.remove_roles(role)
        print(f"Removed LateNightCrew role from {member.name}")

async def manage_late_night_role(user):
    """Handles assigning and removing the LateNightCrew role based on activity during late-night hours."""
    guild = user.guild
    role = guild.get_role(LATE_NIGHT_ROLE_ID)

    if role is None:
        print(f"LateNightCrew role with ID {LATE_NIGHT_ROLE_ID} not found in the guild.")
        return

    active_users = load_active_users()
    current_time = datetime.now()

    # Update the user's last active time
    active_users[str(user.id)] = current_time.isoformat()
    save_active_users(active_users)

    if is_late_night():
        # Add the role if it's late-night
        await add_late_night_role(user, role)

    # Check if there are any users who need the role removed due to inactivity (over 24 hours)
    for user_id, last_active_str in list(active_users.items()):
        last_active = datetime.fromisoformat(last_active_str)
        member = guild.get_member(int(user_id))
        if member and (current_time - last_active) > timedelta(hours=24):
            await remove_late_night_role(member, role)
            del active_users[user_id]  # Remove from active users

    # Save updated active users
    save_active_users(active_users)

async def handle_reaction_xp(message, xp_update_channel_id, send_notifications=True):
    """Handle XP logic when a reaction is added to a message."""
    user = message.author
    user_id = str(user.id)

    # Initialize XP data for new users
    if user_id not in xp_data:
        xp_data[user_id] = {"xp": 0, "level": 1}

    # Add XP for reactions
    xp_data[user_id]["xp"] += 10
    save_xp_data(xp_data)

    # Handle role management based on LateNightCrew activity
    await manage_late_night_role(user)

    # Check for level up
    await check_level_up(user, xp_update_channel_id, send_notifications)
