# Internal_Modules/_Auction.py
"""
Auction module for creating and managing auctions.
"""
import os
import json
import asyncio
from uuid import uuid4
from datetime import datetime, timedelta
import discord
from discord.ext import tasks
import _Bot_Config  # type: ignore
from _logging_setup import setup_logging






# Initialize logger
logger = setup_logging()

# Ensure Json_Files directory exists
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JSON_DIR = os.path.join(PROJECT_ROOT, 'Json_Files')
os.makedirs(JSON_DIR, exist_ok=True)

# File for storing auctions
AUCTIONS_FILE = _Bot_Config._Auctions_File()

# In-memory auctions store
active_auctions = {}


def setup(bot: commands.Bot):
    """Initializes the Auction module by loading data and registering commands."""
    global auctions
    if os.path.exists(AUCTION_FILE):
        with open(AUCTION_FILE, 'r') as f:
            auctions = json.load(f)
    logger.info(f"Loaded {len(auctions)} auctions from file.")

    @bot.tree.command(name="auction", description="Manage auctions.")
    async def auction(interaction: discord.Interaction, action: str, item: str = None, starting_bid: int = 0):
        # Your auction logic here
        await interaction.response.send_message(f"Auction command '{action}' executed.", ephemeral=True)

    logger.info("Auction module setup complete.")



def load_auctions():
    """Load existing auctions from JSON file."""
    if os.path.isfile(AUCTIONS_FILE):
        try:
            with open(AUCTIONS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for entry in data.get('active_auctions', []):
                entry['end_time'] = datetime.fromisoformat(entry['end_time'])
                active_auctions[entry['auction_id']] = entry
            logger.info(f"Loaded {len(active_auctions)} auctions from file.")
        except Exception as e:
            logger.error(f"Error loading auctions file: {e}")
            save_auctions()
    else:
        save_auctions()


def save_auctions():
    """Persist current auctions to JSON file."""
    data = {
        'active_auctions': [
            {**a, 'end_time': a['end_time'].isoformat()}
            for a in active_auctions.values()
        ]
    }
    try:
        with open(AUCTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        logger.debug(f"Saved {len(active_auctions)} auctions.")
    except Exception as e:
        logger.error(f"Error saving auctions file: {e}")


class AuctionView(discord.ui.View):
    """UI view with bid and buy buttons."""
    def __init__(self, auction_id: str):
        super().__init__(timeout=None)
        self.auction_id = auction_id

    @discord.ui.button(label="Bid +10 kr", style=discord.ButtonStyle.green)
    async def bid_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        auction = active_auctions.get(self.auction_id)
        if not auction:
            await interaction.response.send_message("Ingen aktiv auktion hittades.", ephemeral=True)
            return

        # Increment bid
        auction['current_bid'] += 10
        auction['highest_bidder'] = interaction.user.id
        save_auctions()

        content = (
            f"**Item:** {auction['item_name']}\n"
            f"**Current Bid:** {auction['current_bid']} kr\n"
            f"**Highest Bidder:** <@{auction['highest_bidder']}>"
        )
        await interaction.response.edit_message(content=content, view=self)

    @discord.ui.button(label="Buy Now", style=discord.ButtonStyle.red)
    async def buy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        auction = active_auctions.get(self.auction_id)
        if not auction:
            await interaction.response.send_message("Ingen aktiv auktion hittades.", ephemeral=True)
            return

        auction['current_bid'] = auction['buy_now_price']
        auction['highest_bidder'] = interaction.user.id
        save_auctions()

        # Finalize auction
        await end_auction(auction['auction_id'], interaction.client)
        await interaction.response.edit_message(
            content=(
                f"**Item:** {auction['item_name']}\n"
                f"**Sold to:** <@{auction['highest_bidder']}> för {auction['buy_now_price']} kr.\n"
                "**Auction Ended**"
            ),
            view=None
        )


async def create_auction(channel: discord.TextChannel, user: discord.Member,
                   item_name: str, start_price: int,
                   buy_now_price: int, days_duration: int):
    """Initialize a new auction and post the embed with buttons."""
    auction_id = str(uuid4())
    end_time = datetime.now() + timedelta(days=days_duration)

    auction = {
        'auction_id': auction_id,
        'seller': user.id,
        'item_name': item_name,
        'start_price': start_price,
        'buy_now_price': buy_now_price,
        'current_bid': start_price,
        'highest_bidder': None,
        'end_time': end_time,
        'channel_id': channel.id
    }
    active_auctions[auction_id] = auction
    save_auctions()

    embed = discord.Embed(
        title=f"Auktion: {item_name}",
        description=(
            f"**Startpris:** {start_price} kr\n"
            f"**Buy Now:** {buy_now_price} kr\n"
            f"**Slutar:** {end_time:%Y-%m-%d %H:%M:%S}"
        ),
        color=discord.Color.blurple()
    )
    embed.set_author(name=user.display_name, icon_url=user.avatar.url)

    view = AuctionView(auction_id)
    message = await channel.send(embed=embed, view=view)

    # Optionally create thread for discussion
    try:
        thread = await message.create_thread(name=f"Discussion: {item_name}", auto_archive_duration=1440)
        await thread.send(f"{user.mention}, här kan du diskutera din vara.")
    except Exception as e:
        logger.debug(f"Could not create thread: {e}")

    # Schedule auction end
    schedule_auction_end(auction_id)


def schedule_auction_end(auction_id: str):
    """Start a background task to end the auction when time is due."""
    @tasks.loop(minutes=1, count=1)
    async def check_end():
        auction = active_auctions.get(auction_id)
        if auction and datetime.now() >= auction['end_time']:
            await end_auction(auction_id)
            check_end.stop()

    check_end.start()


async def end_auction(auction_id: str, bot_client: discord.Client = None):
    """Finalize auction: announce winner and notify participants."""
    auction = active_auctions.pop(auction_id, None)
    save_auctions()

    if not auction:
        return

    # Retrieve guild and channel
    if not bot_client:
        # fallback: use any running client
        bot_client = discord.utils.get(discord.Client().guilds)
    guild = bot_client.get_guild(auction['channel_id'])
    channel = guild.get_channel(auction['channel_id'])

    # Announce result
    if auction['highest_bidder']:
        winner = guild.get_member(auction['highest_bidder'])
        await channel.send(
            f"Auktionen för **{auction['item_name']}** är över! \
"
            f"Vinnare: {winner.mention} med {auction['current_bid']} kr."
        )
        # Notify via DM
        seller = guild.get_member(auction['seller'])
        for member, role in ((seller, 'säljare'), (winner, 'vinnare')):
            try:
                await member.send(
                    f"Din auktion för **{auction['item_name']}** är avslutad. Du är {role}."
                )
            except discord.Forbidden:
                logger.debug(f"Could not DM {member.display_name}")

    # Optionally clean up: disable view, archive thread, etc.

# Load auctions on module import
def setup():
    load_auctions()

setup()