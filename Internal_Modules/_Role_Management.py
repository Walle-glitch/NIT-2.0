# Internal_Modules/_Role_Management.py
import discord
from discord.ext import commands
import json
import os
from . import _Bot_Config
from ._logging_setup import setup_logging

logger = setup_logging()
role_file_path = "" # Module-level variable

# --- CORRECTED SETUP FUNCTION ---
def setup():
    """Initializes the Role Management module."""
    global role_file_path
    role_file_path = _Bot_Config._Role_Json_File()
    if not os.path.exists(role_file_path):
        with open(role_file_path, 'w') as f:
            json.dump({}, f)
    logger.info("Role Management module setup complete.")

async def fetch_and_save_roles(bot: commands.Bot):
    """Fetches all roles from the main guild and saves them to a JSON file."""
    guild_id = _Bot_Config._Guild_ID()
    guild = bot.get_guild(guild_id)
    if not guild:
        logger.error(f"Could not find guild with ID {guild_id} to fetch roles.")
        return

    roles_data = {str(role.id): role.name for role in guild.roles}
    try:
        with open(role_file_path, 'w', encoding='utf-8') as f:
            json.dump(roles_data, f, indent=4)
        logger.info("Roles saved to JSON file.")
    except Exception as e:
        logger.error(f"Failed to save roles to JSON: {e}")

def create_role_buttons_view():
    """Creates a view with buttons for each manageable role."""
    # This function is now primarily used by the /role slash command
    # You might want to adapt it further based on your slash command needs
    pass # Leaving this to be implemented with slash commands logic

async def assign_role(ctx, role_name):
    # This logic is now handled by the /role slash command
    pass

async def remove_role(ctx, role_name):
    # This logic is now handled by the /role slash command
    pass