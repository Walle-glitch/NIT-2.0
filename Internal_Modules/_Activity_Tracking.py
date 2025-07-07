# Internal_Modules/_Activity_Tracking.py

import os
import json
from datetime import datetime, timedelta
import _Bot_Config  # type: ignore
from _logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

# Determine paths relative to project root
MODULE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(MODULE_DIR, '..'))
JSON_DIR = os.path.join(PROJECT_ROOT, 'Json_Files')
ACTIVE_USERS_FILE = os.path.join(JSON_DIR, 'active_users.json')

# Config values
GUILD_ID = _Bot_Config._Guild_ID()  # You need to add _Guild_ID() in _Bot_Config.py
LATE_NIGHT_ROLE_ID = _Bot_Config._Late_Night_Role_ID()


# --- RENAMED SETUP FUNCTION ---
def setup():
    """Ensure the activity tracking file exists."""
    if not os.path.exists(ACTIVE_USERS_FILE):
        with open(ACTIVE_USERS_FILE, 'w') as f:
            json.dump({}, f)
    logger.info("Activity Tracking module setup complete.")


def setup_file():
    """Ensure Json_Files directory and active_users.json exist."""
    try:
        os.makedirs(JSON_DIR, exist_ok=True)
        if not os.path.isfile(ACTIVE_USERS_FILE):
            with open(ACTIVE_USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            logger.info(f"Created file: {ACTIVE_USERS_FILE}")
    except Exception as e:
        logger.error(f"Error in setup_file: {e}")


def _get_server_time():
    """Return current server time as HH:MM:SS."""
    now = datetime.now()
    ts = now.strftime('%H:%M:%S')
    logger.debug(f"Server time: {ts}")
    return ts


def is_late_night():
    """Return True if current time between 00:01 and 05:00."""
    now = datetime.now().time()
    start = datetime.strptime('00:01', '%H:%M').time()
    end = datetime.strptime('05:00', '%H:%M').time()
    status = start <= now <= end
    logger.debug(f"is_late_night: {status} (current: {now})")
    return status


def load_active_users():
    """Load and return active users dict from file."""
    try:
        with open(ACTIVE_USERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"Loaded active_users: {len(data)} entries")
        return data
    except Exception as e:
        logger.error(f"Error loading active users: {e}")
        return {}


def save_active_users(active_users: dict):
    """Write active users dict to file."""
    try:
        with open(ACTIVE_USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(active_users, f)
        logger.debug(f"Saved {len(active_users)} active users")
    except Exception as e:
        logger.error(f"Error saving active users: {e}")


async def add_role(member, role):
    """Add LateNightCrew role to member if not present."""
    if role not in member.roles:
        await member.add_roles(role)
        logger.info(f"{_get_server_time()} - Added late-night role to {member}")


async def remove_role(member, role):
    """Remove LateNightCrew role from member if present."""
    if role in member.roles:
        await member.remove_roles(role)
        logger.info(f"{_get_server_time()} - Removed late-night role from {member}")


async def track_activity(before, after, bot):
    """Track status changes, assign/remove late-night role based on activity."""
    if after.bot:
        return
    try:
        guild = bot.get_guild(GUILD_ID)
        role = guild.get_role(LATE_NIGHT_ROLE_ID)

        active_users = load_active_users()
        now = datetime.now()

        # Update last active timestamp
        active_users[str(after.id)] = now.isoformat()
        save_active_users(active_users)

        # Assign role during late-night hours
        if is_late_night():
            await add_role(after, role)

        # Remove role for inactivity >14h
        for user_id, ts in list(active_users.items()):
            last_active = datetime.fromisoformat(ts)
            if (now - last_active) > timedelta(hours=14):
                member = guild.get_member(int(user_id))
                if member:
                    await remove_role(member, role)
                del active_users[user_id]
        save_active_users(active_users)

        # Reset file outside late-night
        if not is_late_night():
            save_active_users({})

    except Exception as e:
        logger.error(f"Error in track_activity: {e}")
