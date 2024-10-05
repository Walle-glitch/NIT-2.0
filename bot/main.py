# This is Main.py, the main file for the bot

###########################################_Import_Modules_##########################################

import discord  # Main Discord library for building bots
from discord.ext import commands, tasks  # Commands and tasks extension for Discord
from discord.ui import Button, View
from datetime import datetime #, timedelta  # For handling date and time operations
import json  # For handling JSON data
import os  # For interacting with the operating system, like file paths
import sys  # System-specific parameters and functions
import subprocess  # For running system commands
import asyncio 
import ipaddress
import random

sys.path.append(os.path.join(os.path.dirname(__file__), 'Internal_Modules'))

import _Bot_Modul
import _Open_AI
import _CCIE_Study_Plan
import _CCNP_Study_Plan
import _CCNA_Study_Plan
import _Auction
import _Bot_Config # type: ignore
import _Slash_Commands
from _logging_setup import setup_logging
from _activity_tracker import setup_file, track_activity

###########################################_Global_Variables_##########################################

version_nr = "Current Version is 24/10/05.1"  # Global version number variable

# Roles with access 
BOT_ADMIN_ROLE_NAME = _Bot_Config._Bot_Admin_Role_Name()
ADMIN_ROLE_NAME =  _Bot_Config._Admin_Role_Name()
MOD_ROLE_NAME = _Bot_Config._Mod_Role_Name()
MENTOR_ROLE = _Bot_Config._Mentor_Role_Name()

# Definiera roller som kräver lösenord
PASSWORD_PROTECTED_ROLES = _Bot_Config._protected_Poles()

# Channel IDs
XP_UPDATE_CHANNEL_ID = _Bot_Config._XP_Update_Channel_ID()
JOB_CHANNEL_ID = _Bot_Config._Job_Channel_ID()
CCIE_STUDY_CHANNEL_ID = _Bot_Config._CCIE_Study_Channel_ID()
CCNP_STUDY_CHANNEL_ID = _Bot_Config._CCNP_Study_Channel_ID()
CCNA_STUDY_CHANNEL_ID = _Bot_Config._CCNA_Study_Channel_ID()
WELCOME_CHANNEL_ID = _Bot_Config._Welcome_Channel_ID()
LOG_CHANNEL_ID = _Bot_Config._Log_Channel_ID()
TICKET_CATEGORY_ID = _Bot_Config._Ticket_Category_ID()
GEN_CHANNEL_ID = _Bot_Config._Gen_Channel_ID()
YOUTUBE_CHANNEL_ID = _Bot_Config._YouTube_Channel_ID()
PODCAST_CHANNEL_ID = _Bot_Config._Podcast_Channel_ID()

# File Management 
ROLE_JSON_FILE = _Bot_Config._Role_Json_File() # File where roles are stored
EXCLUDED_ROLES = _Bot_Config._Excluded_Roles() # Roles that cannot be assigned via reactions
ACTIVE_USERS_FILE = _Bot_Config._ACTIVE_USERS_FILE()

###########################################_Bot_Set_Up_Stuff_##########################################

intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True  # Enable reaction events
intents.guilds = True  # Access to server information, including roles
intents.members = True  # Access to members for role assignment
intents.messages = True
# Sätt upp loggern
logger = setup_logging()

bot = commands.Bot(command_prefix="!", intents=intents) # Command Prefix 

# Kör setup för filer
setup_file()

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

# Load module that contain bot Slash commands
_Slash_Commands.setup(bot)

@bot.event
async def on_ready():
    await log_to_channel(bot, f'Logged in as {bot.user}')
    await bot.tree.sync() # Synchronize global application commands
    await log_to_channel(bot, "Global commands synced.") 
    weekly_study_plan_CCIE.start()  
    weekly_study_plan_CCNP.start()
    weekly_study_plan_CCNA.start()
    await log_to_channel(bot, "Study plans active")
    # setup_rich_presence()  # Try setting up Rich Presence
    await log_to_channel(bot, "Processing historical data, notifications are disabled. This Will take a while...") # Disable notifications for historical data processing
    await _Bot_Modul.process_historical_data(bot, XP_UPDATE_CHANNEL_ID)
    await log_to_channel(bot, "Finished processing historical data, notifications are now enabled.") # Re-enable notifications after processing is done
    # Start scheduled tasks when the bot is ready
    update_roles.start()
    await log_to_channel(bot, "Roles active")
    check_welcome_message.start()
    # Find a specific channel to post the welcome message or ensure it's updated
    await log_to_channel(bot, "All Boot Events are now completed") # Re-enable notifications after processing is done

