# This is Main.py, the main file for the bot

###########################################_Import_Modules_##########################################

import os
import discord
import sys
import subprocess
import asyncio
from discord.ext import commands, tasks
from urllib.request import urlopen
import json

# Bot specific Modules
import botConfig  # Bot token and bot information exists locally on the server; this module contains that info.
import _Bot_Modul  # Module for various functions.
import _Games  # Module for games.
import _Open_AI  # Module for handling OpenAI API requests.
import _CCIE_Study_Plan  # CCIE study plan module.
import _CCNP_Study_Plan  # CCNP study plan module.

###########################################_Global_Variables_##########################################

version_nr = "Current Version is 24/08/27.100"  # Global version number variable

# Roles with access to "Sudo commands"
BOT_ADMIN_ROLE_NAME = "Bot-Master"
ADMIN_ROLE_NAME = "Privilege 15"
MOD_ROLE_NAME = "Privilege 10"

# Initialize global variables
current_question = None
correct_answer = None

# Channel IDs
XP_UPDATE_CHANNEL_ID = 1012067343452622949  # Channel for level-up notifications
JOB_CHANNEL_ID = 1012235998308094032  # External job postings
CCIE_STUDY_CHANNEL_ID = 1277674142686248971  # CCIE study channel
CCNP_STUDY_CHANNEL_ID = 1277675077428842496  # CCNP study channel
WELCOME_CHANNEL_ID = 1012026430470766818  # Welcome channel
LOG_CHANNEL_ID = 1277567653765976074  # The Discord channel ID where you want to send the logs

# File Managment 
ROLE_JSON_FILE = "Json_Files/roles.json"  # File where roles are stored
EXCLUDED_ROLES = ["Admin", "Moderator", "Administrator"]  # Roles that cannot be assigned via reactions

###########################################_Bot_Set_Up_Stuff_##########################################

intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True  # Enable reaction events
intents.guilds = True  # Access to server information, including roles
intents.members = True  # Access to members for role assignment

# Command Prefix
bot = commands.Bot(command_prefix="./", intents=intents)

##################_BOT_BOOT_##################

# Create a function that sends messages to both server logs and a Discord channel
async def log_to_channel(bot, message):
    print(message)  # Print to server logs

    # Fetch the Discord channel
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(message)  # Send the message to the Discord channel
    else:
        print("Log channel not found")

@bot.event
async def on_ready():
    await log_to_channel(bot, f'Logged in as {bot.user}')
    await log_to_channel(bot, "Processing historical data, notifications are disabled. This Will take a while...") # Disable notifications for historical data processing
    await _Bot_Modul.process_historical_data(bot, XP_UPDATE_CHANNEL_ID)
    await log_to_channel(bot, "Finished processing historical data, notifications are now enabled.") # Re-enable notifications after processing is done
    # Start scheduled tasks when the bot is ready
    weekly_study_plan_CCIE.start()  
    weekly_study_plan_CCNP.start()  
    update_roles.start()  
    check_welcome_message.start()  
    await log_to_channel(bot, "All Boot Events are now completed") # Re-enable notifications after processing is done

###########################################_All_User_Commands_##########################################

#############################_Utilities_Commands_#############################

# Resource command
@bot.command(name="r")
async def resuser_command(ctx):
    try:
        await _Bot_Modul.send_resource_embed(ctx)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Help Command
@bot.command()
async def h(ctx):
    """
    Display a list of all available commands with descriptions and the current bot version.
    """
    embed = discord.Embed(
        title="Available Commands",
        description=f"Current version: {version_nr}\n\nHere is a list of all available commands:",
        color=discord.Color.blue()
    )
    
    commands_list = {
        "resurser": "./r - Display a list of useful resources.",
        "Help": "./h - Display this help message.",
        "Version": "./version - Show the current bot version.",
        "Git Repository": "./git - Provide the link to the bot's GitHub repository.",
        "Hello": "./hello - Say hello to the bot.",
        "About": "./about - Information about the bot and its purpose.",
        "Ticket": "./ticket [name] - Create a new channel for discussing a specific issue. Use ./close to close this channel.",
        "Close": "./close - Close the current ticket channel.",
        "Subnet Game": "./subnet - Start a subnet game.",
        "Game Menu": "./spel - Choose between different games (Subnet and Network Questions).",
        "Ping": "./ping [IP_ADDRESS] - Perform a ping test to the specified IP address.",
        "RFC": "./rfc [NUMBER] - Retrieve information about the specified RFC number.",
        "BGP Setup": "./BGP-Setup [IP_ADDRESS] [AS_NUMBER] - Configure BGP peering with the given IP address and AS number.",
        "Add Role": "./addrole - Assign a predefined role to the user.",
        "Remove Role": "./removerole - Remove a predefined role from the user.",
        "Kick": "./kick [username] - Kick a user from the server. (Privilege 10/15 only)",
        "Ban": "./ban [username] - Ban a user from the server. (Privilege 10/15 only)",
        "Mute": "./mute [hours] [username] - Mute a user for a specified number of hours. (Privilege 10/15 only)",
        "Reboot": "./Reboot - Perform a git pull and restart the bot. (Bot-Admin only)",
        "Test": "./test - Test all commands. (Bot-Admin only)"
    }

    for command, description in commands_list.items():
        embed.add_field(name=command, value=description, inline=False)
    
    await ctx.send(embed=embed)

