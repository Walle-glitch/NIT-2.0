# Internal_Modules/_Slash_Commands.py

import discord
from discord import app_commands
from discord.ext import commands # Make sure commands is imported
import subprocess
import importlib
from datetime import datetime
import asyncio # Make sure asyncio is imported

# --- CORRECTED IMPORTS ---
# Changed from relative (from . import X) to absolute (import X)
import _XP_Handler
import _Role_Management
import _Cisco_Study_Plans
import _Bot_Config
import _Member_Moderation
import _Game
import _Auction
import _Ticket_System

# --- Central Command Setup ---
# This class will hold all slash commands, making them easy to register.
class CommandGroup(app_commands.Group):
    pass

def setup(bot: commands.Bot):
    """This function is called by main.py to register all commands."""

    # --- Ping Command ---
    @bot.tree.command(name="ping", description="Performs a ping test to a specified IP address (default: 8.8.8.8).")
    @app_commands.describe(ip="The IP address to ping.")
    async def ping(interaction: discord.Interaction, ip: str = '8.8.8.8'):
        await interaction.response.defer(thinking=True)
        try:
            # Using asyncio.create_subprocess_shell is better for async bots
            process = await asyncio.create_subprocess_shell(
                f"ping -c 4 {ip}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                response = stdout.decode()
            else:
                response = stderr.decode()

            await interaction.followup.send(f"```\n{response}\n```")
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}")

    # --- Version Command ---
    @bot.tree.command(name="version", description="Shows the current bot version.")
    async def version(interaction: discord.Interaction):
        version_nr = _Bot_Config.VERSION_NR if hasattr(_Bot_Config, 'VERSION_NR') else "Not specified"
        await interaction.response.send_message(f"Current version: {version_nr}", ephemeral=True)

    # --- Level Command ---
    @bot.tree.command(name="level", description="Shows your or another member's level and XP.")
    @app_commands.describe(member="The member to check the level of. Defaults to you.")
    async def level(interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        user_id = str(member.id)
        user_data = _XP_Handler.xp_data.get(user_id)

        if not user_data:
            await interaction.response.send_message(f"{member.display_name} hasn't earned any XP yet.", ephemeral=True)
            return

        current_level = user_data.get('level', 1)
        current_xp = user_data.get('xp', 0)
        xp_needed = _XP_Handler.xp_needed_for_level(current_level)

        embed = discord.Embed(
            title=f"Level Status for {member.display_name}",
            color=member.color
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Level", value=f"**{current_level}**", inline=True)
        embed.add_field(name="XP", value=f"`{current_xp} / {xp_needed}`", inline=True)

        progress = int((current_xp / xp_needed) * 20)
        progress_bar = '🟩' * progress + '⬛' * (20 - progress)
        embed.add_field(name="Progress", value=progress_bar, inline=False)

        await interaction.response.send_message(embed=embed)

    # --- Role Command ---
    @bot.tree.command(name="role", description="Assign or remove roles using buttons.")
    async def role(interaction: discord.Interaction):
        view = _Role_Management.create_role_buttons_view()
        await interaction.response.send_message("Select a role to assign or remove:", view=view, ephemeral=True)

    # --- Admin Commands ---
    admin_group = CommandGroup(name="admin", description="Admin-only commands.")

    @admin_group.command(name="reload", description="Reloads a specified internal module.")
    @app_commands.describe(module="The module to reload.")
    @app_commands.choices(module=[
        app_commands.Choice(name="Role Management", value="Role_Management"),
        app_commands.Choice(name="XP Handler", value="XP_Handler"),
        app_commands.Choice(name="Auction", value="Auction"),
        app_commands.Choice(name="Game", value="Game"),
        app_commands.Choice(name="Moderation", value="Moderation"),
        app_commands.Choice(name="Ticket System", value="Ticket_System"),
        app_commands.Choice(name="Cisco Study Plans", value="Cisco_Study_Plans"),
        app_commands.Choice(name="Bot Module (Jobs)", value="Bot_Modul"),
    ])
    async def reload_module(interaction: discord.Interaction, module: app_commands.Choice[str]):
        bot_admin_role_name = _Bot_Config._Bot_Admin_Role_Name()
        if not discord.utils.get(interaction.user.roles, name=bot_admin_role_name):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        modules_map = {
            'Role_Management': _Role_Management,
            'XP_Handler': _XP_Handler,
            'Auction': _Auction,
            'Game': _Game,
            'Moderation': _Member_Moderation,
            'Ticket_System': _Ticket_System,
            'Cisco_Study_Plans': _Cisco_Study_Plans,
            'Bot_Modul': _Bot_Modul
        }
        mod_to_reload = modules_map.get(module.value)

        try:
            importlib.reload(mod_to_reload)
            await interaction.response.send_message(f"✅ Module `{module.name}` reloaded successfully.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"🔥 Failed to reload module `{module.name}`. Error: {e}", ephemeral=True)

    # Add the admin command group to the bot's command tree
    bot.tree.add_command(admin_group)

    # Register other slash command modules you have
    _Game.setup(bot)
    _Auction.setup(bot)
    _Ticket_System.setup(bot)
    _Member_Moderation.setup(bot)