@bot.event
async def on_message(message):
    # Logga alla inkommande meddelanden
    if message.author.bot:
        return  # Vi vill inte logga botens egna meddelanden

    logger.info(f"Inkommande meddelande från {message.author}: {message.content}")
    
    # Processera kommandon om meddelandet är ett kommando
    await bot.process_commands(message)

@bot.event
async def on_command(ctx):
    # Logga varje gång ett kommando körs
    logger.info(f"Användare {ctx.author} körde kommandot: {ctx.command}")

@bot.event
async def on_command_error(ctx, error):
    # Logga alla fel som inträffar med kommandon
    logger.error(f"Ett fel inträffade med kommandot {ctx.command}: {error}")

@bot.event
async def on_message(message):
    """Hantera inkommande meddelanden och spåra aktivitet"""
    await track_activity(message, bot)
    await bot.process_commands(message)

###########################################_All_User_Commands_##########################################
#############################_Utilities_Commands_#############################

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

# Resource command
@bot.command(name="r")
async def resuser_command(ctx):
    try:
        await _Bot_Modul.send_resource_embed(ctx)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Version Command
@bot.command()
async def version(ctx):
    try:
        await ctx.send(version_nr)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# About Command
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

#############################_Open_AI_Commands_#############################

@bot.command(name="AI")
async def ai_command(ctx, *, question=None):
    try:
        if question is None:
            await ctx.send("Please provide a question after the command: `!AI \"Question\"`")
            return
        
        await _Open_AI.handle_ai_session(ctx, question)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

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
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

#############################_Study_Commands_#############################

# Global variables for game management
game_task = None
game_initiator = None
current_question = None
correct_answer = None
current_game_type = None
question_timeout_task = None

# Load JSON data for questions and user scores
QUESTION_FILE = "questions.json"  # Adjust the file path
SCORE_FILE = "scores.json"  # Adjust the file path

def load_network_questions():
    """Loads network questions from the JSON file."""
    if os.path.exists(QUESTION_FILE):
        with open(QUESTION_FILE, "r") as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"{QUESTION_FILE} not found!")

def load_user_scores():
    """Loads user scores from the JSON file."""
    if not os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "w") as f:
            json.dump({}, f)  # Create an empty JSON file
    with open(SCORE_FILE, "r") as f:
        return json.load(f)

def save_user_scores(scores):
    """Saves the updated user scores to the JSON file."""
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f, indent=4)

def generate_subnet_question():
    """Generates a random subnet-related question."""
    ip = ipaddress.IPv4Address(random.randint(0, 2**32 - 1))
    prefix_length = random.randint(16, 30)
    network = ipaddress.IPv4Network(f"{ip}/{prefix_length}", strict=False)
    
    question_type = random.choice(["network", "broadcast", "hosts"])
    
    if question_type == "network":
        question = f"What is the network address for {network}?"
        correct_answer = str(network.network_address)
    elif question_type == "broadcast":
        question = f"What is the broadcast address for {network}?"
        correct_answer = str(network.broadcast_address)
    else:
        question = f"How many hosts can be in the subnet {network}?"
        correct_answer = str(network.num_addresses - 2)  # Subtract network and broadcast addresses
    
    return question, correct_answer

def generate_network_question():
    """Generates a random network-related question from the loaded JSON file."""
    questions = load_network_questions()
    question_data = random.choice(questions)
    question = question_data["question"]
    options = question_data["options"]
    correct_index = question_data["correct_option_index"]
    return question, options, correct_index

def check_subnet_answer(user_answer, correct_answer):
    """Checks if the user's answer for subnet question is correct."""
    return user_answer.strip() == correct_answer

