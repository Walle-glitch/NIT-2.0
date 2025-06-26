# Internal_Modules/_Ticket_System.py
"""
Ticketing and GitHub issue integration module for Discord bot.
Provides slash commands for creating/closing tickets and GitHub issues.
"""
import os
import json
import asyncio
from datetime import datetime, timedelta

import discord
from discord.ext import tasks
import aiohttp

import _Bot_Config  # type: ignore
from _logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN') or _Bot_Config._GitHub_Token()
GITHUB_API_URL = _Bot_Config._GitHub_API_URL()
TICKET_CATEGORY_ID = _Bot_Config._Ticket_Category_ID()
ARCHIVE_CATEGORY_ID = _Bot_Config._Archive_Category_ID()
MENTOR_ROLE = _Bot_Config._Mentor_Role_Name()
TICKET_COUNTER_FILE = _Bot_Config._Ticket_Counter_File()
INACTIVITY_CHECK_INTERVAL = 3600  # seconds
INACTIVITY_TIMEOUT = timedelta(days=2)

# Internal state: map channel_id to last activity timestamp
active_tickets = {}


def _load_counter() -> int:
    try:
        with open(TICKET_COUNTER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f).get('last_ticket_number', 0)
    except FileNotFoundError:
        return 0
    except json.JSONDecodeError:
        return 0


def _save_counter(num: int):
    os.makedirs(os.path.dirname(TICKET_COUNTER_FILE), exist_ok=True)
    with open(TICKET_COUNTER_FILE, 'w', encoding='utf-8') as f:
        json.dump({'last_ticket_number': num}, f)


def _next_ticket_number() -> str:
    last = _load_counter()
    nxt = (last + 1) % 10000
    _save_counter(nxt)
    return f"{nxt:04d}"


async def _archive_if_inactive():
    """Periodic task to archive inactive tickets."""
    guild = None
    while True:
        now = datetime.utcnow()
        for chan_id, last_time in list(active_tickets.items()):
            if now - last_time >= INACTIVITY_TIMEOUT:
                channel = guild.get_channel(chan_id) if guild else None
                if channel:
                    await _archive_ticket(channel)
                active_tickets.pop(chan_id, None)
        await asyncio.sleep(INACTIVITY_CHECK_INTERVAL)


def setup_ticketer(bot: discord.Bot):
    """Initialize slash commands and start inactivity checker."""
    @bot.tree.command(name="ticket", description="Create a support ticket")
    async def create_ticket(interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        cat = guild.get_channel(TICKET_CATEGORY_ID)
        if not cat:
            await interaction.response.send_message("Ticket category not found.", ephemeral=True)
            return
        num = _next_ticket_number()
        name = f"ticket-{num}"
        channel = await guild.create_text_channel(name, category=cat)
        msg = await channel.send(f"Hello {user.mention}, describe your issue. Use `/close_ticket` to close.")
        mentor = discord.utils.get(guild.roles, name=MENTOR_ROLE)
        if mentor:
            await channel.send(f"{mentor.mention}")
        active_tickets[channel.id] = datetime.utcnow()
        await interaction.response.send_message(f"Ticket created: {channel.mention}", ephemeral=True)

    @bot.tree.command(name="close_ticket", description="Close this ticket")
    async def close_ticket(interaction: discord.Interaction):
        channel = interaction.channel
        if not channel.name.startswith('ticket-'):
            await interaction.response.send_message("Not a ticket channel.", ephemeral=True)
            return
        perms = interaction.channel.permissions_for(interaction.user)
        mentor = discord.utils.get(interaction.guild.roles, name=MENTOR_ROLE)
        if mentor in interaction.user.roles or perms.manage_channels:
            await interaction.response.send_message("Closing ticket...")
            await channel.send("Ticket closed.")
            await _archive_ticket(channel)
        else:
            await interaction.response.send_message("Insufficient permission.", ephemeral=True)

    @bot.tree.command(name="issue", description="Create a GitHub issue")
    async def create_github_issue(interaction: discord.Interaction, title: str, *, body: str):
        await interaction.response.defer(ephemeral=True)
        url = GITHUB_API_URL.format(owner=_Bot_Config._GitHub_Owner(), repo=_Bot_Config._GitHub_Repo())
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        payload = {"title": title, "body": body}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                data = await resp.json()
        if resp.status == 201 and data.get('html_url'):
            await interaction.followup.send(f"Issue created: {data['html_url']}", ephemeral=True)
        else:
            msg = data.get('message', 'Unknown error')
            await interaction.followup.send(f"Failed: {msg}", ephemeral=True)

    # Start background archiver
    bot.loop.create_task(_archive_if_inactive())


async def _archive_ticket(channel: discord.TextChannel):
    guild = channel.guild
    cat = guild.get_channel(ARCHIVE_CATEGORY_ID)
    if cat:
        await channel.edit(category=cat)
        await channel.send("Ticket archived.")
    else:
        await channel.send("Archive category not found.")