# This is Main.py, the main file for the bot

###########################################_Import_Modules_##########################################

import discord  # Main Discord library for building bots
from discord.ext import commands, tasks  # Commands and tasks extension for Discord
from datetime import datetime #, timedelta  # For handling date and time operations
import os  # For interacting with the operating system, like file paths
import sys  # System-specific parameters and functions
import subprocess  # For running system commands
import asyncio 
from importlib import reload
import openai
import logging
import random

# Local module imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'Internal_Modules'))
from _Cisco_Study_Plans import _CCNA_Study_Plan, _CCNP_Study_Plan, _CCIE_Study_Plan
import _Role_Management as Role_Management  # Importing role management module
import _XP_Handler as XP_Handler  # Import your module
import _Member_Moderation 
import _Game
import _Bot_Modul 
import _Cisco_Study_Plans 
import _Auction
import _Bot_Config # type: ignore
import _Slash_Commands
from _logging_setup import setup_logging
import _Activity_Tracking  # The activity tracking module

###########################################_Global_Variables_##########################################

version_nr = "Current Version is 24/10/06.1M"

###########################################_Logging_Setup_##############################################

setup_logging()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename=f'logs/log-{datetime.now().strftime("%Y-%m-%d")}.txt',
                    format='%(asctime)s %(levelname)s: %(message)s')

###########################################_Bot_Set_Up_Stuff_##########################################

intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True
intents.messages = True
intents.presences = True  # Aktivera för att kunna spåra statusändringar

bot = commands.Bot(command_prefix="!", intents=intents)

##################_XP_DATA_##################

XP_FILE = _Bot_Config._XP_File()  # File for storing all User XP
XP_UPDATE_CHANNEL_ID = _Bot_Config._XP_Update_Channel_ID()

# Load XP data and skip historical data processing if file has content
xp_data = XP_Handler.load_xp_data()

##################_LOG_TO_CHANNEL_##################

LOG_CHANNEL_ID = _Bot_Config._Log_Channel_ID()

async def log_to_channel(bot, message):
    """Log messages to a specified Discord channel."""
    print(message)  # Print to server logs for safety
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel is None:
        logger.error(f"Log channel with ID {LOG_CHANNEL_ID} not found.")
        return
    try:
        await log_channel.send(message)
    except Exception as e:
        logger.error(f"Failed to send log to channel: {str(e)}")

##################_BOT_BOOT_##################

@bot.event
async def on_ready():
    """Called when the bot is ready and logged in."""
    await log_to_channel(bot, f'Logged in as {bot.user}')
    logger.info("Bot logged in")
    
    try:
        await bot.tree.sync()  # Sync global application commands
        await log_to_channel(bot, "Global commands synced.")
        logger.info("Global commands synced.")
    except Exception as e:
        await log_to_channel(bot, f"Failed to sync commands: {str(e)}")
        logger.error(f"Failed to sync commands: {str(e)}")
    
    # Start study plans
    weekly_study_plan_CCIE.start()
    weekly_study_plan_CCNP.start()
    weekly_study_plan_CCNA.start()
    await log_to_channel(bot, "Study plans active.")
    logger.info("Study plans active.")
    
    # Setup activity tracking file
    _Activity_Tracking.setup_file()

    # Ask the user whether to process historical data
    await log_to_channel(bot, "Do you want to process historical data? Respond with 'yes' or 'no' in the log channel.")
    try:
        def check(m):
            return m.author != bot.user and m.channel.id == LOG_CHANNEL_ID and m.content.lower() in ["yes", "no"]

        msg = await bot.wait_for('message', check=check, timeout=60.0)  # Wait for 60 seconds
        if msg.content.lower() == "yes":
            await log_to_channel(bot, "Processing historical data, this may take a while...")
            await XP_Handler.process_historical_data(bot, XP_UPDATE_CHANNEL_ID)
            await log_to_channel(bot, "Finished processing historical data.")
            logger.info("Finished processing historical data.")
        else:
            await log_to_channel(bot, "Skipping historical data processing.")
            logger.info("Skipping historical data processing.")
    except TimeoutError:
        await log_to_channel(bot, "No response received. Skipping historical data processing.")
        logger.info("Timeout waiting for user input. Skipping historical data processing.")

    # Start role management tasks
    update_roles.start()
    await log_to_channel(bot, "Roles active.")
    await log_to_channel(bot, "All boot events completed.")
    logger.info("All boot events completed.")

