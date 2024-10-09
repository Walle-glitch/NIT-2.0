import os
import json
from datetime import datetime, timedelta
import logging
import sys
import discord

import _Bot_Config  # type: ignore

def _get_server_time():
    """Hämta den aktuella server-tiden och returnera i formatet HH:MM:SS (utan mikrosekunder)"""
    server_time = datetime.now()
    formatted_time = server_time.strftime('%H:%M:%S')
    logger.debug(f"Server-tid hämtad: {formatted_time}")
    return formatted_time

# File paths and constants
ACTIVE_USERS_FILE = "/home/bot/NIT-2.0/bot/Json_Files/active_users.json"
GUILD_ID = _Bot_Config._GUILD_ID()
LATE_NIGHT_ROLE_ID = _Bot_Config._LATE_NIGHT_ROLE_ID()
get_server_time = _get_server_time()

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename=f'logs/log-{datetime.now().strftime("%Y-%m-%d")}.txt',
                    format='%(asctime)s %(levelname)s: %(message)s')

def setup_file():
    """Kolla om filen existerar, annars skapa en ny."""
    try:
        if not os.path.exists("/home/bot/NIT-2.0/bot/Json_Files"):
            os.makedirs("/home/bot/NIT-2.0/bot/Json_Files")
            logger.info("Mapp 'Json_Files' skapad.")

        if not os.path.isfile(ACTIVE_USERS_FILE):
            with open(ACTIVE_USERS_FILE, 'w') as file:
                json.dump({}, file)
            logger.info(f"Fil '{ACTIVE_USERS_FILE}' skapad.")
    except Exception as e:
        logger.error(f"Fel vid setup_file: {str(e)}")

def is_late_night():
    """Checks if the current time is between 00:01 and 05:00."""
    current_time = datetime.now().time()  # Fixat här för att använda datetime objekt korrekt
    logger.debug(f"Kollar om det är Late Night: {current_time}")
    return current_time >= datetime.strptime("00:01", "%H:%M").time() and current_time <= datetime.strptime("05:00", "%H:%M").time()

def load_active_users():
    """Loads active users from the JSON file."""
    try:
        with open(ACTIVE_USERS_FILE, 'r') as file:
            logger.debug(f"Laddar aktiva användare från {ACTIVE_USERS_FILE}.")
            return json.load(file)
    except Exception as e:
        logger.error(f"Fel vid läsning av aktiva användare: {str(e)}")
        return {}

def save_active_users(active_users):
    """Saves active users to the JSON file."""
    try:
        with open(ACTIVE_USERS_FILE, 'w') as file:
            json.dump(active_users, file)
        logger.debug(f"Aktiva användare sparade till {ACTIVE_USERS_FILE}.")
    except Exception as e:
        logger.error(f"Fel vid sparning av aktiva användare: {str(e)}")

async def add_role(member, role):
    """Assigns the LateNightCrew role to the member."""
    if role not in member.roles:
        await member.add_roles(role)
        logger.info(f"{get_server_time()} Tilldelade LateNightCrew-roll till {member.name}")

async def remove_role(member, role):
    """Removes the LateNightCrew role from the member."""
    if role in member.roles:
        await member.remove_roles(role)
        logger.info(f"{get_server_time()} Tog bort LateNightCrew-roll från {member.name}")

async def track_activity(message, bot):
    """Tracks user activity and manages roles based on activity."""
    if message.author.bot:
        return

    try:
        # Ladda guild och rollen
        guild = bot.get_guild(GUILD_ID)
        role = guild.get_role(LATE_NIGHT_ROLE_ID)

        active_users = load_active_users()
        current_time = datetime.now()

        # Debug: uppdatering av aktivitet
        logger.debug(f"Användare {message.author.name} aktivitet uppdaterad: {current_time}")
        active_users[message.author.id] = current_time.isoformat()
        save_active_users(active_users)

        # Debug: LateNightCrew rollhantering
        if is_late_night():
            logger.debug(f"Tilldelar LateNightCrew-roll till {message.author.name}")
            await add_role(message.author, role)

        # Ta bort roll om inaktiv i över 14 timmar
        for user_id, last_active_str in list(active_users.items()):
            last_active = datetime.fromisoformat(last_active_str)
            member = guild.get_member(int(user_id))
            if member and (current_time - last_active) > timedelta(hours=14):
                logger.debug(f"Användare {member.name} har varit inaktiv i över 14 timmar. Tar bort LateNightCrew-roll.")
                await remove_role(member, role)
                del active_users[user_id]

        # Spara uppdaterade användare
        save_active_users(active_users)

        # Debug: Rensa filen efter 05:00
        if not is_late_night():
            logger.debug("Efter Late Night period, rensar active_users.json.")
            with open(ACTIVE_USERS_FILE, 'w') as file:
                json.dump({}, file)

    except Exception as e:
        logger.error(f"Fel vid spårning av aktivitet: {str(e)}")
