# Internal_Modules/_Media_Handler.py
"""
Module for managing media channels (YouTube and podcasts) and posting latest content.
"""
import os
import json
import discord
from discord.ext import tasks

import _Bot_Config  # type: ignore
from _logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

# Ensure JSON directory exists
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JSON_DIR = os.path.join(PROJECT_ROOT, 'Json_Files')
os.makedirs(JSON_DIR, exist_ok=True)

# Path to media file
MEDIA_FILE = _Bot_Config._Media_File()

def load_media_channels() -> dict:
    """Load media channels mapping from JSON, return defaults if missing or invalid."""
    try:
        with open(MEDIA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"Loaded media channels: {data}")
        return data
    except FileNotFoundError:
        logger.info(f"Media file not found, initializing: {MEDIA_FILE}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in {MEDIA_FILE}, resetting.")
    default = {'youtube': [], 'podcast': []}
    save_media_channels(default)
    return default


def save_media_channels(media_data: dict):
    """Persist media channels mapping to JSON."""
    try:
        with open(MEDIA_FILE, 'w', encoding='utf-8') as f:
            json.dump(media_data, f, indent=4)
        logger.debug(f"Saved media channels: {media_data}")
    except Exception as e:
        logger.error(f"Error saving media channels: {e}")


def add_channel(media_type: str, channel_name: str) -> bool:
    """Add a channel under media_type if not present, return True if added."""
    media = load_media_channels()
    if channel_name not in media.get(media_type, []):
        media.setdefault(media_type, []).append(channel_name)
        save_media_channels(media)
        return True
    logger.info(f"Channel already exists in {media_type}: {channel_name}")
    return False


def remove_channel(media_type: str, channel_name: str) -> bool:
    """Remove a channel under media_type if present, return True if removed."""
    media = load_media_channels()
    if channel_name in media.get(media_type, []):
        media[media_type].remove(channel_name)
        save_media_channels(media)
        return True
    logger.info(f"Channel not found in {media_type}: {channel_name}")
    return False


def list_active_channels(media_type: str) -> list:
    """Return list of channels for given media_type."""
    media = load_media_channels()
    return media.get(media_type, [])


class MediaPoster:
    """Handles periodic fetching and posting of media content."""
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.youtube_channel_id = _Bot_Config._YouTube_Channel_ID()
        self.podcast_channel_id = _Bot_Config._Podcast_Channel_ID()
        self.fetch_interval = 60  # in minutes

    @tasks.loop(minutes=60)
    async def post_latest(self):
        # Post YouTube
        await self._post_media('youtube', self.youtube_channel_id)
        # Post Podcast
        await self._post_media('podcast', self.podcast_channel_id)

    async def _post_media(self, media_type: str, channel_id: int):
        """Fetch latest and post embed to channel."""
        channels = list_active_channels(media_type)
        channel = self.bot.get_channel(channel_id)
        if not channel:
            logger.error(f"Channel ID not found: {channel_id}")
            return

        embed = discord.Embed(
            title=f"Latest {media_type.capitalize()} Episodes",
            description=f"From: {', '.join(channels)}",
            color=discord.Color.blue()
        )
        # Placeholder fields: to be replaced with real API data
        for idx, name in enumerate(channels, start=1):
            embed.add_field(name=f"{name}", value=f"Episode {idx} - Description...", inline=False)

        await channel.send(embed=embed)
        logger.info(f"Posted latest {media_type} to channel {channel_id}")

    def start(self):
        """Start the periodic posting task."""
        logger.info("Starting media poster loop.")
        self.post_latest.start()


def setup(bot: discord.Bot):
    """Initialize media handler tasks."""
    poster = MediaPoster(bot)
    poster.start()