# Load module that contain bot Slash commands
_Slash_Commands.setup(bot)

##################_EVENT_HANDLERS_##################

@bot.event
async def on_message(message):
    """Logs incoming messages and processes commands."""
    if message.author.bot:
        return  # Ignore bot messages
    logger.info(f"Incoming message from {message.author}: {message.content}")
    await bot.process_commands(message)

@bot.event
async def on_command(ctx):
    """Logs every command execution."""
    logger.info(f"User {ctx.author} executed command: {ctx.command}")

@bot.event
async def on_command_error(ctx, error):
    """Logs any command errors."""
    logger.error(f"Error with command {ctx.command}: {error}")

###############
''' 
Module Reloding function
'''
# Create a dictionary mapping module names to their imports
modules = {
    "Role_Management": Role_Management,
    "XP_Handler": XP_Handler,
    "Member_Moderation": _Member_Moderation,
    "Game": _Game,
    "Bot_Modul": _Bot_Modul,
    "Cisco_Study_Plans": _Cisco_Study_Plans,
    "Auction": _Auction,
    "Slash_Commands": _Slash_Commands,
    "Activity_Tracking": _Activity_Tracking,
    "logging_setup": setup_logging
}

@bot.command()
@commands.has_role(_Bot_Config._Bot_Admin_Role_Name())  # Restrict to bot admin role
async def reload_module(ctx, module_name: str = None):
    """Reloads a specified module. If no argument is provided, lists all available modules."""
    try:
        if module_name is None:
            # List all available modules if no module name is provided
            available_modules = ', '.join(modules.keys())
            await ctx.send(f"Available modules: {available_modules}")
        elif module_name in modules:
            # Reload the specified module
            reload(modules[module_name])
            await ctx.send(f"Module '{module_name}' has been reloaded.")
            logger.info(f"Module '{module_name}' reloaded.")
        else:
            await ctx.send(f"Module '{module_name}' not found. Use the command without arguments to list available modules.")
            logger.warning(f"Module '{module_name}' not found.")
    except Exception as e:
        await ctx.send(f"Failed to reload module '{module_name}': {str(e)}")
        logger.error(f"Failed to reload module '{module_name}': {str(e)}")

''''
Auction Command
Lets users set up an acution for there no longer needed stuff. 

Still has some issues to figure out. //2024.10.05
'''

# Sell command to start an auction
@bot.command(name="Sell")
async def sell(ctx, item_name: str = None, start_price: int = None, buy_now_price: int = None, days_duration: int = None):
    if not all([item_name, start_price, buy_now_price, days_duration]):
        await ctx.send("Error: Please provide all required parameters: `!Sell <item_name> <start_price> <buy_now_price> <days_duration>`.")
        return
    
    channel = ctx.channel
    user = ctx.author

    # Call the auction creation function from Internal_Modules._auction
    await _Auction.create_auction(channel, user, item_name, start_price, buy_now_price, days_duration)

# Load auctions when bot starts
_Auction.load_auctions()

''''
Resource Command
Lets students collect the varius information and tips for diferent resourses. 
'''

@bot.command(name="r")
async def resuser_command(ctx):
    try:
        await _Bot_Modul.send_resource_embed(ctx)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

''''
Version section
'''
@bot.command()
async def version(ctx):
    try:
        await ctx.send(version_nr)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
''''
about section
Just for fun, Like a user test command
'''

