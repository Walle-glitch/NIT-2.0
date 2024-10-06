import os
import json
import random
import _Bot_Config # type: ignore

XP_FILE = _Bot_Config._XP_File()  # File for storing all User XP

xp_data = {}

def load_xp_data():
    if os.path.exists(XP_FILE):
        try:
            with open(XP_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {XP_FILE} is empty or contains invalid JSON. Initializing an empty XP data structure.")
            return {}
    return {}

def save_xp_data(data):
    with open(XP_FILE, "w") as f:
        json.dump(data, f, indent=4)

def xp_needed_for_level(level):
    if level < 11:
        return 1000
    elif level < 101:
        return 10000
    else:
        return 20000

async def handle_xp(message, xp_update_channel_id, send_notifications=True):
    user = message.author
    user_id = str(user.id)

    if user_id not in xp_data:
        xp_data[user_id] = {"xp": 0, "level": 1}

    xp_data[user_id]["xp"] += random.randint(5, 15)
    save_xp_data(xp_data)

    await check_level_up(user, xp_update_channel_id, send_notifications)

async def handle_reaction_xp(message, xp_update_channel_id, send_notifications=True):
    user = message.author
    user_id = str(user.id)

    if user_id not in xp_data:
        xp_data[user_id] = {"xp": 0, "level": 1}

    xp_data[user_id]["xp"] += 10
    save_xp_data(xp_data)

    await check_level_up(user, xp_update_channel_id, send_notifications)

async def check_level_up(user, xp_update_channel_id, send_notifications=True):
    user_id = str(user.id)
    user_data = xp_data.get(user_id, {})
    current_level = user_data.get("level", 1)
    xp_needed = xp_needed_for_level(current_level)

    if user_data["xp"] >= xp_needed:
        user_data["level"] += 1
        user_data["xp"] -= xp_needed  # Remove XP needed for level up
        save_xp_data(xp_data)

        if send_notifications:
            channel = user.guild.get_channel(xp_update_channel_id)
            if channel:
                await channel.send(f"{user.mention} has leveled up to level {user_data['level']}!")

async def show_level(ctx, member):
    user_data = xp_data.get(str(member.id))
    if user_data:
        await ctx.send(f"{member.mention} is at level {user_data['level']} with {user_data['xp']} XP.")
    else:
        await ctx.send(f"{member.mention} has no XP data yet.")

async def process_historical_data(bot, XP_UPDATE_CHANNEL_ID):
    # Check if XP data is already loaded and skip processing if not empty
    if xp_data:
        print("XP file has content. Skipping historical data processing.")
        return

    print("XP file is empty. Processing historical data.")
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                async for message in channel.history(limit=None):
                    await handle_xp(message, XP_UPDATE_CHANNEL_ID, send_notifications=False)

                    for reaction in message.reactions:
                        users = [user async for user in reaction.users()]
                        for user in users:
                            if user != message.author:
                                await handle_reaction_xp(message, XP_UPDATE_CHANNEL_ID, send_notifications=False)
            except Exception as e:
                print(f"Could not process channel {channel.name}: {str(e)}")

    print("Finished processing historical data.")