def check_network_answer(selected_option_index, correct_option_index):
    """Checks if the selected answer for network question is correct."""
    return selected_option_index == correct_option_index

async def start_game(ctx, game_type):
    """Starts a game based on the selected game type."""
    global current_question, correct_answer, current_game_type, game_initiator, game_task

    if game_task and not game_task.done():
        await ctx.send("A game is already in progress. Please finish it first.")
        return

    game_initiator = ctx.author  # Track the user who started the game
    current_game_type = game_type

    if game_type == 'subnet':
        current_question, correct_answer = generate_subnet_question()
        await ctx.send(f"Subnet question: {current_question}")
    elif game_type == 'network':
        question, options, correct_index = generate_network_question()
        options_str = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
        current_question = f"{question}\n\n{options_str}"
        correct_answer = correct_index  # Store the correct answer index
        await ctx.send(f"Network question:\n{current_question}")
    
    game_task = asyncio.create_task(run_game(ctx))

async def run_game(ctx):
    """Runs the game loop until the user stops it with !game_stop or after 5 minutes of inactivity."""
    global question_timeout_task

    while True:
        question_timeout_task = asyncio.create_task(question_timeout(ctx))
        try:
            await question_timeout_task
        except asyncio.CancelledError:
            pass  # Timeout task was cancelled, continue to the next question

async def question_timeout(ctx):
    """Stops the game after 5 minutes of inactivity."""
    await asyncio.sleep(300)  # 5 minutes timeout
    await ctx.send("Game ended due to inactivity.")
    reset_game()

async def process_answer(message):
    """Processes the answer from the game initiator only."""
    global current_question, correct_answer, current_game_type, game_initiator

    if message.author != game_initiator:
        return  # Ignore messages from users who didn't start the game

    if current_question is None or current_game_type is None:
        return

    # Handle Subnet question
    if current_game_type == 'subnet':
        if check_subnet_answer(message.content, correct_answer):
            await message.channel.send(f"Correct! The answer is {correct_answer}.")
            await show_score_comparison(message.channel, message.author.id, 10)  # 10 points for correct answer
        else:
            await message.channel.send(f"Wrong answer. The correct answer is {correct_answer}.")
        await next_question(message)

    # Handle Network question
    elif current_game_type == 'network':
        try:
            selected_option = int(message.content) - 1
            if check_network_answer(selected_option, correct_answer):
                await message.channel.send("Correct!")
                await show_score_comparison(message.channel, message.author.id, 10)
            else:
                await message.channel.send(f"Wrong answer. The correct option was {correct_answer + 1}.")
            await next_question(message)
        except ValueError:
            await message.channel.send("Please respond with the option number (1, 2, 3, etc.).")

async def next_question(message):
    """Asks the next question."""
    global current_game_type
    if current_game_type == 'subnet':
        await start_game(message.channel, 'subnet')
    elif current_game_type == 'network':
        await start_game(message.channel, 'network')

def reset_game():
    """Resets the game state."""
    global current_question, correct_answer, current_game_type, game_task, game_initiator, question_timeout_task
    current_question = None
    correct_answer = None
    current_game_type = None
    game_initiator = None
    if game_task and not game_task.done():
        game_task.cancel()
        game_task = None
    if question_timeout_task and not question_timeout_task.done():
        question_timeout_task.cancel()

def update_user_score(user_id, points):
    """Updates the score for the user and saves it to a JSON file."""
    scores = load_user_scores()
    
    previous_score = scores.get(str(user_id), 0)
    
    # Update user's score
    scores[str(user_id)] = previous_score + points
    
    # Save the updated scores back to the file
    save_user_scores(scores)
    
    return previous_score, scores[str(user_id)]

async def show_score_comparison(ctx, user_id, new_points):
    """Shows the score comparison between the previous and current score."""
    previous_score, new_score = update_user_score(user_id, new_points)
    
    if previous_score == 0:
        await ctx.send(f"Your current score is {new_score} points. This is your first game!")
    else:
        await ctx.send(f"Your previous score was {previous_score} points, and now your score is {new_score} points.")

