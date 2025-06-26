# Internal_Modules/_Bot_Modul.py
"""
Core utility module for resource embeds, RFC lookup, and job postings.
"""
import os
import json
import requests
from bs4 import BeautifulSoup
import discord
from datetime import datetime

import _Bot_Config  # type: ignore
from _logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

# Channel IDs
LOG_CHANNEL_ID = _Bot_Config._Log_Channel_ID()
ADMIN_CHANNEL_ID = _Bot_Config._Admin_Channel_ID()

# --------------- Logging Utility ---------------
async def log_to_channel(bot, message: str):
    """Send message to log channel and server console."""
    logger.info(message)
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        try:
            await channel.send(message)
        except discord.Forbidden:
            logger.error(f"Cannot send log to channel {LOG_CHANNEL_ID}")

# --------------- Resource Command ---------------
async def send_resource_embed(ctx):
    """Send a series of embeds with study resources."""
    resources = [
        {
            "title": "Course Books and Resources",
            "fields": [
                ("linux (ogl)", "https://dl.remilia.se/os/"),
                ("python notes", "https://files.catbox.moe/tj6k7c.zip"),
                # add more as needed
            ]
        },
        {
            "title": "YouTube Resources",
            "fields": [
                ("CCNA Playlist", "https://youtube.com/playlist?list=PLxbwE86jKRgM"),
                ("NetworkChuck", "https://www.youtube.com/@NetworkChuck"),
            ]
        },
    ]
    for res in resources:
        embed = discord.Embed(title=res["title"], color=discord.Color.blue())
        for name, url in res["fields"]:
            embed.add_field(name=name, value=url, inline=False)
        await ctx.send(embed=embed)

# --------------- RFC Lookup Command ---------------
def get_rfc(rfc_number: int) -> str:
    """Fetch RFC title and return it with link."""
    if rfc_number <= 0:
        return "Error: Invalid RFC number."
    url = f"https://datatracker.ietf.org/doc/html/rfc{rfc_number}"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        title_tag = soup.find('title')
        title = title_tag.text if title_tag else "RFC title not found."
        return f"{title}\nLink: {url}"
    except requests.RequestException as e:
        logger.error(f"RFC fetch error: {e}")
        return f"Error retrieving RFC: {e}"

# --------------- Job Posting Command ---------------
INDEED_API_URL = "https://api.indeed.com/ads/apisearch"
INDEED_API_KEY = os.getenv('INDEED_API_KEY')

def fetch_jobs(query: str = "Network Technician", location: str = "Sweden") -> list:
    """Fetch jobs from Indeed API and return list of dicts."""
    params = {
        'publisher': INDEED_API_KEY,
        'q': query,
        'l': location,
        'sort': 'date',
        'format': 'json',
        'v': '2'
    }
    try:
        response = requests.get(INDEED_API_URL, params=params)
        response.raise_for_status()
        data = response.json().get('results', [])
        return [
            {'title': job['jobtitle'], 'company': job['company'], 'location': job['formattedLocation'], 'url': job['url']}
            for job in data
        ]
    except Exception as e:
        logger.error(f"Job fetch error: {e}")
        return []

async def fetch_and_post_jobs(bot, channel_id: int):
    """Fetch jobs and post as embeds in specified channel."""
    jobs = fetch_jobs()
    if not jobs:
        logger.info("No jobs found.")
        return
    channel = bot.get_channel(channel_id)
    if not channel:
        logger.error(f"Channel {channel_id} not found.")
        return
    for job in jobs:
        embed = discord.Embed(
            title=job['title'],
            description=f"{job['company']} - {job['location']}",
            url=job['url'],
            color=discord.Color.green()
        )
        await channel.send(embed=embed)