@bot.command()
async def about(ctx):
    try:
        reply = (
            'The NIT-BOT is a fun bot here on our Discord.\n' 
            'It is public on GitHub and anyone is free to contribute to it,' 
            'either for fun or other (non-malicious) projects.\n' 
            'The server it is hosted on is at my home,' 
            'so it is behind a normal NAT Gateway.\n'
            '\n' 
            'Contact Walle/Nicklas for more info.'
            'https://github.com/Walle-glitch/NIT-2.0.git\n'
        )
        await ctx.send(reply)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

''''
Ping section Start
Just for fun, Like a user test command
'''

@bot.command() # Performs a ping test to a given IP address. If no IP address is specified. it defaults to 8.8.8.8.
async def ping(ctx, ip: str = "8.8.8.8"):
    try:
        result = subprocess.run(["ping", "-c", "4", ip], capture_output=True, text=True)
        await ctx.send(f"Ping results for {ip}:\n```\n{result.stdout}\n```")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"ERROR:\n```\n{e.stderr}\n```")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


@bot.command() 
async def hack(ctx, ip: str = "8.8.8.8"):
    try:
        result = subprocess.run(["ping", "-c", "4", ip], capture_output=True, text=True)
        await ctx.send(f"Ping results for {ip}:\n```\n{result.stdout}\n```")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"ERROR:\n```\n{e.stderr}\n```")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command()
async def hack(ctx, target: str = "8.8.8.8"):
    await ctx.send(f"Starting Nmap scan on {target}...")
    
    try:
        # Run Nmap scan
        result = subprocess.run(["nmap", target], capture_output=True, text=True)
        await ctx.send(f"Nmap scan results for {target}:\n```\n{result.stdout}\n```")
        
        # Simulate the fake exploit process
        await asyncio.sleep(10)
        await ctx.send("Exploit found!")
        
        await asyncio.sleep(2)
        await ctx.send("Analyzing...")
        
        await asyncio.sleep(1)
        await ctx.send("Generating script...")
        
        await asyncio.sleep(5)
        await ctx.send("Starting hacking sequence...")

        # Simulate the hacking progress
        for i in range(10):
            progress = random.randint(0, 100)
            await ctx.send(f"Hacking progress: {progress}%")
            await asyncio.sleep(1)

        # Fake interactive prompt
        await ctx.send(f"Interactive prompt: `root@{target}:~#`")

        # Wait for user input
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            user_input = await bot.wait_for('message', check=check, timeout=15)
            await ctx.send(f"Connection to {target} lost: {user_input.content}\nReason: Connection aborted.")
        except asyncio.TimeoutError:
            await ctx.send(f"Connection to {target} lost: No input detected.\nReason: Timeout.")

    except subprocess.CalledProcessError as e:
        await ctx.send(f"Error during Nmap scan:\n```\n{e.stderr}\n```")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")



''''
AI section START
    Sends a question to ChatGPT and returns the response.
    
    :param question: The user's question to ChatGPT.
    :param conversation_history: The conversation history to maintain context.
    :return: The response from ChatGPT or an error message if something goes wrong.
'''

# Set your OpenAI API key here
openai.api_key = _Bot_Config._Open_AI_Token()

# Maximum tokens per response and max questions per session
MAX_TOKENS = 150
MAX_QUESTIONS_PER_SESSION = 5

