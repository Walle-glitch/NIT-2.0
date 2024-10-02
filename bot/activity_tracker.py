import os
import json
from datetime import datetime, timedelta
import logging
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'Internal_Modules'))

import _Bot_Config

# Definiera filvägar och konstanter
ACTIVE_USERS_FILE = "/home/bot/NIT-2.0/bot/Json_Files/active_users.json"
GUILD_ID = _Bot_Config._GUILD_ID()
LATE_NIGHT_ROLE_ID = _Bot_Config._LATE_NIGHT_ROLE_ID()

# Setup logging (importera från logging_setup)
logger = logging.getLogger(__name__)

# Kolla om filen existerar, annars skapa en ny fil
def setup_file():
    if not os.path.exists("/home/bot/NIT-2.0/bot/Json_Files"):
        os.makedirs("/home/bot/NIT-2.0/bot/Json_Files")

    if not os.path.isfile(ACTIVE_USERS_FILE):
        with open(ACTIVE_USERS_FILE, 'w') as file:
            json.dump({}, file)

def is_late_night():
    """Kolla om det är mellan 00:01 och 05:00"""
    current_time = datetime.now().time()
    return current_time >= datetime.strptime("00:01", "%H:%M").time() and current_time <= datetime.strptime("05:00", "%H:%M").time()

def load_active_users():
    """Ladda aktiva användare från JSON-filen"""
    with open(ACTIVE_USERS_FILE, 'r') as file:
        return json.load(file)

def save_active_users(active_users):
    """Spara aktiva användare till JSON-filen"""
    with open(ACTIVE_USERS_FILE, 'w') as file:
        json.dump(active_users, file)

async def add_role(member, role):
    """Lägg till LateNightCrew rollen till medlemmen"""
    if role not in member.roles:
        await member.add_roles(role)
        logger.info(f"Lagt till LateNightCrew-roll för {member.name}")

async def remove_role(member, role):
    """Ta bort LateNightCrew rollen från medlemmen"""
    if role in member.roles:
        await member.remove_roles(role)
        logger.info(f"Tagit bort LateNightCrew-roll från {member.name}")

async def track_activity(message, bot):
    """Spåra användaraktivitet och hantera roller"""
    if message.author.bot:
        return

    # Ladda guild och rollen
    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(LATE_NIGHT_ROLE_ID)

    # Ladda aktiva användare
    active_users = load_active_users()
    current_time = datetime.now()

    # Uppdatera aktivitet
    active_users[message.author.id] = current_time.isoformat()
    save_active_users(active_users)

    # Hantera Late Night Crew-roll
    if is_late_night():
        await add_role(message.author, role)

    # Ta bort roll om användare varit inaktiva i mer än 14 timmar
    for user_id, last_active_str in list(active_users.items()):
        last_active = datetime.fromisoformat(last_active_str)
        member = guild.get_member(int(user_id))

        if member and (current_time - last_active) > timedelta(hours=14):
            await remove_role(member, role)
            del active_users[user_id]

    # Uppdatera JSON-filen
    save_active_users(active_users)

    # Rensa filen om klockan är efter 05:00
    if not is_late_night():
        with open(ACTIVE_USERS_FILE, 'w') as file:
            json.dump({}, file)

