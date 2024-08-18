import os
import discord
import sys
import subprocess
import asyncio
from discord.ext import commands
from urllib.request import urlopen
import botConfig  # Bot-token and Bot info exists locally on the server; this module contains that info.
import _Bot_Modul  # Module for various functions.
import _Subnet_Game  # Module for the Subnet game.

# Global version number variable
version_nr = "Current Version is 24/08/18.20"

# Setup for intents
intents = discord.Intents.all()
intents.message_content = True

# Initialize bot with command prefix "./"
bot = commands.Bot(command_prefix="./", intents=intents)

# Roles with access to "Sudo commands"
BOT_ADMIN_ROLE_NAME = "Bot-Master"

# A verification event to check if the bot is alive
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

###########################################_Below this line_##########################################
#############################################_All users_##############################################
###########################################_can run the code_#########################################

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
        "Ping": "./ping [IP_ADDRESS] - Perform a ping test to the specified IP address. Defaults to 8.8.8.8 if no IP is provided.",
        "RFC": "./rfc [NUMBER] - Retrieve information about the specified RFC number.",
        "Subnet Game": "./subnet - Start a subnetting quiz game. Use ./answer to submit your answer and ./stop_game to end the game.",
        "Network Game": "./start_game [subnet|network] - Start a network quiz game. Choose between 'subnet' and 'network'.",
        "BGP Setup": "./BGP_Setup [IP_ADDRESS] [AS_NUMBER] - Configure BGP peering with the given IP address and AS number.",
        "Reboot": "./Reboot - Perform a git pull and restart the bot. (Admin only)",
        "Add Role": "./addrole - Assign a specific role to the user. (Admin only)",
        "Remove Role": "./removerole - Remove a specific role from the user. (Admin only)",
        "Setup Roles": "./setup_roles - Create an embedded message for role assignment via reactions. (Admin only)"
    }
    
    for command, description in commands_list.items():
        embed.add_field(name=command, value=description, inline=False)
    
    await ctx.send(embed=embed)


@bot.command(name='start_game')
async def start_game_command(ctx, chosen_game):
    if chosen_game not in ['subnet', 'network']:
        await ctx.send("Invalid game type. Choose 'subnet' or 'network'.")
        return
    await _Subnet_Game.start_game(ctx, chosen_game)

@bot.command(name='stop_game')
async def stop_game_command(ctx):
    _Subnet_Game.reset_game()
    await ctx.send("The game has been stopped.")

@bot.command(name='answer')
async def answer_command(ctx, *, user_answer):
    if _Subnet_Game.check_answer(user_answer):
        await ctx.send("Correct! Well done.")
        _Subnet_Game.reset_game()
    else:
        await ctx.send("Incorrect. Try again.")

# Version Command
@bot.command()
async def version(ctx):
    await ctx.send(version_nr)

# Git Command
@bot.command()
async def git(ctx):
    await ctx.send('https://github.com/Walle-glitch/NIT-2.0.git')

# Hello Command
@bot.command()
async def hello(ctx):
    await ctx.send('Hello?')

# About Command
@bot.command()
async def about(ctx):
    reply = (
        "The NIT-BOT is a fun bot here on our Discord. It is public on GitHub and anyone is free to contribute to it, either for fun or other (non-malicious) projects. "
        "The server it is hosted on is at my home, so it is behind a normal (NAT Gateway). Contact Walle/Nicklas for more info. Use ./git for the link to the GitHub repo."
    )
    await ctx.send(reply)

# Ping Command
@bot.command()
async def ping(ctx, ip: str = "8.8.8.8"):
    """
    Performs a ping test to a given IP address. If no IP address is specified,
    it defaults to 8.8.8.8.
    """
    try:
        # Execute the ping command with a specified IP address (defaults to 8.8.8.8 if none is specified)
        result = subprocess.run(["ping", "-c", "4", ip], capture_output=True, text=True)
        
        # Sends the output of the ping command to the server
        await ctx.send(f"Ping results for {ip}:\n```\n{result.stdout}\n```")
    except subprocess.CalledProcessError as e:
        # If something goes wrong
        await ctx.send(f"ERROR:\n```\n{e.stderr}\n```")