async def ask_chatgpt(question, conversation_history):

    try:
        # Add user's question to the conversation history
        conversation_history.append({"role": "user", "content": question})

        # Call the OpenAI API to get a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use another model if preferred
            messages=conversation_history,
            max_tokens=MAX_TOKENS  # Limit the number of tokens in the response
        )
        
        # Extract the answer and add it to the conversation history
        answer = response['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": answer})

        return answer
    except Exception as e:
        return f"An error occurred: {str(e)}"

async def handle_ai_session(ctx, initial_question):

    # Handles a session where the user can interact with ChatGPT.
    # :param ctx: The context in which the command was invoked.
    # :param initial_question: The initial question the user asked.
   
    user_id = ctx.author.id
    conversation_history = []
    questions_asked = 0  # Counter for the number of questions in the session

    # Ask the initial question
    answer = await ask_chatgpt(initial_question, conversation_history)
    await ctx.send(answer)
    questions_asked += 1

    # Wait for follow-up questions
    while questions_asked < MAX_QUESTIONS_PER_SESSION:
        try:
            # Wait for the next message from the user
            message = await ctx.bot.wait_for('message', check=lambda m: m.author.id == user_id, timeout=300)
            
            # End session if the user sends the stop command
            if message.content.strip().lower() == "/ai-stop":
                await ctx.send("AI session ended.")
                break

            # Handle the next question and increment the counter
            answer = await ask_chatgpt(message.content, conversation_history)
            await message.channel.send(answer)
            questions_asked += 1

        except asyncio.TimeoutError:
            await ctx.send("AI session ended due to inactivity.")
            break

@bot.command(name="AI")
async def ai_command(ctx, *, question=None):
    try:
        if question is None:
            await ctx.send("Please provide a question after the command: `!AI \"Question\"`")
            return
        
        await handle_ai_session(ctx, question)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

''''
Game section Start
# This section implements a continuous Q&A game with subnet and network modes.
# Game state is tracked to allow multiple rounds until manually stopped or a timeout occurs.
# Subnet questions are generated dynamically, while network questions are loaded from a JSON file.
# User answers are processed with real-time feedback, and the game state is reset after stop or timeout.
# Extensive logging is used for tracking and debugging game events and user interactions.
'''

# Start game command
@bot.command()
async def game(ctx):
    """Starts the game and prompts the user to choose a mode."""
    view = discord.ui.View()

    subnet_button = discord.ui.Button(label="Subnet", style=discord.ButtonStyle.primary)
    network_button = discord.ui.Button(label="Network Questions", style=discord.ButtonStyle.secondary)

    async def subnet_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await _Game.start_game(ctx, 'subnet', bot)

    async def network_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await _Game.start_game(ctx, 'network', bot)

    subnet_button.callback = subnet_callback
    network_button.callback = network_callback

    view.add_item(subnet_button)
    view.add_item(network_button)

    await ctx.send("Choose a game mode:", view=view)

# Stop game command
@bot.command()
async def game_stop(ctx):
    """Command to stop the game."""
    if _Game.game_active and ctx.author == _Game.game_initiator:
        _Game.reset_game()
        await ctx.send("Game stopped.")
    elif ctx.author != _Game.game_initiator and _Game.game_active == True:
        await ctx.send(f"Game can only be stoped by {_Game.game_initiator}")
    else:
        await ctx.send("No game is currently running.")
        
'''
GET an RFC section: 
 
    Retrieves and displays information about an RFC based on the number.
    :param rfc_number: RFC number to fetch. If none is provided, an error message is displayed.
'''

@bot.command()
async def rfc(ctx, rfc_number: str = None):
    try:
        if rfc_number is None:
            await ctx.send("Error: No RFC number provided. Please provide an RFC number after the command.")
            return
        try:
            rfc_number = int(rfc_number)
            result = _Bot_Modul.get_rfc(rfc_number)
        except ValueError:
            result = "Error: Invalid RFC number. Please provide a valid integer."
        await ctx.send(result)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

'''
Role managment section:
'''

# Task to periodically update roles
@tasks.loop(hours=1)
async def update_roles():
    try:    
        await Role_Management.fetch_and_save_roles(bot)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Command to assign a role
@bot.command()
async def addrole(ctx, role_name: str = None):
    """Command to add a role to the user."""
    if role_name is None:
        roles = Role_Management.load_roles()
        available_roles = [role for role in roles.keys() if role not in Role_Management.EXCLUDED_ROLES]
        
        if not available_roles:
            await ctx.send("No roles available for assignment.")
            return
        
        embed = discord.Embed(title="Available Roles", description="Here are the roles you can assign:", color=discord.Color.blue())
        for role in available_roles:
            embed.add_field(name=f'"{role}"', value=f'Assign with `!addrole "{role}"`', inline=False)
        
        await ctx.send(embed=embed)
        return

    await Role_Management.assign_role(ctx, role_name)

# Command to remove a role
@bot.command()
async def removerole(ctx, role_name: str = None):
    """Command to remove a role from the user."""
    if role_name is None:
        roles = Role_Management.load_roles()
        available_roles = [role for role in roles.keys() if role not in Role_Management.EXCLUDED_ROLES]

        if not available_roles:
            await ctx.send("No roles available for removal.")
            return
        
        embed = discord.Embed(title="Available Roles", description="Here are the roles you can remove:", color=discord.Color.blue())
        for role in available_roles:
            embed.add_field(name=role, value=f'Remove with `!removerole "{role}"`', inline=False)
        
        await ctx.send(embed=embed)
        return

    await Role_Management.remove_role(ctx, role_name)

'''
#LateNightCrew role assignment. 
'''
@bot.event
async def on_member_update(before, after):
    """Track user status and manage LateNightCrew role with debug logging."""
    
    # Check if the status has changed
    if before.status != after.status:
        logger.debug(f"Status update: {after.name} changed from {before.status} to {after.status}")

        # Attempt to track activity
        try:
            logger.debug(f"Tracking activity for {after.name}")
            await _Activity_Tracking.track_activity(before, after, bot)
        except Exception as e:
            logger.error(f"Error tracking activity: {str(e)}")

    # Always log that the event has been processed
    logger.debug(f"Member update event processed for {after.name}")

    # Make sure to continue processing other bot commands
    await bot.process_commands(after)

###########################################_Study_Plan_Loops_###########################################

CCIE_STUDY_CHANNEL_ID = _Bot_Config._CCIE_Study_Channel_ID()
CCNP_STUDY_CHANNEL_ID = _Bot_Config._CCNP_Study_Channel_ID()
CCNA_STUDY_CHANNEL_ID = _Bot_Config._CCNA_Study_Channel_ID()

@tasks.loop(hours=24)  # run every 24th H
async def weekly_study_plan_CCIE():
    if datetime.now().weekday() == 6:  # Check if it's Sunday
        try:
            await _CCIE_Study_Plan.post_weekly_goal(bot, CCIE_STUDY_CHANNEL_ID)
        except Exception as e:
            await log_to_channel(bot, f"An error occurred during the CCIE study plan: {str(e)}")

@tasks.loop(hours=24)  # run every 24 hours
async def weekly_study_plan_CCNP():
    if datetime.now().weekday() == 6:  # Sunday
        try:
            logger.info("Fetching CCNP study plan...")
            await _CCNP_Study_Plan.post_weekly_goal(bot, CCNP_STUDY_CHANNEL_ID)
        except Exception as e:
            await log_to_channel(bot, f"An error occurred during the CCNP study plan: {str(e)}")
            logger.error(f"An error occurred during the CCNP study plan: {str(e)}")

@tasks.loop(hours=24)  # run every 24th H
async def weekly_study_plan_CCNA():
    if datetime.now().weekday() == 6:  # Check if it's Sunday
        try:
            await _CCNA_Study_Plan.post_weekly_goal(bot, CCNA_STUDY_CHANNEL_ID)
        except Exception as e:
            await log_to_channel(bot, f"An error occurred during the CCNA study plan: {str(e)}")

# Command to manually fetch and post jobs

JOB_CHANNEL_ID = _Bot_Config._Job_Channel_ID()

@bot.command()
async def post_jobs(ctx):
    try:
        await _Bot_Modul.fetch_and_post_jobs(bot, JOB_CHANNEL_ID)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@tasks.loop(hours=24)  # Job posting loop (daily)
async def job_posting_loop():
    try:
        await _Bot_Modul.fetch_and_post_jobs(bot, JOB_CHANNEL_ID)
    except Exception as e:
        await log_to_channel(bot, f"An error occurred during job posting: {str(e)}")

####################################################

# Boot Logic on top of file 

XP_UPDATE_CHANNEL_ID = _Bot_Config._XP_Update_Channel_ID()

@bot.event
async def on_message(message):
    """Triggered whenever a message is sent in a text channel."""
    if message.author.bot:
        return  # Ignore bot messages

    try:
        # Handle XP and LateNightCrew role management
        await XP_Handler.handle_xp(message, XP_UPDATE_CHANNEL_ID)
        print(f"XP handled for {message.author.name}")
    except Exception as e:
        print(f"An error occurred while handling XP: {str(e)}")

    # Ensure bot commands are processed
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    """Triggered whenever a reaction is added to a message."""
    if user.bot:
        return  # Ignore bot reactions

    try:
        # Handle XP for reactions and LateNightCrew role management
        await XP_Handler.handle_reaction_xp(reaction.message, XP_UPDATE_CHANNEL_ID)
        print(f"Reaction XP handled for {user.name}")
    except Exception as e:
        print(f"An error occurred while handling reaction XP: {str(e)}")

@bot.command()
async def level(ctx, member: discord.Member = None):
    """Command to check a user's level and XP."""
    if member is None:
        member = ctx.author  # Default to the command author if no member is specified
    
    try:
        await XP_Handler.show_level(ctx, member)
        print(f"Level command processed for {member.name}")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

###########################################_Admin_Commands_###########################################
'''
Section below is for member moderation
'''

# Set the Admin Channel ID
_Member_Moderation.set_admin_channel_id(_Bot_Config._Admin_Channel_ID())

# Kick Command
@bot.command(name="kick")
@commands.check(_Member_Moderation.has_privileged_role)
@commands.has_permissions(kick_members=True)
async def kick_command(ctx, user: discord.Member, *, reason=None):
    try:
        await _Member_Moderation.kick_user(ctx, user, reason)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Ban Command
@bot.command(name="ban")
@commands.check(_Member_Moderation.has_privileged_role)
@commands.has_permissions(ban_members=True)
async def ban_command(ctx, user: discord.Member, *, reason=None):
    try:
        await _Member_Moderation.ban_user(ctx, user, reason)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Mute Command
@bot.command(name="mute")
@commands.check(_Member_Moderation.has_privileged_role)
@commands.has_permissions(moderate_members=True)
async def mute_command(ctx, duration: int, user: discord.Member, *, reason=None):
    try:
        await _Member_Moderation.mute_user(ctx, user, duration, reason)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

'''
Mantinence Commandes Only for Bot admin ! 
'''

BOT_ADMIN_ROLE_NAME = _Bot_Config._Bot_Admin_Role_Name()

@bot.command()
@commands.has_role(_Bot_Config._Bot_Admin_Role_Name())  # Restrict to bot admin role
async def git_pull(ctx):
    """Executes git pull on the server."""
    try:
        # Execute the git pull command
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True, check=True)
        
        # Send the output back to the Discord channel
        await ctx.send(f"Git pull successful:\n```\n{result.stdout}\n```")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"Git pull failed:\n```\n{e.stderr}\n```")
    except Exception as e:
        await ctx.send(f"An error occurred while trying to perform git pull: {str(e)}")

# Reboot Command
@bot.command(name="Reboot")
@commands.has_role(BOT_ADMIN_ROLE_NAME)
async def reboot(ctx):
    try:
        await ctx.send("Performing `git pull` and restarting the bot...")
        result = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
        await ctx.send(f"`git pull` executed:\n```\n{result.stdout}\n```")
        python = sys.executable
        os.execl(python, python, *sys.argv)
    except subprocess.CalledProcessError as e:
        await ctx.send(f"Error during `git pull`:\n```\n{e.stderr}\n```")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

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
        ("hello", None),
        ("about", None),
        ("ping", "8.8.8.8"),
        ("rfc", "791"),
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

##################################_NO_CODE_BELOW_THIS_LINE_####################################
###########################################_Run_Bot_###########################################
if __name__ == "__main__":
    bot.run(_Bot_Config._Bot_Token())
#############################################_END_#############################################