# Version Command
@bot.command()
async def version(ctx):
    await ctx.send(version_nr)

# Git Repository Command
@bot.command()
async def git(ctx):
    await ctx.send('https://github.com/Walle-glitch/NIT-2.0.git')

# About Command
@bot.command()
async def about(ctx):
    reply = (
    'The NIT-BOT is a fun bot here on our Discord.\n' 
    'It is public on GitHub and anyone is free to contribute to it,' 
    'either for fun or other (non-malicious) projects.\n' 
    'The server it is hosted on is at my home,' 
    'so it is behind a normal (NAT Gateway).\n'
    '\n' 
    'Contact Walle/Nicklas for more info.'
    'Use ./git for the link to the GitHub repo.\n'
    )
    await ctx.send(reply)

# Ticket creation     
@bot.command(name="ticket")
async def create_ticket_command(ctx, *, channel_name=None):
    guild = ctx.guild
    category_id = 1012026430470766816  # Replace with your actual category ID
    channel = await _Bot_Modul.create_ticket(guild, category_id, ctx.author, channel_name)
    
    if channel:
        await ctx.send(f"Your ticket has been created: {channel.mention}")
    else:
        await ctx.send("Failed to create the ticket. Please contact an administrator.")

@bot.command(name="close")
async def close_ticket_command(ctx):
    await _Bot_Modul.close_ticket(ctx.channel)
    await ctx.send("This ticket has been closed.")

#############################_Open_AI_Commands_#############################

@bot.command(name="AI")
async def ai_command(ctx, *, question=None):
    if question is None:
        await ctx.send("Please provide a question after the command: `./AI \"Question\"`")
        return
    
    await _Open_AI.handle_ai_session(ctx, question)


#############################_User_Test_Commands_#############################

# Hello Command
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

#############################_Game_Commands_#############################

@bot.command()
async def subnet(ctx):
    global current_question, correct_answer
    
    current_question, correct_answer = _Games.generate_subnet_question()
    await ctx.send(f"Subnet question: {current_question}")

@bot.event
async def on_message(message):
    global current_question, correct_answer
    
    if current_question and message.author != bot.user:
        user_answer = message.content
        
        if _Games.check_answer(user_answer, correct_answer):
            await message.channel.send("Correct answer! Well done!")
            _Games.reset_game()
        else:
            await message.channel.send(f"Incorrect answer. The correct answer is: {correct_answer}")
        
        current_question = None
        correct_answer = None
    
    await bot.process_commands(message)


#############################_Network_Commands_#############################

@bot.command()
async def ping(ctx, ip: str = "8.8.8.8"):
    """
    Performs a ping test to a given IP address. If no IP address is specified,
    it defaults to 8.8.8.8.
    """
    try:
        result = subprocess.run(["ping", "-c", "4", ip], capture_output=True, text=True)
        await ctx.send(f"Ping results for {ip}:\n```\n{result.stdout}\n```")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"ERROR:\n```\n{e.stderr}\n```")

@bot.command()
async def BGP(ctx):
    reply = (
        'When using the ./BGP_Setup command,\n' 
        'you need to provide two variables,\n'
        'like this: "./BGP_Setup [your IP address] [your AS number]".\n'
        'You will receive a reply with the needed info when the configuration is complete.'
    )
    await ctx.send(reply)

@bot.command()
async def BGP_Setup(ctx, neighbor_ip: str, neighbor_as: str):
    await ctx.send("Starting BGP configuration...")
    gi0_ip, as_number = _Bot_Modul.configure_bgp_neighbor(neighbor_ip, neighbor_as)
    
    if as_number is None:
        await ctx.send(f"An error occurred: {gi0_ip}")
    else:
        await ctx.send(f"BGP configuration complete. GigabitEthernet0/0 IP address: {gi0_ip}, AS number: {as_number}")

############################_Role_Assignment_############################

@tasks.loop(hours=1)
async def update_roles():
    try:    
        await _Bot_Modul.fetch_and_save_roles(bot)
    except Exception as e:
        await print(f"An error occurred: {str(e)}")

