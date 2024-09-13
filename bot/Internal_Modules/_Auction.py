import discord
from datetime import datetime, timedelta
import asyncio
import json
import os
from uuid import uuid4

AUCTIONS_FILE = "Json_Files/auctions.json"  # Path to the file storing auctions
active_auctions = {}

# Function to load existing auctions from the file
def load_auctions():
    if os.path.exists(AUCTIONS_FILE):
        try:
            with open(AUCTIONS_FILE, "r") as file:
                data = json.load(file)
                for auction_data in data.get("active_auctions", []):
                    auction_data["end_time"] = datetime.fromisoformat(auction_data["end_time"])
                    active_auctions[auction_data["channel_id"]] = auction_data
        except (json.JSONDecodeError, ValueError):
            print("Error: auctions.json is empty or corrupted. Initializing with an empty auction list.")
            save_auctions()  # Create a new file with an empty structure
    else:
        save_auctions()  # If the file doesn't exist, create it

# Function to save the current state of auctions to a file
def save_auctions():
    data = {
        "active_auctions": [
            {**auction, "end_time": auction["end_time"].isoformat()}
            for auction in active_auctions.values()
        ]
    }
    with open(AUCTIONS_FILE, "w") as file:
        json.dump(data, file, indent=4)

class AuctionView(discord.ui.View):
    def __init__(self, auction_id, first_bid_placed):
        super().__init__(timeout=None)
        self.auction_id = auction_id
        self.first_bid_placed = first_bid_placed

    @discord.ui.button(label="Bid +10 kr", style=discord.ButtonStyle.green)
    async def place_bid(self, interaction: discord.Interaction, button: discord.ui.Button):
        auction = active_auctions.get(self.auction_id)
        if not auction:
            await interaction.response.send_message("No active auction found.", ephemeral=True)
            return

        if not self.first_bid_placed:
            auction["current_bid"] = auction["start_price"]
            self.first_bid_placed = True
        else:
            auction["current_bid"] += 10

        auction["highest_bidder"] = interaction.user.id

        await interaction.response.edit_message(content=f"**Item:** {auction['item_name']}\n"
                                                        f"**Current Bid:** {auction['current_bid']} kr\n"
                                                        f"**Highest Bidder:** {interaction.user.mention}",
                                                view=self)

        save_auctions()

        await interaction.followup.send(f"Your bid of {auction['current_bid']} kr has been placed!", ephemeral=True)

# Function to create a new auction with a unique ID
async def create_auction(channel, user, item_name, start_price, buy_now_price, days_duration):
    # Generate a unique ID for the auction
    auction_id = str(uuid4())  # Generates a unique identifier for the auction
    end_time = datetime.now() + timedelta(days=days_duration)

    auction = {
        "auction_id": auction_id,
        "seller": user.id,
        "item_name": item_name,
        "start_price": start_price,
        "buy_now_price": buy_now_price,
        "current_bid": start_price,
        "highest_bidder": None,
        "end_time": end_time,
        "channel_id": channel.id,
        "first_bid_placed": False  # Tracks whether the first bid is placed
    }

    active_auctions[auction_id] = auction
    save_auctions()

    # Create a thread for questions and discussion
    thread = await channel.create_thread(name=f"Questions for {item_name}", auto_archive_duration=1440)

    # Create and send the auction message with the bid button
    embed = discord.Embed(
        title=f"Auction for {item_name}",
        description=f"**Starting Price:** {start_price} kr\n"
                    f"**Buy Now Price:** {buy_now_price} kr\n"
                    f"**Auction Ends:** {end_time.strftime('%Y-%m-%d')}",
        color=discord.Color.green()
    )
    embed.set_author(name=user.display_name, icon_url=user.avatar.url)
    embed.set_footer(text=f"Auction ends on {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    view = AuctionView(auction_id, False)  # Pass auction_id instead of channel.id
    await channel.send(embed=embed, view=view)

    # Handle auction end asynchronously
    asyncio.create_task(handle_auction_end(auction_id))

async def handle_auction_end(auction_id):
    auction = active_auctions.get(auction_id)
    while auction["end_time"] > datetime.now():
        await asyncio.sleep(60)  # Check every minute

    await end_auction(auction_id)

async def end_auction(auction_id, reason="time"):
    auction = active_auctions.pop(auction_id, None)

    if not auction:
        return

    save_auctions()

    channel = auction["channel_id"]
    # Resten av auktionens slutkod förblir densamma

    if auction["highest_bidder"]:
        guild = channel.guild
        winner = await guild.fetch_member(auction["highest_bidder"])
        seller = await guild.fetch_member(auction["seller"])

        await channel.send(f"Auction for **{auction['item_name']}** is over!\n"
                           f"Winner: {winner.mention} with a bid of {auction['current_bid']} kr.")

        # Create a group DM with the seller and the winner
        group_dm = await create_group_dm([seller, winner])
        await group_dm.send(f"Congratulations! {seller.mention} and {winner.mention}, you've been connected to complete the transaction.")
    
    await channel.delete()

# Helper function to create a group DM
async def create_group_dm(users):
    return await users[0].create_dm_group(*users[1:])

# Load auctions at bot startup
load_auctions()
