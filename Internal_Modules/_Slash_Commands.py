# Internal_Modules/_Slash_Commands.py

import discord
from discord import app_commands
from discord.ext import commands
import subprocess
import importlib
from datetime import datetime
import asyncio

# --- Imports for command logic ---
import _XP_Handler
import _Role_Management
import _Bot_Config
import _Gemini_Handler  # Correctly imported for the new command
# The modules below are only needed for the 'reload' command map
import _Cisco_Study_Plans
import _Member_Moderation
import _Game
import _Auction
import _Ticket_System
import _Bot_Modul

class CommandGroup(app_commands.Group):
    pass

def setup(bot: commands.Bot):
    """This function is called by main.py to register all commands."""

    # --- Ping Command ---
    @bot.tree.command(name="ping", description="Performs a ping test to a specified IP address.")
    @app_commands.describe(ip="The IP address to ping (defaults to 8.8.8.8).")
    async def ping(interaction: discord.Interaction, ip: str = '8.8.8.8'):
        await interaction.response.defer(thinking=True)
        try:
            process = await asyncio.create_subprocess_shell(
                f"ping -c 4 {ip}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            response = stdout.decode() if process.returncode == 0 else stderr.decode()
            await interaction.followup.send(f"```\n{response}\n```")
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}")

    # --- Version Command ---
    @bot.tree.command(name="version", description="Shows the current bot version.")
    async def version(interaction: discord.Interaction):
        version_nr = getattr(_Bot_Config, 'VERSION_NR', "Not specified")
        await interaction.response.send_message(f"Current version: {version_nr}", ephemeral=True)

    # --- Level Command ---
    @bot.tree.command(name="level", description="Shows your or another member's level and XP.")
    @app_commands.describe(member="The member to check the level of.")
    async def level(interaction: discord.Interaction, member: discord.Member = None):
        target_member = member or interaction.user
        user_id = str(target_member.id)
        user_data = _XP_Handler.xp_data.get(user_id)

        if not user_data:
            await interaction.response.send_message(f"{target_member.display_name} hasn't earned any XP yet.", ephemeral=True)
            return

        current_level = user_data.get('level', 1)
        current_xp = user_data.get('xp', 0)
        xp_needed = _XP_Handler.xp_needed_for_level(current_level)

        embed = discord.Embed(title=f"Level Status for {target_member.display_name}", color=target_member.color)
        embed.set_thumbnail(url=target_member.display_avatar.url)
        embed.add_field(name="Level", value=f"**{current_level}**", inline=True)
        embed.add_field(name="XP", value=f"`{current_xp} / {xp_needed}`", inline=True)
        
        progress = int((current_xp / xp_needed) * 20)
        progress_bar = '🟩' * progress + '⬛' * (20 - progress)
        embed.add_field(name="Progress", value=progress_bar, inline=False)
        
        await interaction.response.send_message(embed=embed)

    # --- Role Command ---
    @bot.tree.command(name="role", description="Assign or remove roles using buttons.")
    async def role(interaction: discord.Interaction):
        # Assuming create_role_buttons_view returns a View object
        view = _Role_Management.create_role_buttons_view()
        await interaction.response.send_message("Select a role to assign or remove:", view=view, ephemeral=True)

    # --- Gemini Command ---
    @bot.tree.command(name="ask", description="Ask a question to the Gemini AI.")
    @app_commands.describe(question="The question you want to ask.")
    async def ask(interaction: discord.Interaction, question: str):
        await interaction.response.defer(thinking=True)
        answer = await _Gemini_Handler.ask_gemini(question)
        
        embed = discord.Embed(title="❓ Your Question", description=question, color=discord.Color.from_rgb(100, 100, 255))
        embed.add_field(name="💡 Gemini's Answer", value=answer, inline=False)
        embed.set_footer(text=f"Asked by {interaction.user.display_name}")
        
        await interaction.followup.send(embed=embed)

    # --- Admin Command Group ---
    admin_group = CommandGroup(name="admin", description="Admin-only commands.")

    @admin_group.command(name="reload", description="Reloads a specified internal module.")
    @app_commands.describe(module="The module to reload.")
    @app_commands.choices(module=[
        app_commands.Choice(name=name, value=value) for name, value in [
            ("Role Management", "Role_Management"), ("XP Handler", "XP_Handler"),
            ("Auction", "Auction"), ("Game", "Game"), ("Moderation", "Moderation"),
            ("Ticket System", "Ticket_System"), ("Cisco Study Plans", "Cisco_Study_Plans"),
            ("Bot Module", "Bot_Modul"), ("Gemini Handler", "Gemini_Handler")
        ]
    ])
    async def reload_module(interaction: discord.Interaction, module: app_commands.Choice[str]):
        bot_admin_role_name = _Bot_Config._Bot_Admin_Role_Name()
        if not discord.utils.get(interaction.user.roles, name=bot_admin_role_name):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        modules_map = {
            'Role_Management': _Role_Management, 'XP_Handler': _XP_Handler, 'Auction': _Auction,
            'Game': _Game, 'Moderation': _Member_Moderation, 'Ticket_System': _Ticket_System,
            'Cisco_Study_Plans': _Cisco_Study_Plans, 'Bot_Modul': _Bot_Modul, 'Gemini_Handler': _Gemini_Handler
        }
        mod_to_reload = modules_map.get(module.value)

        try:
            importlib.reload(mod_to_reload)
            await interaction.response.send_message(f"✅ Module `{module.name}` reloaded successfully.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"🔥 Failed to reload module `{module.name}`. Error: {e}", ephemeral=True)

    # Add the admin command group to the bot's command tree
    bot.tree.add_command(admin_group)

  