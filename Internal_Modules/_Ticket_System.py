# Internal_Modules/_Ticket_System.py

import discord
from discord import app_commands
from discord.ext import tasks
import aiohttp
import logging
import os
import json
from datetime import datetime
import _Bot_Config  # type: ignore

logger = logging.getLogger(__name__)

# Configuration refs
GUILD_ID = _Bot_Config._Guild_ID()
TICKET_CATEGORY_ID = _Bot_Config._Ticket_Category_ID()
ARCHIVE_CATEGORY_ID = _Bot_Config._Archive_Category_ID()
COUNTER_FILE = _Bot_Config._Ticket_Counter_File()
GITHUB_API_URL = _Bot_Config._GitHub_API_URL()  # e.g. "https://api.github.com/repos/owner/repo/issues"
GITHUB_TOKEN = _Bot_Config._GitHub_Token()
MENTOR_ROLE = _Bot_Config._Mentor_Role_Name()

# Utility for ticket numbering
def load_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            try:
                return json.load(f).get('counter', 0)
            except json.JSONDecodeError:
                return 0
    return 0

def save_counter(count):
    with open(COUNTER_FILE, 'w') as f:
        json.dump({'counter': count}, f)

def get_next_ticket_number():
    c = load_counter() + 1
    save_counter(c)
    return f"{c:04d}"

# GitHub integration
async def create_github_issue(title: str, body: str, labels=None):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    payload = {'title': title, 'body': body, 'labels': labels or []}
    async with aiohttp.ClientSession() as session:
        async with session.post(GITHUB_API_URL, json=payload, headers=headers) as resp:
            if resp.status == 201:
                return await resp.json()
            text = await resp.text()
            logger.error(f"GitHub issue creation failed {resp.status}: {text}")
            return None

# Slash command group for tickets
ticket_group = app_commands.Group(name='ticket', description='Support ticket commands')

@ticket_group.command(name='create', description='Create a new support ticket')
@app_commands.describe(subject='Short description of your issue')
async def create_ticket(interaction: discord.Interaction, subject: str):
    guild = interaction.guild
    category = guild.get_channel(TICKET_CATEGORY_ID)
    if category is None:
        await interaction.response.send_message("Ticket category not found.", ephemeral=True)
        return

    num = get_next_ticket_number()
    channel = await guild.create_text_channel(f"ticket-{num}", category=category)
    await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
    await channel.send(f"{interaction.user.mention} opened ticket **#{num}**: **{subject}**")
    mentor = discord.utils.get(guild.roles, name=MENTOR_ROLE)
    if mentor:
        await channel.send(f"{mentor.mention}, please assist.")

    # Create GitHub issue
    issue = await create_github_issue(f"Ticket #{num}: {subject}",
                                      f"Opened by {interaction.user} in Discord. Channel: {channel.mention}")
    if issue and issue.get('html_url'):
        await channel.send(f"GitHub issue created: {issue['html_url']}")

    await interaction.response.send_message(f"Ticket channel {channel.mention} created.", ephemeral=True)

@ticket_group.command(name='close', description='Close and archive the current ticket')
async def close_ticket(interaction: discord.Interaction):
    channel = interaction.channel
    if not channel.name.startswith('ticket-'):
        await interaction.response.send_message("This command can only be used in a ticket channel.", ephemeral=True)
        return

    archive_cat = interaction.guild.get_channel(ARCHIVE_CATEGORY_ID)
    if archive_cat:
        await channel.edit(category=archive_cat)
    await channel.send("This ticket has been closed and archived.")
    await interaction.response.send_message("Ticket closed.", ephemeral=True)

# Optional background task for cleanup (e.g., auto-archive after inactivity)
@tasks.loop(hours=24)
async def cleanup_inactive_tickets(bot: discord.Bot):
    guild = bot.get_guild(GUILD_ID)
    category = guild.get_channel(TICKET_CATEGORY_ID)
    archive_cat = guild.get_channel(ARCHIVE_CATEGORY_ID)
    cutoff = datetime.utcnow() - timedelta(days=2)
    for ch in category.channels:
        last = (await ch.history(limit=1).flatten())[0].created_at if ch.history else ch.created_at
        if last < cutoff and archive_cat:
            await ch.edit(category=archive_cat)
            logger.info(f"Archived inactive ticket {ch.name}")

# Setup function to register commands and start tasks
def setup_ticketer(bot):
    bot.tree.add_command(ticket_group)
    @bot.event
    async def on_ready():
        if not cleanup_inactive_tickets.is_running():
            cleanup_inactive_tickets.start(bot)
            logger.info("Started cleanup_inactive_tickets task.")
    logger.info("Ticket_System setup completed.")