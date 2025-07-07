# Internal_Modules/_Auction.py
import discord
from discord import app_commands
from discord.ext import commands  # <--- THIS LINE FIXES THE ERROR
import json
import os
from _logging_setup import setup_logging

logger = setup_logging()
AUCTION_FILE = "Json_Files/auctions.json"
auctions = {}

def setup(bot: commands.Bot):
    """Initializes the Auction module by loading data and registering commands."""
    global auctions
    
    try:
        if os.path.exists(AUCTION_FILE):
            with open(AUCTION_FILE, 'r') as f:
                # Handle empty or invalid JSON file
                content = f.read()
                if content:
                    auctions = json.loads(content)
                else:
                    auctions = {}
        else:
            # Create the file if it doesn't exist
            with open(AUCTION_FILE, 'w') as f:
                json.dump({}, f)
            auctions = {}
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error loading auctions file: {e}")
        auctions = {}

    logger.info(f"Loaded {len(auctions)} auctions from file.")

    @bot.tree.command(name="auction", description="Manage auctions.")
    @app_commands.describe(action="The action to perform (create, bid, view).", item="The item to auction.", starting_bid="The starting bid amount.")
    async def auction(interaction: discord.Interaction, action: str, item: str = None, starting_bid: int = 0):
        # Your auction logic here
        await interaction.response.send_message(f"Auction command '{action}' executed.", ephemeral=True)

    logger.info("Auction module setup complete.")