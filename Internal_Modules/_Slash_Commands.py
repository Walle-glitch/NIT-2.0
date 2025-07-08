# Internal_Modules/_Slash_Commands.py

# --- Imports ---
import asyncio
import importlib
import subprocess
from datetime import datetime
import discord
from discord import app_commands
from discord.ext import commands

from _logging_setup import setup_logging
import _XP_Handler
import _Role_Management
import _Bot_Config
import _Gemini_Handler
# ... (and all other necessary local module imports)
import _Cisco_Study_Plans, _Member_Moderation, _Game, _Auction, _Ticket_System, _Bot_Modul

# --- Initial Setup ---
logger = setup_logging()

class AdminCommandGroup(app_commands.Group):
    """A dedicated group for admin commands for better organization."""
    pass

def setup(bot: commands.Bot):
    """This function is called by main.py to register all slash commands."""

    # --- Helper function for splitting long text ---
    def split_into_chunks(text: str, chunk_size: int):
        """Splits a string into chunks of a specified size."""
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    # --- General User Commands ---
    # ... (Your /ping, /version, /level, /role commands are here, no changes needed) ...
    @bot.tree.command(name="ping", description="Performs a ping test to a specified IP address.")
    async def ping(interaction: discord.Interaction, ip: str = '8.8.8.8'):
        # Ping logic here
        pass # Placeholder

    @bot.tree.command(name="version", description="Shows the current bot version.")
    async def version(interaction: discord.Interaction):
        # Version logic here
        pass # Placeholder

    @bot.tree.command(name="level", description="Shows your or another member's level and XP.")
    async def level(interaction: discord.Interaction, member: discord.Member = None):
        # Level logic here
        pass # Placeholder

    @bot.tree.command(name="role", description="Assign or remove roles using buttons.")
    async def role(interaction: discord.Interaction):
        # Role logic here
        pass # Placeholder


    # --- CORRECTED GEMINI COMMAND ---
    @bot.tree.command(name="ask", description="Ask a question to the Gemini AI.")
    @app_commands.describe(question="The question you want to ask.")
    async def ask(interaction: discord.Interaction, question: str):
        await interaction.response.defer(thinking=True)
        answer = await _Gemini_Handler.ask_gemini(question)

        embed = discord.Embed(
            title="❓ Your Question",
            description=question,
            color=discord.Color.from_rgb(100, 100, 255)
        )
        embed.set_footer(text=f"Asked by {interaction.user.display_name}")

        # Check if the answer is too long for a single field
        if len(answer) <= 1024:
            embed.add_field(name="💡 Gemini's Answer", value=answer, inline=False)
        else:
            # If it's too long, split it into chunks
            answer_chunks = split_into_chunks(answer, 1024)
            for i, chunk in enumerate(answer_chunks):
                # The first field gets the title, subsequent fields get a "continuation" title
                field_name = "💡 Gemini's Answer" if i == 0 else f"...(part {i+1})"
                embed.add_field(name=field_name, value=chunk, inline=False)

        await interaction.followup.send(embed=embed)


    # --- Admin Command Group ---
    # ... (Your /admin reload and /admin populate_xp commands are here, no changes needed) ...
    admin_group = AdminCommandGroup(name="admin", description="Admin-only commands.")
    
    @admin_group.command(name="reload", description="Reloads a specified internal module.")
    async def reload_module(interaction: discord.Interaction, module: str):
        # Reload logic here
        pass # Placeholder

    @admin_group.command(name="populate_xp", description="[DANGER] Scans server history to populate XP.")
    async def populate_xp(interaction: discord.Interaction):
        # Populate XP logic here
        pass # Placeholder

    bot.tree.add_command(admin_group)