# Internal_Modules/_Role_Management.py
"""
Module for dynamic role assignment/removal in Discord via buttons or commands.
"""
import os
import json
import discord
import asyncio
from discord.ui import Button, View

import _Bot_Config  # type: ignore
from _logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

# Config values
BOT_ADMIN_ROLE_NAME = _Bot_Config._Bot_Admin_Role_Name()
ADMIN_ROLE_NAME = _Bot_Config._Admin_Role_Name()
MOD_ROLE_NAME = _Bot_Config._Mod_Role_Name()
MENTOR_ROLE_NAME = _Bot_Config._Mentor_Role_Name()

STATIC_ROLES = _Bot_Config._Static_Roles()  # name->id mapping
PASSWORD_PROTECTED_ROLES = _Bot_Config._Protected_Roles()  # name->password mapping
ROLE_JSON_FILE = _Bot_Config._Role_Json_File()
EXCLUDED_ROLES = _Bot_Config._Excluded_Roles()

# Helper to load/save role JSON

def load_roles() -> dict:
    """Load persisted roles from JSON file."""
    try:
        with open(ROLE_JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load roles: {e}")
        return {}


def save_roles(roles: dict):
    """Save roles mapping to JSON file."""
    try:
        os.makedirs(os.path.dirname(ROLE_JSON_FILE), exist_ok=True)
        with open(ROLE_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(roles, f, indent=4)
        logger.debug("Roles saved to JSON.")
    except Exception as e:
        logger.error(f"Failed to save roles: {e}")

# Button class for role assignment
class RoleButton(Button):
    def __init__(self, label: str, style: discord.ButtonStyle, role_id: int=None):
        super().__init__(label=label, style=style)
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        # Find role by ID or by name
        role = guild.get_role(self.role_id) if self.role_id else discord.utils.get(guild.roles, name=self.label)
        if not role:
            await interaction.response.send_message(f"Role {self.label} not found.", ephemeral=True)
            return
        if role in user.roles:
            await interaction.response.send_message(f"You already have the role {role.name}.", ephemeral=True)
        else:
            try:
                await user.add_roles(role)
                await interaction.response.send_message(f"Assigned role {role.name}.", ephemeral=True)
                logger.info(f"Assigned {role.name} to {user}")
            except discord.Forbidden:
                await interaction.response.send_message("Insufficient permissions.", ephemeral=True)
                logger.warning(f"Permission denied assigning {role.name} to {user}")

# Create a persistent view for buttons
def create_role_buttons_view() -> View:
    """Return a View containing buttons for static roles."""
    view = View(timeout=None)
    buttons = [
        (name, discord.ButtonStyle.blurple) for name in STATIC_ROLES.keys()
    ]
    for name, style in buttons:
        role_id = STATIC_ROLES.get(name)
        view.add_item(RoleButton(label=name, style=style, role_id=role_id))
    return view

# Assign a role via command
async def assign_role(ctx, role_name: str):
    """Assign specified role by name, handling password if protected."""
    roles = load_roles()
    if role_name not in roles:
        await ctx.send(f"Role '{role_name}' not found.")
        return
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"Role '{role_name}' not on this server.")
        return
    # Check password if protected
    if role_name in PASSWORD_PROTECTED_ROLES:
        password = PASSWORD_PROTECTED_ROLES[role_name]
        await ctx.author.send(f"Enter password for '{role_name}':")
        try:
            msg = await ctx.bot.wait_for(
                'message', check=lambda m: m.author==ctx.author and isinstance(m.channel, discord.DMChannel), timeout=60
            )
            if msg.content != password:
                await ctx.author.send("Incorrect password.")
                return
        except asyncio.TimeoutError:
            await ctx.author.send("Timed out.")
            return
    # Assign
    try:
        await ctx.author.add_roles(role)
        await ctx.send(embed=discord.Embed(
            title="Role Assigned", description=f"{role_name} added.", color=discord.Color.green()
        ))
        logger.info(f"{ctx.author} assigned {role_name}")
    except discord.Forbidden:
        await ctx.send("Cannot assign role.")
        logger.warning(f"Failed to assign {role_name} to {ctx.author}")

# Remove a role via command
async def remove_role(ctx, role_name: str):
    """Remove specified role from user."""
    roles = load_roles()
    if role_name not in roles:
        await ctx.send(f"Role '{role_name}' not found.")
        return
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"Role '{role_name}' not on this server.")
        return
    if role not in ctx.author.roles:
        await ctx.send(f"You do not have {role_name}.")
        return
    try:
        await ctx.author.remove_roles(role)
        await ctx.send(embed=discord.Embed(
            title="Role Removed", description=f"{role_name} removed.", color=discord.Color.red()
        ))
        logger.info(f"Removed {role_name} from {ctx.author}")
    except discord.Forbidden:
        await ctx.send("Cannot remove role.")
        logger.warning(f"Failed to remove {role_name} from {ctx.author}")