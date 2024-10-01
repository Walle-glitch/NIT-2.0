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
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), 'Internal_Modules'))

import _Bot_Modul
import _Open_AI
import _Games
import _CCIE_Study_Plan
import _CCNP_Study_Plan
import _External_Media
import _Auction
import _Bot_Config
import _Slash_Commands

###########################################_Global_Variables_##########################################

version_nr = "Current Version is 24/10/01.3"  # Global version number variable

# Roles with access 
BOT_ADMIN_ROLE_NAME = _Bot_Config._Bot_Admin_Role_Name()
ADMIN_ROLE_NAME =  _Bot_Config._Admin_Role_Name()
MOD_ROLE_NAME = _Bot_Config._Mod_Role_Name()
MENTOR_ROLE = _Bot_Config._Mentor_Role_Name()
LATE_NIGHT_ROLE_ID = _Bot_Config._LATE_NIGHT_ROLE_ID()

# Definiera roller som kräver lösenord
PASSWORD_PROTECTED_ROLES = _Bot_Config._protected_Poles()

GUILD_ID = _Bot_Config._GUILD_ID()

# Channel IDs
XP_UPDATE_CHANNEL_ID = _Bot_Config._XP_Update_Channel_ID()
JOB_CHANNEL_ID = _Bot_Config._Job_Channel_ID()
CCIE_STUDY_CHANNEL_ID = _Bot_Config._CCIE_Study_Channel_ID()
CCNP_STUDY_CHANNEL_ID = _Bot_Config._CCNP_Study_Channel_ID()
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

bot = commands.Bot(command_prefix="!", intents=intents) # Command Prefix 

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
    await bot.tree.sync() # Synchronize global application commands
    print("Global commands synced.")
    weekly_study_plan_CCIE.start()  
    weekly_study_plan_CCNP.start()
    monitor_activity.start(bot)
    # setup_rich_presence()  # Try setting up Rich Presence
    await log_to_channel(bot, "Processing historical data, notifications are disabled. This Will take a while...") # Disable notifications for historical data processing
    await _Bot_Modul.process_historical_data(bot, XP_UPDATE_CHANNEL_ID)
    await log_to_channel(bot, "Finished processing historical data, notifications are now enabled.") # Re-enable notifications after processing is done
    # Start scheduled tasks when the bot is ready
    update_roles.start()  
    check_welcome_message.start()
    # Find a specific channel to post the welcome message or ensure it's updated
    await log_to_channel(bot, "All Boot Events are now completed") # Re-enable notifications after processing is done

@bot.event
async def on_message(message):
    await track_activity(message)
    await bot.process_commands(message)

# Load module that contain bot Slash commands
_Slash_Commands.setup(bot)

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

# Git Repository Command
@bot.command()
async def git(ctx):
    try:
        await ctx.send('https://github.com/Walle-glitch/NIT-2.0.git')
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
            'so it is behind a normal (NAT Gateway).\n'
            '\n' 
            'Contact Walle/Nicklas for more info.'
            'Use /git for the link to the GitHub repo.\n'
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

@bot.command()
async def game(ctx):
    view = View()
    
    subnet_button = Button(label="Subnet", style=discord.ButtonStyle.primary)
    network_button = Button(label="Network Questions", style=discord.ButtonStyle.secondary)
    
    # Lägg till callbacks för knapparna
    async def subnet_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await _Games.start_game(ctx, 'subnet')

    async def network_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await _Games.start_game(ctx, 'network')
    
    subnet_button.callback = subnet_callback
    network_button.callback = network_callback
    
    view.add_item(subnet_button)
    view.add_item(network_button)
    
    await ctx.send("Choose a game mode:", view=view)

@bot.command()
async def game_stop(ctx):
    """Command to stop a running game."""
    if _Games.game_task:
        _Games.reset_game()
        await ctx.send("Game stopped.")
    else:
        await ctx.send("No game is currently running.")

@bot.event
async def on_message(message):
    # Process commands first
    await bot.process_commands(message)
    
    # Check if a game is running and if we are waiting for an answer
    if _Games.current_question is not None and message.content and message.author != bot.user:
        await _Games.process_answer(message)

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
#############################################_Media_Stuff_#############################################

@bot.command()
async def add_youtube(ctx, channel: str = None):
    if channel:
        added = _External_Media.add_channel("youtube", channel)
        if added:
            await ctx.send(f'YouTube channel "{channel}" added successfully.')
        else:
            await ctx.send(f'YouTube channel "{channel}" is already added.')
    else:
        await _External_Media.display_instructions("youtube", bot, ctx)

