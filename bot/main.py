# This is Main.py The main File for the bot

###########################################_Import_Modules_##########################################

import os
import discord
import sys
import subprocess
import asyncio
from discord.ext import commands, tasks
from urllib.request import urlopen
import botConfig  # Bot-token and Bot info exists locally on the server; this module contains that info.
import _Bot_Modul # Module for various functions.
import _Games # Module for the games.
#import _Network_Tech_Game # Module for the Network Game.
#import _Subnet_Game # Module for the Subnet game.

###########################################_Bot_Set_Up_Stuff_##########################################

# Setup for intents
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="./", intents=intents)

# A verification event to check if the bot is alive
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

###########################################_Global_Variables_##########################################

# Global version number variable
version_nr = "Current Version is 24/08/25.1"

# The following roles have access to "Sudo commands"
BOT_ADMIN_ROLE_NAME = "Bot-Master"

# Initialize global variables
current_question = None
correct_answer = None

###########################################_All_User_Commands_##########################################

#############################_Utilities_Commands_#############################

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
        "Help": "./h - Display this help message.",
        "Version": "./version - Show the current bot version.",
        "Git Repository": "./git - Provide the link to the bot's GitHub repository.",
        "Hello": "./hello - Say hello to the bot.",
        "About": "./about - Information about the bot and its purpose.",
        "ticket": "./ticket - creates a new chanel to disscuss a speicif issue Use the comand ./close to close this chanel.",
        "Ping": "./ping [IP_ADDRESS] - Perform a ping test to the specified IP address.",
        "RFC": "./rfc [NUMBER] - Retrieve information about the specified RFC number.",
        "Network Games": "./start_game - Chose between Subnet and Network",
        "BGP Setup": "./BGP-Setup [IP_ADDRESS] [AS_NUMBER] - Configure BGP peering with the given IP address and AS number.",
        "Reboot": "./Reboot - Perform a git pull and restart the bot. (Admin only)",
        "Test": "./test - Test all commands. (Admin only)"
    }

    for command, description in commands_list.items():
        embed.add_field(name=command, value=description, inline=False)
    
    await ctx.send(embed=embed)

# Version Number
@bot.command()
async def version(ctx):
    Reply = version_nr
    await ctx.send(Reply)

# Git Repository
@bot.command()
async def git(ctx):
    Reply = 'https://github.com/Walle-glitch/NIT-2.0.git'
    await ctx.send(Reply)


# About
@bot.command()
async def about(ctx):
    Reply = (
    'The NIT-BOT is a fun bot here on our Discord.\n' 
    'It is public on GitHub and anyone is free to contribute to it,' 
    'either for fun or other (non-malicious) projects.\n' 
    'The server it is hosted on is at my home,' 
    'so it is behind a normal (NAT Gateway).\n'
    '\n' 
    'Contact Walle/Nicklas for more info.'
    'Use ./git for the link to the GitHub repo.\n'
    )
    await ctx.send(Reply)

# Ticket creation     

@bot.command(name="ticket")
async def create_ticket_command(ctx):
    guild = ctx.guild
    category_id = 1012026430470766816  # Replace with your actual category ID
    channel = await _Bot_Modul.create_ticket(guild, category_id, ctx.author)
    
    if channel:
        await ctx.send(f"Your ticket has been created: {channel.mention}")
    else:
        await ctx.send("Failed to create the ticket. Please contact an administrator.")

@bot.command(name="close")
async def close_ticket_command(ctx):
    # Close the channel where the command is invoked
    await _Bot_Modul.close_ticket(ctx.channel)
    await ctx.send("This ticket has been closed.")



#############################_User_Test_Commands_#############################

# Hello
@bot.command()
async def hello(ctx):
    Reply = 'Hello?'
    await ctx.send(Reply)

#############################_Game_Commands_#############################

# Command to start a subnet game
@bot.command()
async def subnet(ctx):
    global current_question, correct_answer
    
    current_question, correct_answer = _Games.generate_subnet_question()
    await ctx.send(f"Subnet question: {current_question}")

# Event to check the user's answer
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


#############################_Under Development_#############################

# Game Command  Not Working Yet! 

@bot.command(name='spel')
async def game_menu(ctx):
    menu_message = (
        "Welcome to the Game Menu! Please choose an option:\n"
        "1. Subnet Game\n"
        "2. Network Questions\n"
        "Type `1` for Subnet Game or `2` for Network Questions."
    )
    await ctx.send(menu_message)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == '1':
        await _Games.start_game(message.channel, 'subnet')
    elif message.content == '2':
        await _Games.start_game(message.channel, 'network')
    else:
        await bot.process_commands(message)
###

