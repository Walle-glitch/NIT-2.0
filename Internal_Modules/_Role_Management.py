# Internal_Modules/_Role_Management.py

import os
import json
import discord
import asyncio
from discord.ui import Button, View
import logging
import _Bot_Config  # type: ignore

# Initialize logger
logger = logging.getLogger(__name__)

# Configuration refs
ROLE_JSON_FILE = _Bot_Config._Role_Json_File()
EXCLUDED_ROLES = _Bot_Config._Excluded_Roles()
STATIC_ROLES = _Bot_Config._Static_Roles()
PASSWORD_PROTECTED_ROLES = _Bot_Config._protected_Poles()

# Setup function to initialize JSON file and directories
def setup(role_json_file: str):
    """Ensure the roles JSON file and its directory exist."""
    directory = os.path.dirname(role_json_file)
    try:
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created roles directory: {directory}")
        if not os.path.isfile(role_json_file):
            with open(role_json_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            logger.info(f"Initialized roles file: {role_json_file}")
    except Exception as e:
        logger.error(f"Error setting up roles file: {e}")

# Button class for static roles
class RoleButton(Button):
    def __init__(self, label, style, role_id=None):
        super().__init__(label=label, style=style)
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(int(self.role_id)) if self.role_id else discord.utils.get(interaction.guild.roles, name=self.label)
        if not role:
            await interaction.response.send_message(f"Role '{self.label}' not found.", ephemeral=True)
            return
        if role in interaction.user.roles:
            await interaction.response.send_message(f"You already have the role {role.name}.", ephemeral=True)
        else:
            try:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"Role {role.name} assigned.", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("Insufficient permissions to assign role.", ephemeral=True)

# Create view for buttons
def create_role_buttons_view():
    view = View(timeout=None)
    for label, role_id in STATIC_ROLES.items():
        if label in EXCLUDED_ROLES:
            continue
        style = discord.ButtonStyle.green
        view.add_item(RoleButton(label=label, style=style, role_id=role_id))
    return view

# Load roles mapping from JSON
def load_roles():
    try:
        with open(ROLE_JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load roles: {e}")
        return {}

# Fetch and save roles from discord server
async def fetch_and_save_roles(bot):
    roles = {}
    for guild in bot.guilds:
        for role in guild.roles:
            if role.name not in EXCLUDED_ROLES:
                roles[role.name] = role.id
    try:
        with open(ROLE_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(roles, f, indent=4)
        logger.info("Roles saved to JSON file.")
    except Exception as e:
        logger.error(f"Failed to save roles: {e}")

# Assign a role by command
async def assign_role(ctx, role_name: str):
    roles = load_roles()
    if role_name not in roles:
        await ctx.send(f"Role '{role_name}' not found.")
        return
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"Role '{role_name}' not present on server.")
        return
    # Password-protection if needed
    if role_name in PASSWORD_PROTECTED_ROLES:
        await ctx.author.send(f"Role '{role_name}' requires a password. Reply with password.")
        try:
            msg = await ctx.bot.wait_for('message', check=lambda m: m.author == ctx.author and isinstance(m.channel, discord.DMChannel), timeout=60)
            if msg.content != PASSWORD_PROTECTED_ROLES[role_name]:
                await ctx.author.send("Incorrect password. Operation cancelled.")
                return
        except asyncio.TimeoutError:
            await ctx.author.send("No response. Operation cancelled.")
            return
    # Assign or notify
    try:
        if role in ctx.author.roles:
            await ctx.send(f"You already have the role {role_name}.")
        else:
            await ctx.author.add_roles(role)
            await ctx.send(f"Role {role_name} assigned.")
    except discord.Forbidden:
        await ctx.send("Insufficient permissions to assign role.")

# Remove a role by command
async def remove_role(ctx, role_name: str):
    roles = load_roles()
    if role_name not in roles:
        await ctx.send(f"Role '{role_name}' not found.")
        return
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"Role '{role_name}' not present on server.")
        return
    try:
        if role not in ctx.author.roles:
            await ctx.send(f"You do not have the role {role_name}.")
        else:
            await ctx.author.remove_roles(role)
            await ctx.send(f"Role {role_name} removed.")
    except discord.Forbidden:
        await ctx.send("Insufficient permissions to remove role.")