@bot.command()
async def remove_youtube(ctx, channel: str = None):
    if channel:
        removed = _External_Media.remove_channel("youtube", channel)
        if removed:
            await ctx.send(f'YouTube channel "{channel}" removed successfully.')
        else:
            await ctx.send(f'YouTube channel "{channel}" not found in the list.')
    else:
        await _External_Media.display_active_channels("youtube", bot, ctx)

@bot.command()
async def add_pod(ctx, channel: str = None):
    if channel:
        added = _External_Media.add_channel("podcast", channel)
        if added:
            await ctx.send(f'Podcast "{channel}" added successfully.')
        else:
            await ctx.send(f'Podcast "{channel}" is already added.')
    else:
        await _External_Media.display_instructions("podcast", bot, ctx)

@bot.command()
async def remove_pod(ctx, channel: str = None):
    if channel:
        removed = _External_Media.remove_channel("podcast", channel)
        if removed:
            await ctx.send(f'Podcast "{channel}" removed successfully.')
        else:
            await ctx.send(f'Podcast "{channel}" not found in the list.')
    else:
        await _External_Media.display_active_channels("podcast", bot, ctx)

@tasks.loop(hours=1)  # Weekly loop for fetching latest YouTube content
async def fetch_youtube_content():
    await _External_Media.fetch_latest_content("youtube", bot, YOUTUBE_CHANNEL_ID)

@tasks.loop(hours=1)  # Weekly loop for fetching latest podcast content
async def fetch_podcast_content():
    await _External_Media.fetch_latest_content("podcast", bot, PODCAST_CHANNEL_ID)

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

# Kolla om filen existerar, annars skapa en ny fil
if not os.path.exists("/home/bot/NIT-2.0/bot/Json_Files"):
    os.makedirs("/home/bot/NIT-2.0/bot/Json_Files")

if not os.path.isfile(ACTIVE_USERS_FILE):
    with open(ACTIVE_USERS_FILE, 'w') as file:
        json.dump({}, file)

def is_late_night():
    """Kolla om det är mellan 00:01 och 05:00"""
    current_time = datetime.now().time()
    return current_time >= datetime.strptime("00:01", "%H:%M").time() and current_time <= datetime.strptime("05:00", "%H:%M").time()

def load_active_users():
    """Ladda aktiva användare från JSON-filen"""
    with open(ACTIVE_USERS_FILE, 'r') as file:
        return json.load(file)

def save_active_users(active_users):
    """Spara aktiva användare till JSON-filen"""
    with open(ACTIVE_USERS_FILE, 'w') as file:
        json.dump(active_users, file)

async def add_role(member, role):
    """Lägg till LateNightCrew rollen till medlemmen"""
    if role not in member.roles:
        await member.add_roles(role)
        print(f"Lagt till LateNightCrew-roll för {member.name}")

async def remove_role(member, role):
    """Ta bort LateNightCrew rollen från medlemmen"""
    if role in member.roles:
        await member.remove_roles(role)
        print(f"Tagit bort LateNightCrew-roll från {member.name}")

@tasks.loop(minutes=1)
async def monitor_activity(bot):
    """Hanterar loopen för att övervaka användaraktiviteten"""
    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(LATE_NIGHT_ROLE_ID)
    active_users = load_active_users()
    current_time = datetime.now()

    for user_id, last_active_str in list(active_users.items()):
        last_active = datetime.fromisoformat(last_active_str)
        member = guild.get_member(int(user_id))

        if member and is_late_night():
            # Lägg till roll om den inte redan finns
            await add_role(member, role)
        elif member and (current_time - last_active) > timedelta(hours=14):
            # Ta bort roll om 14 timmar har gått
            await remove_role(member, role)
            del active_users[user_id]

    # Uppdatera JSON-filen
    save_active_users(active_users)

    # Rensa filen om klockan är efter 05:00
    if not is_late_night():
        with open(ACTIVE_USERS_FILE, 'w') as file:
            json.dump({}, file)

async def track_activity(message):
    """Spåra användaraktivitet"""
    if message.author.bot:
        return

    if is_late_night():
        active_users = load_active_users()
        active_users[message.author.id] = datetime.now().isoformat()
        save_active_users(active_users)

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
        ("git", None),
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