@bot.command()
async def roll(ctx, *, role_name: str):
    try:    
        await _Bot_Modul.assign_role(ctx, role_name)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

#############################_Study_Commands_#############################

@bot.command()
async def rfc(ctx, rfc_number: str = None):
    """
    Retrieves and displays information about an RFC based on the number.
    
    :param rfc_number: RFC number to fetch. If none is provided, an error message is displayed.
    """
    if rfc_number is None:
        await ctx.send("Error: No RFC number provided. Please provide an RFC number after the command.")
        return

    try:
        rfc_number = int(rfc_number)
        result = _Bot_Modul.get_rfc(rfc_number)
    except ValueError:
        result = "Error: Invalid RFC number. Please provide a valid integer."

    await ctx.send(result)

###########################################_Below this line_###########################################

# Role name to be assigned by the bot
ROLE_NAME = "YourRoleName"

@bot.command()
async def addrole(ctx):
    """
    Assigns a specific role to the user running the command.
    Uses an embedded message to provide feedback.
    """
    role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
    
    if role is None:
        await ctx.send(f"Role '{ROLE_NAME}' could not be found on the server.")
        return

    if role in ctx.author.roles:
        embed = discord.Embed(title="Role Assigned", description=f"You already have the role **{ROLE_NAME}**.", color=discord.Color.orange())
    else:
        try:
            await ctx.author.add_roles(role)
            embed = discord.Embed(title="Role Assigned", description=f"The role **{ROLE_NAME}** has been assigned to you!", color=discord.Color.green())
        except discord.Forbidden:
            embed = discord.Embed(title="Error", description="I do not have sufficient permissions to assign this role.", color=discord.Color.red())
    
    await ctx.send(embed=embed)

@bot.command()
async def removerole(ctx):
    """
    Removes a specific role from the user running the command.
    Uses an embedded message to provide feedback.
    """
    role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
    
    if role is None:
        await ctx.send(f"Role '{ROLE_NAME}' could not be found on the server.")
        return

    if role not in ctx.author.roles:
        embed = discord.Embed(title="Role Removed", description=f"You do not have the role **{ROLE_NAME}**.", color=discord.Color.orange())
    else:
        try:
            await ctx.author.remove_roles(role)
            embed = discord.Embed(title="Role Removed", description=f"The role **{ROLE_NAME}** has been removed from you.", color=discord.Color.green())
        except discord.Forbidden:
            embed = discord.Embed(title="Error", description="I do not have sufficient permissions to remove this role.", color=discord.Color.red())
    
    await ctx.send(embed=embed)

###########################################_Study_Plan_Loops_###########################################

@tasks.loop(hours=168)  # CCIE study plan loop (weekly)
async def weekly_study_plan_CCIE():
    await _CCIE_Study_Plan.post_weekly_goal_CCIE(bot, CCIE_STUDY_CHANNEL_ID)

@tasks.loop(hours=168)  # CCNP study plan loop (weekly)
async def weekly_study_plan_CCNP():
    await _CCNP_Study_Plan.post_weekly_goal_CCNP(bot, CCNP_STUDY_CHANNEL_ID)

# Command to manually fetch and post jobs
@bot.command()
async def post_jobs(ctx):
    await _Bot_Modul.fetch_and_post_jobs(bot, JOB_CHANNEL_ID)

@tasks.loop(hours=24)  # Job posting loop (daily)
async def job_posting_loop():
    await _Bot_Modul.fetch_and_post_jobs(bot, JOB_CHANNEL_ID)

# Welcome Message
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}!")

# XP Levels Handling
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await _Bot_Modul.handle_xp(message, XP_UPDATE_CHANNEL_ID)
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    await _Bot_Modul.handle_reaction_xp(reaction.message, XP_UPDATE_CHANNEL_ID)

# Command to show user's level and XP
@bot.command()
async def level(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    await _Bot_Modul.show_level(ctx, member)

# Loop to check welcome message every hour
@tasks.loop(hours=1)
async def check_welcome_message():
    await _Bot_Modul.ensure_welcome_message(bot, WELCOME_CHANNEL_ID)

###########################################_Admin_Commands_###########################################

def has_privileged_role(ctx):
    roles = [role.name for role in ctx.author.roles]
    return "Privilege 15" in roles or "Privilege 10" in roles

# Kick Command
@bot.command(name="kick")
@commands.check(has_privileged_role)
@commands.has_permissions(kick_members=True)
async def kick_command(ctx, user: discord.Member, *, reason=None):
    try:
        await _Bot_Modul.kick_user(ctx, user, reason)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Ban Command
@bot.command(name="ban")
@commands.check(has_privileged_role)
@commands.has_permissions(ban_members=True)
async def ban_command(ctx, user: discord.Member, *, reason=None):
    try:
        await _Bot_Modul.ban_user(ctx, user, reason)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Mute Command
@bot.command(name="mute")
@commands.check(has_privileged_role)
@commands.has_permissions(moderate_members=True)
async def mute_command(ctx, duration: int, user: discord.Member, *, reason=None):
    try:
        await _Bot_Modul.mute_user(ctx, user, duration, reason)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Reboot Command
@bot.command(name="Reboot")
@commands.has_role(BOT_ADMIN_ROLE_NAME)
async def reboot(ctx):
    await ctx.send("Performing `git pull` and restarting the bot...")
    try:
        result = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
        await ctx.send(f"`git pull` executed:\n```\n{result.stdout}\n```")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"Error during `git pull`:\n```\n{e.stderr}\n```")
        return

    python = sys.executable
    os.execl(python, python, *sys.argv)

