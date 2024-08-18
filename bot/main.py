import os
import discord
import sys
import subprocess
import asyncio
from discord.ext import commands, tasks
from urllib.request import urlopen
import botConfig  # Bot-token and Bot info exists locally on the server; this module contains that info.
import _Bot_Modul # Module for various functions.
import _Subnet_Game # Module for the Subnet game.

# Global version number variable
version_nr = "Current Version is 24/08/18.15"

# Setup for intents
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="./", intents=intents)

# The following roles have access to "Sudo commands"
BOT_ADMIN_ROLE_NAME = "Bot-Master"

# Initialize global variables
current_question = None
correct_answer = None

# A verification event to check if the bot is alive
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

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
        "Ping": "./ping [IP_ADDRESS] - Perform a ping test to the specified IP address.",
        "RFC": "./rfc [NUMBER] - Retrieve information about the specified RFC number.",
        "Subnet Game": "./subnet - Start a subnetting quiz game.",
        "Network Game": "./network - Start a network quiz game.",
        "BGP Setup": "./BGP-Setup [IP_ADDRESS] [AS_NUMBER] - Configure BGP peering with the given IP address and AS number.",
        "Reboot": "./Reboot - Perform a git pull and restart the bot. (Admin only)",
        "Test": "./test - Test all commands. (Admin only)"
    }
    
    for command, description in commands_list.items():
        embed.add_field(name=command, value=description, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='start_game')
async def start_game_command(ctx, chosen_game):
    if chosen_game not in ['subnet', 'network']:
        await ctx.send("Invalid game type. Choose 'subnet' or 'network'.")
        return
    await start_game(ctx, chosen_game)

@bot.command(name='stop_game')
async def stop_game_command(ctx):
    reset_game()
    await ctx.send("The game has been stopped.")

@bot.command(name='answer')
async def answer_command(ctx, *, user_answer):
    if check_answer(user_answer):
        await ctx.send("Correct! Well done.")
        reset_game()
    else:
        await ctx.send("Incorrect. Try again.")

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

# Hello
@bot.command()
async def hello(ctx):
    Reply = 'Hello?'
    await ctx.send(Reply)

# About
@bot.command()
async def about(ctx):
    Reply = 'The NIT-BOT is a fun bot here on our Discord. It is public on GitHub and anyone is free to contribute to it, either for fun or other (non-malicious) projects. The server it is hosted on is at my home, so it is behind a normal (NAT Gateway). Contact Walle/Nicklas for more info. Use ./git for the link to the GitHub repo.'
    await ctx.send(Reply)

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

# Command to start a subnet game
@bot.command()
async def subnet(ctx):
    global current_question, correct_answer
    
    current_question, correct_answer = _Subnet_Game.generate_subnet_question()
    await ctx.send(f"Subnet question: {current_question}")

# Event to check the user's answer
@bot.event
async def on_message(message):
    global current_question, correct_answer
    
    if current_question and message.author != bot.user:
        user_answer = message.content
        
        if _Subnet_Game.check_answer(user_answer, correct_answer):
            await message.channel.send("Correct answer! Well done!")
            reset_game()
        else:
            await message.channel.send(f"Incorrect answer. The correct answer is: {correct_answer}")
        
        current_question = None
        correct_answer = None
    
    await bot.process_commands(message)

# BGP Setup Instructions
@bot.command()
async def BGP(ctx):
    Reply = 'When using the ./BGP_Setup command, you need to provide two variables, like this: "./BGP_Setup [your IP address] [your AS number]". You will receive a reply with the needed info when the configuration is complete.'
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

# Admin command to test all commands
@bot.command()
@commands.has_role(BOT_ADMIN_ROLE_NAME)
async def test(ctx):
    test_commands = [
        ("version", None),
        ("Reboot", None),
        ("h", None),
        ("git", None),
        ("hello", None),
        ("about", None),
        ("ping", "8.8.8.8"),
        ("rfc", "791"),
        ("subnet", None),
        ("BGP-Setup", "1.1.1.1 65000"),
        ("start_game", "subnet"),
        ("stop_game", None),
        ("start_game", "network"),
        ("stop_game", None),
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

# Run the bot using its token
bot.run(botConfig._Bot_Token())