# Get an RFC Command
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
    
    # Generate a new question and correct answer
    current_question, correct_answer = _Subnet_Game.generate_subnet_question()
    
    # Send the question to the user
    await ctx.send(f"Subnet question: {current_question}")

# Event to check the user's answer
@bot.event
async def on_message(message):
    global current_question, correct_answer
    
    # Check if the user is trying to answer a subnet question
    if current_question and message.author != bot.user:
        user_answer = message.content
        
        # Check if the answer is correct
        if _Subnet_Game.check_answer(user_answer):
            await message.channel.send("Correct answer! Well done!")
        else:
            await message.channel.send(f"Incorrect answer. The correct answer is: {correct_answer}")
        
        # Reset the question and answer
        current_question = None
        correct_answer = None
    
    # Allow other commands to be processed normally
    await bot.process_commands(message)

# BGP Setup Command Explanation
@bot.command()
async def BGP(ctx):
    reply = (
        'When using the ./BGP_Setup command, you need to provide two variables, like this: "./BGP_Setup [your IP address] [your AS number]". '
        'You will receive a reply with the needed info when the configuration is complete.'
    )
    await ctx.send(reply)

# Command to configure BGP peering
@bot.command()
async def BGP_Setup(ctx, neighbor_ip: str, neighbor_as: str):
    await ctx.send("Starting BGP configuration...")

    # Run BGP configuration and retrieve information
    gi0_ip, as_number = _Bot_Modul.configure_bgp_neighbor(neighbor_ip, neighbor_as)
    
    # Check if any error occurred during configuration
    if as_number is None:
        await ctx.send(f"An error occurred: {gi0_ip}")
    else:
        await ctx.send(f"BGP configuration complete. GigabitEthernet0/0 IP address: {gi0_ip}, AS number: {as_number}")

###########################################_Below this line_##########################################
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


# Test command.

@bot.command(name='test')
@commands.has_role(BOT_ADMIN_ROLE_NAME)  # Ensure only Bot-Master can run this command
async def test(ctx):
    """
    Tests all commands and outputs their results.
    """
    responses = []
    
    # Define a list of commands to test
    test_commands = [
        './version', './git', './hello', './about',
        './ping 8.8.8.8', './rfc 791', './subnet', './start_game subnet',
        './start_game network', './BGP_Setup 192.168.1.1 65001', './addrole',
        './removerole', './setup_roles'
    ]
    
    # Function to execute commands
    async def run_command(command):
        """Simulate running a command and collect its response."""
        try:
            # Invoke command and collect response
            ctx.message.content = command  # Mock the command message content
            await bot.process_commands(ctx.message)  # Process the command
            await asyncio.sleep(1)  # Wait a moment for the command to be processed
        except Exception as e:
            responses.append(f"Error with command `{command}`: {e}")

    # Run each command and gather responses
    for command in test_commands:
        await run_command(command)
        
        # Special handling for games
        if command.startswith('./start_game'):
            # If a game was started, provide a correct answer to end it
            responses.append(f"Testing game command `{command}`")
            await asyncio.sleep(2)  # Simulate waiting for game to start
            if command.endswith('subnet'):
                await run_command('./answer 255.255.255.0')
            elif command.endswith('network'):
                await run_command('./answer 192.168.1.0/24')
            # Stop game after testing
            await run_command('./stop_game')
    
    # Send collected responses
    response_text = "\n".join(responses)
    await ctx.send(f"Testing complete:\n{response_text}")

# Handle errors for the `./test` command
@test.error
async def test_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to use this command.")

###########_All_Code_Above_This_Line_#################

# Run the bot using its token
bot.run(botConfig._Bot_Token())
