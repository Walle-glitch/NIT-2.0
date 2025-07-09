# Internal_Modules/_Slash_Commands.py

# --- Imports ---
# 1. Standard Library
import asyncio
import importlib
import subprocess
from datetime import datetime

# 2. Third-party Libraries
import discord
from discord import app_commands
from discord.ext import commands

# 3. Local Application Modules
from _logging_setup import setup_logging
import _XP_Handler
import _Role_Management
import _Bot_Config
import _Gemini_Handler
import _Cisco_Study_Plans
import _Member_Moderation
import _Game
import _Auction
import _Ticket_System
import _Bot_Modul

# --- Initial Setup ---
logger = setup_logging()

class AdminCommandGroup(app_commands.Group):
    """A dedicated group for admin commands for better organization."""
    pass

def setup(bot: commands.Bot):
    """
    This function is called by main.py to register all slash commands.
    """

    # --- Helper function for splitting long text ---
    def split_into_chunks(text: str, chunk_size: int):
        """Splits a string into chunks of a specified size."""
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    # --- General User Commands ---

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

    @bot.tree.command(name="version", description="Shows the current bot version.")
    async def version(interaction: discord.Interaction):
        version_nr = getattr(_Bot_Config, 'VERSION_NR', "Not specified")
        await interaction.response.send_message(f"Current version: {version_nr}", ephemeral=True)

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

    @bot.tree.command(name="role", description="Assign or remove roles using buttons.")
    async def role(interaction: discord.Interaction):
        view = _Role_Management.create_role_buttons_view()
        if view:
            await interaction.response.send_message("Select a role to assign or remove:", view=view, ephemeral=True)
        else:
            await interaction.response.send_message("Role assignment is not available at the moment.", ephemeral=True)

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
    admin_group = AdminCommandGroup(name="admin", description="Admin-only commands.")

    # Define the modules that can be reloaded
    reloadable_modules = {
        'Role Management': _Role_Management, 'XP Handler': _XP_Handler, 'Auction': _Auction,
        'Game': _Game, 'Moderation': _Member_Moderation, 'Ticket System': _Ticket_System,
        'Cisco Study Plans': _Cisco_Study_Plans, 'Bot Module': _Bot_Modul, 'Gemini Handler': _Gemini_Handler
    }

    @admin_group.command(name="reload", description="Reloads a specified internal module.")
    @app_commands.describe(module="The module to reload.")
    @app_commands.choices(module=[
        app_commands.Choice(name=name, value=name) for name in reloadable_modules.keys()
    ])
    async def reload_module(interaction: discord.Interaction, module: app_commands.Choice[str]):
        bot_admin_role_name = _Bot_Config._Bot_Admin_Role_Name()
        if not discord.utils.get(interaction.user.roles, name=bot_admin_role_name):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        mod_to_reload = reloadable_modules.get(module.value)
        try:
            importlib.reload(mod_to_reload)
            await interaction.response.send_message(f"✅ Module `{module.name}` reloaded successfully.", ephemeral=True)
            logger.info(f"Module '{module.name}' reloaded by {interaction.user.name}.")
        except Exception as e:
            await interaction.response.send_message(f"🔥 Failed to reload module `{module.name}`. Error: {e}", ephemeral=True)
            logger.error(f"Failed to reload module {module.name}: {e}", exc_info=True)

    @admin_group.command(name="populate_xp", description="[DANGER] Scans server history to populate XP.")
    async def populate_xp(interaction: discord.Interaction):
        """Scans all channels and messages to build the XP database from scratch."""
        bot_admin_role_name = _Bot_Config._Bot_Admin_Role_Name()
        if not discord.utils.get(interaction.user.roles, name=bot_admin_role_name):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True, ephemeral=True)
        await interaction.followup.send("✅ **Starting XP Population.**\nThis is a one-time operation and will take a very long time. Please do not run this command again.", ephemeral=True)
        
        logger.info(f"XP Population started by {interaction.user.name}.")
        
        message_counts = {}
        total_messages_scanned = 0
        guild = interaction.guild
        
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).read_message_history:
                logger.info(f"Scanning channel: #{channel.name}")
                try:
                    async for message in channel.history(limit=None):
                        if not message.author.bot:
                            author_id = message.author.id
                            if author_id not in message_counts:
                                message_counts[author_id] = {'count': 0, 'name': message.author.name}
                            message_counts[author_id]['count'] += 1
                        total_messages_scanned += 1
                except discord.Forbidden:
                    logger.warning(f"Skipping channel #{channel.name} due to missing permissions.")
                except Exception as e:
                    logger.error(f"An error occurred while scanning #{channel.name}: {e}")

        logger.info(f"Finished scanning. Found {total_messages_scanned} messages from {len(message_counts)} unique users.")
        
        xp_per_message = 7
        for user_id, data in message_counts.items():
            total_xp_to_add = data['count'] * xp_per_message
            _XP_Handler.add_xp_for_history(user_id, data['name'], total_xp_to_add)
            
        _XP_Handler.save_xp_data(_XP_Handler.xp_data)
        logger.info("XP data has been saved to file.")

        await interaction.followup.send(f"✅ **XP Population Complete!**\n- Scanned `{total_messages_scanned}` messages.\n- Updated XP for `{len(message_counts)}` unique users.", ephemeral=True)

    # Add the admin command group to the bot's command tree
    bot.tree.add_command(admin_group)