###
#############################_Network_Commands_#############################

# Ping
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


# BGP Setup Instructions
@bot.command()
async def BGP(ctx):
    Reply = (
        'When using the ./BGP_Setup command,\n' 
        'you need to provide two variables,\n'
        'like this: "./BGP_Setup [your IP address] [your AS number]".\n'
        'You will receive a reply with the needed info when the configuration is complete.'
        )
    await ctx.send(Reply)

# Command to configure BGP peering
@bot.command()
async def BGP_Setup(ctx, neighbor_ip: str, neighbor_as: str):
    await ctx.send("Starting BGP configuration...")
    gi0_ip, as_number = _Bot_Modul.configure_bgp_neighbor(neighbor_ip, neighbor_as)
    
    if as_number is None:
        await ctx.send(f"An error occurred: {gi0_ip}")
    else:
        await ctx.send(f"BGP configuration complete. GigabitEthernet0/0 IP address: {gi0_ip}, AS number: {as_number}")

#############################_Study_Commands_#############################

# Get an RFC
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
###########################################_Work In Progress_##########################################

# Role name to be assigned by the bot
ROLE_NAME = "YourRoleName"  # Change this to the role you want the bot to assign

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
    
    # Send an embedded message as a reply
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
    
    # Send an embedded message as a reply
    await ctx.send(embed=embed)

###########################################_Below this line_##########################################
###########################################_Only Admin Code_##########################################

# Command to perform a `git pull` and reboot the bot (only for the role "Bot-Master")
@bot.command(name="Reboot")
@commands.has_role(BOT_ADMIN_ROLE_NAME)  # Verify that the user has the correct role
async def reboot(ctx):
    await ctx.send("Performing `git pull` and restarting the bot...")

    # Execute "git pull" in the directory
    try:
        result = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
        await ctx.send(f"`git pull` executed:\n```\n{result.stdout}\n```")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"Error during `git pull`:\n```\n{e.stderr}\n```")
        return

    # Save the current Python executable
    python = sys.executable

    # Restart the Python script
    os.execl(python, python, *sys.argv)


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
            
            # If a game command was run, break after the first successful game answer
            if command_name in ['subnet', 'network']:
                global current_question, correct_answer
                if current_question:
                    await ctx.send("Game command test completed successfully. Stopping the game.")
                    await bot.get_command('stop_game')(ctx)
                    break

# Error handling for test command
@test.error
async def test_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")

###########################################_Below this line_###########################################
###########################################_Work In Progress_##########################################
###############################################_Admin_#################################################

# Manages errors if a non-"Bot-Master" tries the command
@reboot.error
async def reboot_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")

# Role IDs for roles to be assigned
ROLE_EMOJI_MAP = {
    "🟢": "Role1_ID",  # Green emoji corresponds to role 1
    "🔵": "Role2_ID",  # Blue emoji corresponds to role 2
    "🔴": "Role3_ID",  # Red emoji corresponds to role 3
}

# Command to create an embedded message with reaction roles
@bot.command()
@commands.has_permissions(administrator=True)  # Only administrators can run this command
async def setup_roles(ctx):
    """
    Creates an embedded message for role assignment via reactions.
    """
    embed = discord.Embed(
        title="Choose Your Role!",
        description="React with an emoji to receive the corresponding role:\n\n"
                    "🟢 - Green Role\n"
                    "🔵 - Blue Role\n"
                    "🔴 - Red Role\n",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Click on an emoji to get a role assigned.")
    
    # Send the embedded message
    message = await ctx.send(embed=embed)
    
    # Add reactions (emojis) to the message
    for emoji in ROLE_EMOJI_MAP.keys():
        await message.add_reaction(emoji)

# Event to listen for reactions and assign roles
@bot.event
async def on_raw_reaction_add(payload):
    """
    Event that handles role assignment when a user reacts to a message.
    """
    MESSAGE_ID = 0

    if payload.message_id == MESSAGE_ID:  # Replace this with the message ID of your embedded message
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
                    pass  # Ignore if the user has disabled direct messages

# Event to handle role removal when a user removes their reaction
@bot.event
async def on_raw_reaction_remove(payload):
    """
    Event that handles role removal when a user removes their reaction.
    """
    MESSAGE_ID = 0

    if payload.message_id == MESSAGE_ID:  # Replace this with the message ID of your embedded message
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
                    pass  # Ignore if the user has disabled direct messages


###########################################_Don_Not_Add_###########################################
##########################################_Anything_Below_#########################################
############################################_Here_=)_##############################################

# Run the bot using its token
bot.run(botConfig._Bot_Token())

#####################################################################################
########################################_END_########################################
#####################################################################################