# Handle errors for the Reboot command
@reboot.error
async def reboot_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")

# Admin command to test all commands
@bot.command()
@commands.has_role(BOT_ADMIN_ROLE_NAME)
async def test(ctx):
    test_commands = [
        ("version", None),
        ("h", None),
        ("git", None),
        ("hello", None),
        ("about", None),
        ("ping", "8.8.8.8"),
        ("rfc", "791"),
        ("subnet", "null"),
        ("BGP-Setup", "1.1.1.1 65000"),
        ("start_game", "subnet"),
        ("stop_game", None),
        ("start_game", "network"),
        ("stop_game", None),
        ("Reboot", None),
    ]
    
    for command_name, arg in test_commands:
        command = bot.get_command(command_name)
        if command:
            try:
                if arg:
                    await command(ctx, arg)
                else:
                    await command(ctx)
            except Exception as e:
                await ctx.send(f"Error running command `{command_name}`: {e}")
            
            if command_name in ['subnet', 'network']:
                global current_question, correct_answer
                if current_question:
                    await ctx.send("Game command test completed successfully. Stopping the game.")
                    await bot.get_command('stop_game')(ctx)
                    break

@test.error
async def test_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")

###########################################_Below this line_###########################################
###########################################_Work In Progress_##########################################

ROLE_EMOJI_MAP = {
    "🟢": None,  # Green emoji will correspond to a role
    "🔵": None,  # Blue emoji will correspond to a role
    "🔴": None,  # Red emoji will correspond to a role
}

def load_roles_and_map_emojis():
    if os.path.exists(ROLE_JSON_FILE):
        with open(ROLE_JSON_FILE, "r") as f:
            roles_data = json.load(f)
        role_names = [role for role in roles_data if role not in EXCLUDED_ROLES]
        for emoji, role_name in zip(ROLE_EMOJI_MAP.keys(), role_names):
            ROLE_EMOJI_MAP[emoji] = roles_data[role_name]

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_roles(ctx):
    load_roles_and_map_emojis()

    embed_description = "React with an emoji to receive the corresponding role:\n\n"
    for emoji, role_id in ROLE_EMOJI_MAP.items():
        if role_id:
            role_name = discord.utils.get(ctx.guild.roles, id=role_id).name
            embed_description += f"{emoji} - {role_name}\n"

    embed = discord.Embed(
        title="Choose Your Role!",
        description=embed_description,
        color=discord.Color.blue()
    )
    embed.set_footer(text="Click on an emoji to get a role assigned.")
    
    message = await ctx.send(embed=embed)
    for emoji in ROLE_EMOJI_MAP.keys():
        if ROLE_EMOJI_MAP[emoji]:
            await message.add_reaction(emoji)

@bot.event
async def on_raw_reaction_add(payload):
    MESSAGE_ID = 0
    if payload.message_id == MESSAGE_ID:
        guild = bot.get_guild(payload.guild_id)
        role_id = ROLE_EMOJI_MAP.get(str(payload.emoji))
        
        if role_id:
            role = guild.get_role(int(role_id))
            member = guild.get_member(payload.user_id)
            
            if role and member:
                await member.add_roles(role)
                try:
                    await member.send(f"You have been assigned the role: {role.name}")
                except discord.Forbidden:
                    pass

@bot.event
async def on_raw_reaction_remove(payload):
    MESSAGE_ID = 0
    if payload.message_id == MESSAGE_ID:
        guild = bot.get_guild(payload.guild_id)
        role_id = ROLE_EMOJI_MAP.get(str(payload.emoji))
        
        if role_id:
            role = guild.get_role(int(role_id))
            member = guild.get_member(payload.user_id)
            
            if role and member:
                await member.remove_roles(role)
                try:
                    await member.send(f"The role {role.name} has been removed from you.")
                except discord.Forbidden:
                    pass

###########################################_Run_Bot_###########################################
bot.run(botConfig._Bot_Token())
