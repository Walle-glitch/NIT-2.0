import discord
import json
import os
from discord import app_commands

# Path to the media JSON file
_Media_File = "Json_Files/media_channels.json"

def setup(bot):
    @bot.tree.command(name="add_youtube", description="Add a YouTube channel")
    async def add_youtube(interaction: discord.Interaction, channel: str):
        # Logic to add a YouTube channel
        await interaction.response.send_message(f"Added YouTube channel: {channel}", ephemeral=True)

    @bot.tree.command(name="remove_youtube", description="Remove a YouTube channel")
    async def remove_youtube(interaction: discord.Interaction, channel: str):
        # Logic to remove a YouTube channel
        await interaction.response.send_message(f"Removed YouTube channel: {channel}", ephemeral=True)

    @bot.tree.command(name="add_podcast", description="Add a podcast")
    async def add_podcast(interaction: discord.Interaction, channel: str):
        # Logic to add a podcast
        await interaction.response.send_message(f"Added podcast: {channel}", ephemeral=True)

    @bot.tree.command(name="remove_podcast", description="Remove a podcast")
    async def remove_podcast(interaction: discord.Interaction, channel: str):
        # Logic to remove a podcast
        await interaction.response.send_message(f"Removed podcast: {channel}", ephemeral=True)

# Function to load the media channels from the JSON file
def load_media_channels():
    if os.path.exists(_Media_File):
        with open(_Media_File, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"youtube": [], "podcast": []}
    return {"youtube": [], "podcast": []}

# Function to save media channels to the JSON file
def save_media_channels(media_data):
    with open(_Media_File, "w") as f:
        json.dump(media_data, f, indent=4)

# Function to add a YouTube channel or podcast
def add_channel(media_type, channel):
    media_data = load_media_channels()
    if channel not in media_data[media_type]:
        media_data[media_type].append(channel)
        save_media_channels(media_data)
        return True
    return False

# Function to remove a YouTube channel or podcast
def remove_channel(media_type, channel):
    media_data = load_media_channels()
    if channel in media_data[media_type]:
        media_data[media_type].remove(channel)
        save_media_channels(media_data)
        return True
    return False

# Function to list all active channels
def list_active_channels(media_type):
    media_data = load_media_channels()
    return media_data.get(media_type, [])

# Function to fetch the latest content from YouTube or Podcasts
async def fetch_latest_content(media_type, bot, channel_id):
    # Placeholder function: Implement actual fetching logic from APIs
    # YouTube Data API or podcast feed scraping would go here
    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"Channel with ID {channel_id} not found.")
        return

    # Sample logic for fetching and posting the latest episode (to be replaced with actual API calls)
    embed = discord.Embed(
        title=f"Latest {media_type.capitalize()} Episodes",
        description=f"Here are the latest episodes from your {media_type} channels.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Channel 1", value="Episode 1 - Some description", inline=False)
    embed.add_field(name="Channel 2", value="Episode 2 - Another description", inline=False)
    await channel.send(embed=embed)

# Function to display instructions if no channel is provided
async def display_instructions(media_type, bot, ctx):
    embed = discord.Embed(
        title=f"Add {media_type.capitalize()} Channel",
        description=f"To add a {media_type} channel, use the command:\n`/add-{media_type} [channel_name]`\nTo remove, use `/remove-{media_type} [channel_name]`.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# Function to display active channels if no channel is provided for removal
async def display_active_channels(media_type, bot, ctx):
    channels = list_active_channels(media_type)
    if channels:
        embed = discord.Embed(
            title=f"Active {media_type.capitalize()} Channels",
            description=f"Here are your active {media_type} channels:",
            color=discord.Color.blue()
        )
        for channel in channels:
            embed.add_field(name=channel, value=f"To remove: `/remove-{media_type} {channel}`", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"No active {media_type} channels found.")
