# Internal_Modules/_Bot_Modul.py
"""
Core utility module for resource embeds, RFC lookup, and job postings.
"""
import os
import json
import requests  # For synchronous RFC lookup
import aiohttp   # For asynchronous job fetching
from bs4 import BeautifulSoup
import discord
from datetime import datetime

import _Bot_Config
from _logging_setup import setup_logging

# --- 1. Initial Setup ---
logger = setup_logging()

# --- 2. Setup Function ---
def setup():
    """Initializes the Bot Module."""
    # This module doesn't need complex setup for now, but the function must exist.
    logger.info("Bot Module (Jobs & Utilities) setup complete.")


# --- 3. Job Posting ---
INDEED_API_KEY = os.getenv('INDEED_API_KEY') # It's better to load this once

async def fetch_and_post_jobs(bot: discord.Client, channel_id: int):
    """
    Fetches job listings from the Indeed API asynchronously and posts them as embeds.
    This is the single, corrected version of the function.
    """
    # Note: Indeed's public API for job search was deprecated.
    # This may not work without a valid, grandfathered publisher key.
    if not INDEED_API_KEY:
        logger.warning("INDEED_API_KEY is not set. Skipping job fetch.")
        return

    params = {
        'publisher': INDEED_API_KEY,
        'q': "Network Engineer",
        'l': "Sweden",
        'sort': 'date',
        'format': 'json',
        'v': '2'
    }
    url = "https://api.indeed.com/ads/apisearch"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status() # Will raise an error for 4xx/5xx status
                data = await response.json()
                jobs = data.get('results', [])

                if not jobs:
                    logger.info("No new jobs found via API.")
                    return

                channel = bot.get_channel(channel_id)
                if not channel:
                    logger.error(f"Job posting channel with ID {channel_id} not found.")
                    return

                logger.info(f"Posting {len(jobs)} new jobs to channel {channel.name}.")
                for job in jobs[:5]: # Limit to the 5 newest jobs
                    embed = discord.Embed(
                        title=job.get('jobtitle', 'No Title'),
                        description=f"{job.get('company', 'N/A')} - {job.get('formattedLocation', 'N/A')}",
                        url=job.get('url'),
                        color=discord.Color.blue()
                    )
                    await channel.send(embed=embed)

    except aiohttp.ClientError as e:
        logger.error(f"Job fetch network error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during job fetching: {e}", exc_info=True)


# --- 4. Other Utilities (for potential use in slash commands) ---

async def log_to_channel(bot: discord.Client, message: str):
    """Send message to the designated log channel."""
    log_channel_id = _Bot_Config._Log_Channel_ID()
    logger.info(message)
    channel = bot.get_channel(log_channel_id)
    if channel:
        try:
            await channel.send(f"```{datetime.now():%Y-%m-%d %H:%M:%S} - {message}```")
        except discord.Forbidden:
            logger.error(f"Cannot send log to channel {log_channel_id} due to permissions.")


def get_rfc(rfc_number: int) -> str:
    """
    Fetches an RFC title and link using a synchronous request.
    This is suitable for a command context where a small block is acceptable.
    """
    if rfc_number <= 0:
        return "Error: Invalid RFC number provided."

    url = f"https://datatracker.ietf.org/doc/html/rfc{rfc_number}"
    try:
        # Using requests here is fine for a one-off command action
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else "RFC title not found."
        return f"**{title}**\n{url}"
    except requests.RequestException as e:
        logger.error(f"RFC fetch error for RFC {rfc_number}: {e}")
        return f"Error: Could not retrieve RFC {rfc_number}."