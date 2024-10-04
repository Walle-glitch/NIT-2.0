import discord
from datetime import datetime, timedelta
import asyncio
import json
import os
from uuid import uuid4
import _Bot_Config # type: ignore

AUCTIONS_FILE = _Bot_Config._Auctions_File()
active_auctions = {}

# Load existing auctions from the file
def load_auctions():
    if os.path.exists(AUCTIONS_FILE):
        try:
            with open(AUCTIONS_FILE, "r") as file:
                data = json.load(file)
                for auction_data in data.get("active_auctions", []):
                    auction_data["end_time"] = datetime.fromisoformat(auction_data["end_time"])
                    active_auctions[auction_data["auction_id"]] = auction_data
        except (json.JSONDecodeError, ValueError):
            print("Error: auctions.json is empty or corrupted. Initializing with an empty auction list.")
            save_auctions()  # Create a new file with an empty structure
    else:
        save_auctions()  # If the file doesn't exist, create it

# Save the current state of auctions to a file
def save_auctions():
    data = {
        "active_auctions": [
            {**auction, "end_time": auction["end_time"].isoformat()}
            for auction in active_auctions.values()
        ]
    }
    with open(AUCTIONS_FILE, "w") as file:
        json.dump(data, file, indent=4)

# View for the auction buttons
class AuctionView(discord.ui.View):
    def __init__(self, auction_id, first_bid_placed, auction_channel):
        super().__init__(timeout=None)
        self.auction_id = auction_id
        self.first_bid_placed = first_bid_placed
        self.auction_channel = auction_channel

    # Bid button
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

        # Update the auction message
        await interaction.response.edit_message(content=f"**Item:** {auction['item_name']}\n"
                                                        f"**Current Bid:** {auction['current_bid']} kr\n"
                                                        f"**Highest Bidder:** {interaction.user.mention}",
                                                view=self)

        save_auctions()

    # Buy Now button
    @discord.ui.button(label="Buy Now", style=discord.ButtonStyle.red)
    async def buy_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        auction = active_auctions.get(self.auction_id)
        if not auction:
            await interaction.response.send_message("No active auction found.", ephemeral=True)
            return

        auction["current_bid"] = auction["buy_now_price"]
        auction["highest_bidder"] = interaction.user.id

        # End the auction immediately
        await end_auction(self.auction_id, reason="buy_now")

        # Remove the buttons from the auction post
        await interaction.response.edit_message(content=f"**Item:** {auction['item_name']}\n"
                                                        f"**Sold to:** {interaction.user.mention} for {auction['buy_now_price']} kr.\n"
                                                        f"**Auction Ended**",
                                                view=None)

        save_auctions()

# Function to create a new auction with a unique ID
async def create_auction(channel, user, item_name, start_price, buy_now_price, days_duration):
    # Generate a unique ID for the auction
    auction_id = str(uuid4())
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
        "first_bid_placed": False
    }

    active_auctions[auction_id] = auction
    save_auctions()

    # Create and send the auction message with the bid and buy now buttons
    embed = discord.Embed(
        title=f"Auction for {item_name}",
        description=f"**Starting Price:** {start_price} kr\n"
                    f"**Buy Now Price:** {buy_now_price} kr\n"
                    f"**Auction Ends:** {end_time.strftime('%Y-%m-%d %H:%M:%S')}",
        color=discord.Color.green()
    )
    embed.set_author(name=user.display_name, icon_url=user.avatar.url)

    view = AuctionView(auction_id, False, channel)
    auction_message = await channel.send(embed=embed, view=view)

    # Create a thread and ping the user
    thread = await auction_message.create_thread(name=f"{item_name} Discussion", auto_archive_duration=1440)
    await thread.send(f"{user.mention}, här kan du lägga till information om din vara, eller svara på frågor om den.")

    # Handle auction end asynchronously
    asyncio.create_task(handle_auction_end(auction_id))

# Function to handle auction end
async def handle_auction_end(auction_id):
    auction = active_auctions.get(auction_id)
    while auction["end_time"] > datetime.now():
        await asyncio.sleep(60)  # Check every minute

    await end_auction(auction_id)

# Function to finalize the auction
async def end_auction(auction_id, reason="time"):
    auction = active_auctions.pop(auction_id, None)

    if not auction:
        return

    save_auctions()

    channel_id = auction["channel_id"]
    guild = discord.utils.get(discord.Client().guilds, id=channel_id)  # Fetch the guild the auction belongs to
    channel = guild.get_channel(channel_id)

    if auction["highest_bidder"]:
        winner = await guild.fetch_member(auction["highest_bidder"])
        seller = await guild.fetch_member(auction["seller"])

        await channel.send(f"Auction for **{auction['item_name']}** is over!\n"
                           f"Winner: {winner.mention} with a bid of {auction['current_bid']} kr.")

        # Send PMs to the seller and winner
        try:
            await seller.send(f"Your auction for **{auction['item_name']}** has ended. The winner is {winner.display_name} with a bid of {auction['current_bid']} kr.")
        except discord.Forbidden:
            print(f"Could not send PM to seller {seller.display_name}")

        try:
            await winner.send(f"Congratulations! You won the auction for **{auction['item_name']}** with a bid of {auction['current_bid']} kr.")
        except discord.Forbidden:
            print(f"Could not send PM to winner {winner.display_name}")

    # Remove the buttons and disable the view
    await channel.edit(name=f"closed-{auction['item_name']}")

    # Delete the auction channel after closing
    await channel.delete()

# Load auctions at bot startup
load_auctions()