@bot.command()
async def game(ctx):
    """Starts the game and prompts the user to select a game type."""
    view = discord.ui.View()
    
    subnet_button = discord.ui.Button(label="Subnet", style=discord.ButtonStyle.primary)
    network_button = discord.ui.Button(label="Network Questions", style=discord.ButtonStyle.secondary)
    
    async def subnet_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await start_game(ctx, 'subnet')

    async def network_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await start_game(ctx, 'network')
    
    subnet_button.callback = subnet_callback
    network_button.callback = network_callback
    
    view.add_item(subnet_button)
    view.add_item(network_button)
    
    await ctx.send("Choose a game mode:", view=view)

@bot.command()
async def game_stop(ctx):
    """Command to stop the running game."""
    if game_task:
        reset_game()
        await ctx.send("Game stopped.")
    else:
        await ctx.send("No game is currently running.")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if game_initiator and current_question:
        await process_answer(message)

##############_RFC_##############

@bot.command()
async def rfc(ctx, rfc_number: str = None):
    """
    Retrieves and displays information about an RFC based on the number.
    
    :param rfc_number: RFC number to fetch. If none is provided, an error message is displayed.
    """
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

###########################################_Below this line_###########################################
###########################################_Role_Assignment_###########################################

@tasks.loop(hours=1)
async def update_roles():
    try:    
        await _Bot_Modul.fetch_and_save_roles(bot)
    except Exception as e:
        await log_to_channel(bot, f"An error occurred: {str(e)}")

def load_roles():
    try:
        with open(ROLE_JSON_FILE, 'r') as file:
            roles = json.load(file)
        return roles
    except Exception as e:
        print(f"Failed to load roles: {str(e)}")
        return {}

@bot.command()
async def addrole(ctx, role_name: str = None):
    """
    Assigns a specific role to the user running the command. Lists available roles if none specified or role not found.
    """
    roles = load_roles()

    if role_name is None:
        # Filtrera roller som inte finns i EXCLUDED_ROLES
        available_roles = [role for role in roles.keys() if role not in EXCLUDED_ROLES]
        if not available_roles:
            await ctx.send("No roles available for assignment.")
            return

        # Skapa en embed med rollerna
        embed = discord.Embed(title="Available Roles", description="Here are the roles you can assign:", color=discord.Color.blue())
        for role in available_roles:
            embed.add_field(name=f'"{role}"', value=f'Assign with `!addrole "{role}"`', inline=False)

        await ctx.send(embed=embed)
        return

    if role_name not in roles:
        await ctx.send(f"Role '{role_name}' could not be found.")
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        await ctx.send(f"Role '{role_name}' could not be found on this server.")
        return

    # Kontrollera om rollen är lösenordsskyddad
    if role_name in PASSWORD_PROTECTED_ROLES:
        await ctx.author.send(f"The role '{role_name}' requires a password. Please respond with the password within 60 seconds, The pasword can be found on Canvas in the descussion thread.:")

        try:
            # Vänta på att användaren skickar lösenordet i DM
            msg = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and isinstance(m.channel, discord.DMChannel))

            # Kontrollera om lösenordet är korrekt
            if msg.content != PASSWORD_PROTECTED_ROLES[role_name]:
                await ctx.author.send("Incorrect password. Role assignment canceled.")
                return

        except asyncio.TimeoutError:
            await ctx.author.send("You took too long to respond. Role assignment canceled.")
            return

    if role in ctx.author.roles:
        embed = discord.Embed(title="Role Already Assigned", description=f"You already have the role **{role_name}**.", color=discord.Color.orange())
    else:
        try:
            await ctx.author.add_roles(role)
            embed = discord.Embed(title="Role Assigned", description=f"The role **{role_name}** has been assigned to you!", color=discord.Color.green())
        except discord.Forbidden:
            embed = discord.Embed(title="Error", description="I do not have sufficient permissions to assign this role.", color=discord.Color.red())

    await ctx.send(embed=embed)

######_Remove_Role_#####

