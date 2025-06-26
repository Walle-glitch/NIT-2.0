# Internal_Modules/_Slash_Commands.py

import os
import json
import logging
import discord
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger(__name__)

# Path to help commands JSON
HELP_FILE = os.path.join(os.getcwd(), 'Json_Files', 'Help_Commands.json')

# Utility function to load help data
def load_help_commands():
    if os.path.exists(HELP_FILE):
        try:
            with open(HELP_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load help commands: {e}")
    return None

# Setup function to register slash commands
def setup(bot: commands.Bot):
    """
    Register slash commands: help and RFC retrieval.
    """
    # /help command
    @bot.tree.command(name="help", description="Get information on available commands")
    async def help_command(interaction: discord.Interaction):
        help_data = load_help_commands()
        if not help_data:
            await interaction.response.send_message("Help data not found.", ephemeral=True)
            return

        version = help_data.get('version', 'Unknown')
        commands_list = help_data.get('commands', {})

        embed = discord.Embed(
            title="Available Commands",
            description=f"**Version:** {version}",
            color=discord.Color.blue()
        )
        for cmd, desc in commands_list.items():
            embed.add_field(name=cmd, value=desc, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    # /rfc command
    @bot.tree.command(name="rfc", description="Retrieve information about an RFC by number")
    @app_commands.describe(number="RFC number to fetch")
    async def rfc_command(interaction: discord.Interaction, number: int):
        try:
            import _Bot_Modul as bot_modul  # type: ignore
            result = bot_modul.get_rfc(number)
        except Exception as e:
            result = f"Error fetching RFC: {e}"
        await interaction.response.send_message(result)

    logger.info("Slash_Commands setup completed.")