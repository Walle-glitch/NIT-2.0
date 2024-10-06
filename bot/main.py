# This is Main.py, the main file for the bot

###########################################_Import_Modules_##########################################

import discord  # Main Discord library for building bots
from discord.ext import commands, tasks  # Commands and tasks extension for Discord
from datetime import datetime #, timedelta  # For handling date and time operations
import os  # For interacting with the operating system, like file paths
import sys  # System-specific parameters and functions
import subprocess  # For running system commands
import asyncio 
import importlib
from importlib import reload
import openai
import logging

# Local module imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'Internal_Modules'))
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

###########################################_Bot_Set_Up_Stuff_##########################################

intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

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
    
    # Handle XP data processing if file is empty
    try:
        if not xp_data:  # Ensure `xp_data` is defined
            await log_to_channel(bot, "Processing historical data, this may take a while...")
            await XP_Handler.process_historical_data(bot, XP_UPDATE_CHANNEL_ID)
            await log_to_channel(bot, "Finished processing historical data.")
            logger.info("Finished processing historical data.")
    except NameError:
        logger.error("xp_data is not defined")
    
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

##################_MODULE_RELOAD_COMMAND_##################

@bot.command()
@commands.has_role(_Bot_Config._Bot_Admin_Role_Name())  # Restrict to bot admin role
async def reload_module(ctx, module_name: str):
    """Reloads a specified module."""
    try:
        if module_name == "Activity_Tracking":
            reload(_Activity_Tracking)
            await ctx.send(f"{module_name} module has been reloaded.")
            logger.info(f"Module {module_name} reloaded.")
        else:
            await ctx.send("Module not found.")
            logger.warning(f"Module {module_name} not found for reloading.")
    except Exception as e:
        await ctx.send(f"Failed to reload {module_name}: {str(e)}")
        logger.error(f"Failed to reload {module_name}: {str(e)}")

###############

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

# Reload Game module command
@bot.command()
async def reload_game(ctx):
    """Reload the Game module without restarting the bot."""
    importlib.reload(_Game)
    await ctx.send("Game module reloaded successfully.")
    print("Game module reloaded.")

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
    if _Game.game_active:
        _Game.reset_game()
        await ctx.send("Game stopped.")
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

XP_UPDATE_CHANNEL_ID = _Bot_Config._XP_Update_Channel_ID()

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} is online.")
    update_roles.start()
    channel = bot.get_channel(XP_UPDATE_CHANNEL_ID)
    if channel:
        view = Role_Management.create_role_buttons_view()  # Create role buttons view
        await channel.send("Click the buttons to assign yourself a role:", view=view)  # Send buttons in the channel

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
async def on_message(message):
    """Handles incoming messages and tracks user activity."""
    await _Activity_Tracking.track_activity(message, bot)
    await bot.process_commands(message)

@bot.command()
@commands.has_role(_Bot_Config._Bot_Admin_Role_Name())  # Restrict to bot admin role
async def reload_module(ctx, module_name: str):
    """Reloads a specified module."""
    try:
        if module_name == "Activity_Tracking":
            reload(_Activity_Tracking)
            await ctx.send(f"{module_name} module has been reloaded.")
        else:
            await ctx.send("Module not found.")
    except Exception as e:
        await ctx.send(f"Failed to reload {module_name}: {str(e)}")

###########################################_Study_Plan_Loops_###########################################

CCIE_STUDY_CHANNEL_ID = _Bot_Config._CCIE_Study_Channel_ID()

@tasks.loop(hours=24)  # run every 24th H
async def weekly_study_plan_CCIE():
    # Kontrollera att det är söndag innan den postar veckans tips
    if datetime.now().weekday() == 6:  # Söndag (0 = Måndag, 6 = Söndag)
        try:
            await _Cisco_Study_Plans._CCIE_Study_Plan.post_weekly_goal_CCIE(bot, CCIE_STUDY_CHANNEL_ID)
        except Exception as e:
            await log_to_channel(bot, f"An error occurred during the CCIE study plan: {str(e)}")

CCNP_STUDY_CHANNEL_ID = _Bot_Config._CCNP_Study_Channel_ID()

@tasks.loop(hours=24)  # run every 24th H
async def weekly_study_plan_CCNP():
    # Kontrollera att det är söndag innan den postar veckans tips
    if datetime.now().weekday() == 6:  # Söndag (0 = Måndag, 6 = Söndag)
        try:
            await _Cisco_Study_Plans._CCNP_Study_Plan.post_weekly_goal_CCNP(bot, CCNP_STUDY_CHANNEL_ID)
        except Exception as e:
            await log_to_channel(bot, f"An error occurred during the CCNP study plan: {str(e)}")

CCNA_STUDY_CHANNEL_ID = _Bot_Config._CCNA_Study_Channel_ID()

@tasks.loop(hours=24)  # run every 24th H
async def weekly_study_plan_CCNA():
    # Kontrollera att det är söndag innan den postar veckans tips
    if datetime.now().weekday() == 6:  # Söndag (0 = Måndag, 6 = Söndag)
        try:
            await _Cisco_Study_Plans._CCNA_Study_Plan.post_weekly_goal_CCNA(bot, CCNA_STUDY_CHANNEL_ID)
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

XP_FILE = _Bot_Config._XP_File()  # File for storing all User XP
XP_UPDATE_CHANNEL_ID = _Bot_Config._XP_Update_Channel_ID()

# Load XP data and skip historical data processing if file has content
xp_data = XP_Handler.load_xp_data()

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    try:
        await XP_Handler.handle_xp(message, XP_UPDATE_CHANNEL_ID)
    except Exception as e:
        print(f"An error occurred while handling XP: {str(e)}")
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    try:
        await XP_Handler.handle_reaction_xp(reaction.message, XP_UPDATE_CHANNEL_ID)
    except Exception as e:
        print(f"An error occurred while handling reaction XP: {str(e)}")

# Command to show user's level and XP
@bot.command()
async def level(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    try:
        await XP_Handler.show_level(ctx, member)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


###########################################_Admin_Commands_###########################################
'''
Section below is for member moderation
'''

# Set the Admin Channel ID
_Member_Moderation.set_admin_channel_id(_Bot_Config._Admin_Channel_ID())

# Reload Member Moderation Module Command
@bot.command(name="reload_moderation")
async def reload_moderation_module(ctx):
    """Reloads the member moderation module."""
    importlib.reload(_Member_Moderation)
    await ctx.send("Member Moderation module reloaded successfully.")
    print("Member Moderation module reloaded.")

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