@bot.command()
async def removerole(ctx, role_name: str = None):
    """
    Removes a specific role from the user running the command. Lists available roles if none specified or role not found.
    """
    roles = load_roles()
    
    if role_name is None:
        # Filtrera roller som inte finns i EXCLUDED_ROLES
        available_roles = [role for role in roles.keys() if role not in EXCLUDED_ROLES]
        if not available_roles:
            await ctx.send("No roles available for removal.")
            return
        
        # Skapa en embed med rollerna
        embed = discord.Embed(title="Available Roles", description="Here are the roles you can remove:", color=discord.Color.blue())
        for role in available_roles:
            embed.add_field(name=role, value=f'Remove with `!removerole "{role}"`', inline=False)
        
        await ctx.send(embed=embed)
        return
    
    if role_name not in roles:
        await ctx.send(f"Role '{role_name}' could not be found.")
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        await ctx.send(f"Role '{role_name}' could not be found on this server.")
        return

    if role not in ctx.author.roles:
        embed = discord.Embed(title="Role Not Found", description=f"You do not have the role **{role_name}**.", color=discord.Color.orange())
    else:
        try:
            await ctx.author.remove_roles(role)
            embed = discord.Embed(title="Role Removed", description=f"The role **{role_name}** has been removed from you.", color=discord.Color.green())
        except discord.Forbidden:
            embed = discord.Embed(title="Error", description="I do not have sufficient permissions to remove this role.", color=discord.Color.red())
    
    await ctx.send(embed=embed)

###########################################_Study_Plan_Loops_###########################################

@tasks.loop(hours=24)  # Kör varje vecka (168 timmar = 7 dagar)
async def weekly_study_plan_CCIE():
    # Kontrollera att det är söndag innan den postar veckans tips
    if datetime.now().weekday() == 6:  # Söndag (0 = Måndag, 6 = Söndag)
        try:
            await _CCIE_Study_Plan.post_weekly_goal_CCIE(bot, CCIE_STUDY_CHANNEL_ID)
        except Exception as e:
            await log_to_channel(bot, f"An error occurred during the CCIE study plan: {str(e)}")

@tasks.loop(hours=24)  # Kör varje vecka (12 timme)
async def weekly_study_plan_CCNP():
    # Kontrollera att det är söndag innan den postar veckans tips
    if datetime.now().weekday() == 6:  # Söndag (0 = Måndag, 6 = Söndag)
        try:
            await _CCNP_Study_Plan.post_weekly_goal_CCNP(bot, CCNP_STUDY_CHANNEL_ID)
        except Exception as e:
            await log_to_channel(bot, f"An error occurred during the CCNP study plan: {str(e)}")

@tasks.loop(hours=24)  # Kör varje vecka (12 timme)
async def weekly_study_plan_CCNA():
    # Kontrollera att det är söndag innan den postar veckans tips
    if datetime.now().weekday() == 6:  # Söndag (0 = Måndag, 6 = Söndag)
        try:
            await _CCNA_Study_Plan.post_weekly_goal_CCNA(bot, CCNA_STUDY_CHANNEL_ID)
        except Exception as e:
            await log_to_channel(bot, f"An error occurred during the CCNA study plan: {str(e)}")

# Command to manually fetch and post jobs
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

# XP Levels Handling
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    try:
        await _Bot_Modul.handle_xp(message, XP_UPDATE_CHANNEL_ID)
    except Exception as e:
        await log_to_channel(bot, f"An error occurred while handling XP: {str(e)}")
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    try:
        await _Bot_Modul.handle_reaction_xp(reaction.message, XP_UPDATE_CHANNEL_ID)
    except Exception as e:
        await log_to_channel(bot, f"An error occurred while handling reaction XP: {str(e)}")

# Command to show user's level and XP
@bot.command()
async def level(ctx, member: discord.Member = None):
    try:
        if member is None:
            member = ctx.author
        await _Bot_Modul.show_level(ctx, member)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Loop to check welcome message every hour
@tasks.loop(hours=1)
async def check_welcome_message():
    try:
        await _Bot_Modul.ensure_welcome_message(bot, WELCOME_CHANNEL_ID)
    except Exception as e:
        await log_to_channel(bot, f"An error occurred while checking the welcome message: {str(e)}")

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