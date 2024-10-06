import json
import discord
import asyncio
import _Bot_Config  # type: ignore
from discord.ui import Button, View

# Load role configuration from _Bot_Config
BOT_ADMIN_ROLE_NAME = _Bot_Config._Bot_Admin_Role_Name()
ADMIN_ROLE_NAME = _Bot_Config._Admin_Role_Name()
MOD_ROLE_NAME = _Bot_Config._Mod_Role_Name()
MENTOR_ROLE = _Bot_Config._Mentor_Role_Name()

STATIC_ROLES = _Bot_Config._Static_Roles()  # Static role names and their IDs
PASSWORD_PROTECTED_ROLES = _Bot_Config._protected_Poles()  # Roles that require password
ROLE_JSON_FILE = _Bot_Config._Role_Json_File()  # File where roles are stored
EXCLUDED_ROLES = _Bot_Config._Excluded_Roles()  # Roles excluded from being assigned

# Define the Role   class
class RoleButton(Button):
    def __init__(self, label, style, role_id=None):
        super().__init__(label=label, style=style)
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(int(self.role_id)) if self.role_id else discord.utils.get(interaction.guild.roles, name=self.label)
        
        if role:
            if role in interaction.user.roles:
                await interaction.response.send_message(f"You already have the role {role.name}.", ephemeral=True)
            else:
                try:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"The role {role.name} has been assigned to you.", ephemeral=True)
                except discord.Forbidden:
                    await interaction.response.send_message("I do not have permission to assign roles.", ephemeral=True)
        else:
            await interaction.response.send_message(f"The role for {self.label} could not be found on the server.", ephemeral=True)

# Create the view with buttons for role assignment
def create_role_buttons_view():
    view = View(timeout=None)  # View will not expire unless manually stopped

    ROLE_BUTTONS = [
        {"label": "NIT_24", "style": discord.ButtonStyle.blurple, "role_id": STATIC_ROLES.get("NIT_24")},
        {"label": "NIT_23", "style": discord.ButtonStyle.blurple, "role_id": STATIC_ROLES.get("NIT_23")},
        {"label": "NIT_22", "style": discord.ButtonStyle.blurple, "role_id": STATIC_ROLES.get("NIT_22")},
        {"label": "Another Start Year", "style": discord.ButtonStyle.gray, "role_id": STATIC_ROLES.get("Another Start Year")},
        {"label": "3rd Year!", "style": discord.ButtonStyle.green, "role_id": STATIC_ROLES.get("3rd Year!")},
        {"label": "Union Member", "style": discord.ButtonStyle.red, "role_id": STATIC_ROLES.get("Union Member")},
    ]
    
    for button_info in ROLE_BUTTONS:
        button = RoleButton(label=button_info['label'], style=button_info['style'], role_id=button_info['role_id'])
        view.add_item(button)
    
    return view

# Load roles from the JSON file
def load_roles():
    try:
        with open(ROLE_JSON_FILE, 'r') as file:
            roles = json.load(file)
        return roles
    except Exception as e:
        print(f"Failed to load roles: {str(e)}")
        return {}

# Fetch and save roles to the JSON file
async def fetch_and_save_roles(bot):
    roles = {}
    for guild in bot.guilds:
        for role in guild.roles:
            if role.name not in EXCLUDED_ROLES:
                roles[role.name] = role.id

    with open(ROLE_JSON_FILE, 'w') as file:
        json.dump(roles, file, indent=4)

# Assign a role to the user
async def assign_role(ctx, role_name: str):
    roles = load_roles()
    
    if role_name not in roles:
        await ctx.send(f"Role '{role_name}' could not be found.")
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        await ctx.send(f"Role '{role_name}' could not be found on this server.")
        return

    if role_name in PASSWORD_PROTECTED_ROLES:
        await ctx.author.send(f"The role '{role_name}' requires a password. Please respond with the password within 60 seconds:")

        try:
            msg = await ctx.bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and isinstance(m.channel, discord.DMChannel))

            if msg.content != PASSWORD_PROTECTED_ROLES[role_name]:
                await ctx.author.send("Incorrect password. Role assignment canceled.")
                return

        except asyncio.TimeoutError:
            await ctx.author.send("You took too long to respond. Role assignment canceled.")
            return

    if role in ctx.author.roles:
        embed = discord.Embed(title="Role Already Assigned", description=f"You already have the role **{role_name}**.", color=discord.Color.orange())
    else:
        try:
            await ctx.author.add_roles(role)
            embed = discord.Embed(title="Role Assigned", description=f"The role **{role_name}** has been assigned to you!", color=discord.Color.green())
        except discord.Forbidden:
            embed = discord.Embed(title="Error", description="I do not have sufficient permissions to assign this role.", color=discord.Color.red())

    await ctx.send(embed=embed)

# Remove a role from the user
async def remove_role(ctx, role_name: str):
    roles = load_roles()

    if role_name not in roles:
        await ctx.send(f"Role '{role_name}' could not be found.")
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        await ctx.send(f"Role '{role_name}' could not be found on this server.")
        return

    if role not in ctx.author.roles:
        embed = discord.Embed(title="Role Not Found", description=f"You do not have the role **{role_name}**.", color=discord.Color.orange())
    else:
        try:
            await ctx.author.remove_roles(role)
            embed = discord.Embed(title="Role Removed", description=f"The role **{role_name}** has been removed from you.", color=discord.Color.green())
        except discord.Forbidden:
            embed = discord.Embed(title="Error", description="I do not have sufficient permissions to remove this role.", color=discord.Color.red())

    await ctx.send(embed=embed)
