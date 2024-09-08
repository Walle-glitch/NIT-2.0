# This is _Bot_Modul.py

###########################################_Import_Modules_##########################################

import requests
import telnetlib
from bs4 import BeautifulSoup
import paramiko
import _Router_Conf
import time
from datetime import datetime, timedelta
import discord
import asyncio
import random
from discord.ext import commands
import json
import os
import _Bot_Config as botConfig
#nimport botConfig  # Bot-token and Bot info exists locally on the server; this module contains that info.
from discord.ui import Button, View
from discord import app_commands

################  Global Refs ################

ROLE_JSON_FILE = "./Json_Files/roles.json"  # File where roles are saved
WELCOME_MESSAGE_FILE = "./Json_Files/welcome_message_id.json"  # File where the welcome message ID is saved
XP_FILE = "./Json_Files/xp_data.json" # File For storing all User XP
EXCLUDED_ROLES = ["Admin", "Moderator", "Administrator"] # Roles that cannot be assigned using the /roll command

# Define static roles in a dictionary format
STATIC_ROLES = {
    "NIT_24": "1254895590567837776",
    "NIT_23": "1115331511848271942",
    "NIT_22": "1012047713610760383",
    "Another Start Year": "1013246037349126204",
    "3rd Year!": "1079120617560879195",
    "Union Member": "1079112794189865111",
    "Arkiv-enjoyer": "1160861563083837511",
}

log_to_channel_id = 1277567653765976074  # The Discord channel ID where you want to send the logs OBS! Controll that it is the same as LOG_CHANNEL_ID in main.py
Admin_Channel_id = 1012447677880995920 # Admin Channel ID.  


def setup(bot):
    # Define a simple slash command
    @bot.tree.command(name="ping", description="Check if the bot is active")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

    @bot.tree.command(name="hello", description="Say hello")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message("Hello!", ephemeral=True)

######### Utility Functions for Logging #########

async def log_to_channel(bot, message):
    """
    Sends a message to the logging channel and prints to the server logs.
    """
    print(message)  # Print to server logs
    channel = bot.get_channel(log_to_channel_id)
    if channel:
        await channel.send(message)

######### The Resources ############ 

async def send_resource_embed(ctx):
    # Create a list to hold multiple embeds
    embeds = []

    # First embed
    embed = discord.Embed(
        title="Course Books and Resources",
        description="",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="[**linux (ogl) (Might Be old)**]", value="https://dl.remilia.se/os/", inline=False)
    embed.add_field(name="[**linux (ogl-tenta) (Might Be old)**]", value="https://www.studocu.com/sv/document/hogskolan-vast/operativsystem-med-gnulinux/ogl202-tentafragor-en-sammanfattning-fran-gamla-tenta-fragor-och-fragor-som-kan-uppkomma/10085924", inline=False)
    embed.add_field(name="[**python (most of it)**]", value="https://files.catbox.moe/tj6k7c.zip", inline=False)
    embed.add_field(name="[**ekonomi Kursen (Might Be old)**]", value="http://libgen.rs/book/index.php?md5=78A08A5D5329DF2BE639849653A0E199", inline=False)
    embed.add_field(name="**CWNA-107 (Old version but still good):**", value="\u200b", inline=False)
    embed.add_field(name="[**epub**]", value="http://libgen.rs/book/index.php?md5=05F137E9D19D066C6E9E50F3E5C5B110", inline=False)
    embed.add_field(name="[**pdf**]", value="http://libgen.rs/book/index.php?md5=D80B9C3F3A0FDC642A955197C94BDEBB", inline=False)
    embed.add_field(name="[**Cisco firewall**]", value="http://library.lol/main/0E0CCB79FF5E15785BCFEA8BF5559AC7", inline=False)
    embed.add_field(name="[**Some Notes CCNP and SEC**]", value="https://docs.google.com/document/d/1JAeWT1ovXITvOxSoUHjhk_sERsZlIZOrnKJYe5X6Y0M/edit", inline=False)
    embed.add_field(name="[**vSphere 6.7**]", value="http://libgen.rs/book/index.php?md5=77B976B18B7F5B218DC1324E27621F72", inline=False)
    embed.add_field(name="[**uppgrade/repair pcs (22nd edition)**]", value="http://libgen.rs/book/index.php?md5=9D0AE23F01B7D7E130EF88D62A01FAF6", inline=False)
    embed.add_field(name="[**ccnp2 nit20 powerpoints**]", value="https://files.catbox.moe/6l0pep.zip", inline=False)
    embed.add_field(name="[**ccnp3 nit20 powerpoints**]", value="https://files.catbox.moe/5utyd8.zip", inline=False)
    embed.add_field(name="[**Wi-Fi Dump**]", value="https://docs.google.com/document/d/1BFMuQcGjwZxuaD9DJ0fco3xRuCCinvWuEWbFpCviMUM/edit", inline=False)
    embed.add_field(name="[**ENARSI för CCNP3**]", value="https://annas-archive.org/md5/45c415c2296f0f6709e5547e2d5d2c7e", inline=False)

    embeds.append(embed)

    # Second embed for additional information
    embed2 = discord.Embed(
        title="Blogs and Fun Stuff",
        description="",
        color=discord.Color.blue()
    )
    
    embed2.add_field(name="[**Cloudflare Blog**]", value="https://blog.cloudflare.com/making-phishing-defense-seamless-cloudflare-yubico/", inline=False)
    embed2.add_field(name="[**Study tips**]", value="https://www-freecodecamp-org.cdn.ampproject.org/c/s/www.freecodecamp.org/news/supercharged-studying-with-python-anki-chatgpt/amp/", inline=False)
    embed2.add_field(name="[**BEST cheat-sheets in the world**]", value="https://packetlife.net/library/cheat-sheets/", inline=False)
    
    embeds.append(embed2)

    # Third embed for YouTube resources
    embed3 = discord.Embed(
        title="YouTube Resources",
        description="",
        color=discord.Color.blue()
    )
    
    embed3.add_field(name="[**CCNA**]", value="https://youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ&si=Z_ApQ1TJtE1EJqhB", inline=False)
    embed3.add_field(name="[**Cybersecurity**]", value="https://www.youtube.com/watch?v=IQZXqUggR8w&list=PL1U-z6tCj5WBwy4WoMS3jSi7WE4AGOUcY", inline=False)
    embed3.add_field(name="[**Mixed Resources for GDA course and Internet services**]", value="https://www.youtube.com/watch?v=bYjQakUxeVY&list=PLdz-iDPGfMEJWW0JdbWwP0bCkBnJGP5q4", inline=False)
    embed3.add_field(name="[**CCNA (Complements well with Jeremy)**]", value="https://www.youtube.com/watch?v=S7MNX_UD7vY&list=PLIhvC56v63IJVXv0GJcl9vO5Z6znCVb1P", inline=False)
    embed3.add_field(name="[**CCNA**]", value="https://www.youtube.com/playlist?list=PLIhvC56v63IKrRHh3gvZZBAGvsvOhwrRF", inline=False)
    
    embeds.append(embed3)

    # Fourth embed for content creators and downloads
    embed4 = discord.Embed(
        title="**Content Creators on YouTube**",
        description="",
        color=discord.Color.blue()
    )
    
    embed4.add_field(name="[**Indently**]", value="https://www.youtube.com/@Indently", inline=False)
    embed4.add_field(name="[**Ccieordie**]", value="https://www.youtube.com/@Ccieordie_arteq", inline=False)
    embed4.add_field(name="[**INE**]", value="https://www.youtube.com/@INEtraining", inline=False)
    embed4.add_field(name="[**Art of Network Engineering**]", value="https://www.youtube.com/@artofneteng", inline=False)
    embed4.add_field(name="[**Keith Barker**]", value="https://www.youtube.com/@KeithBarker", inline=False)
    embed4.add_field(name="[**Chris Greer**]", value="https://www.youtube.com/@ChrisGreer", inline=False)
    embed4.add_field(name="[**David Bombal**]", value="https://www.youtube.com/@davidbombal", inline=False)
    embed4.add_field(name="[**Jeremy's IT Lab**]", value="https://www.youtube.com/@JeremysITLab", inline=False)
    embed4.add_field(name="[**Arthur Salmon**]", value="https://www.youtube.com/@arthursalmon3414", inline=False)
    embed4.add_field(name="[**PowerCert Animated Videos**]", value="https://www.youtube.com/@PowerCertAnimatedVideos", inline=False)
    embed4.add_field(name="[**NetworkChuck**]", value="https://www.youtube.com/@NetworkChuck", inline=False)

    embeds.append(embed4)

    # Fifth embed for downloads
    embed5 = discord.Embed(
        title="Good Downloads",
        description="",
        color=discord.Color.blue()
    )
   
    embed5.add_field(name="[**(note taking) Notepad++**]", value="https://notepad-plus-plus.org/", inline=False)
    embed5.add_field(name="[**(note taking) Obsidian**]", value="https://obsidian.md/", inline=False)
    embed5.add_field(name="[**(Programming/ IDE) Visual Studio Code**]", value="https://code.visualstudio.com/", inline=False)
    embed5.add_field(name="[**(Your best friend) Putty**]", value="https://www.putty.org/", inline=False)
    embed5.add_field(name="[**(Flash Cards) Anki**]", value="https://apps.ankiweb.net/", inline=False)
    embed5.add_field(name="[**(Packet Capture & Analyzer) Wireshark**]", value="https://www.wireshark.org/", inline=False)
    embed5.add_field(name="[**(GNS3)**]", value="https://gns3.teachable.com/courses/", inline=False)
    embed5.add_field(name="[**(Eve-ng)**]", value="https://www.eve-ng.net/", inline=False)
    
    embeds.append(embed5)

    # Sixth embed for account creation
    embed6 = discord.Embed(
        title="Get an account",
        description="",
        color=discord.Color.blue()
    )
    
    embed6.add_field(name="[**GitHub**]", value="https://github.com/", inline=False)
    embed6.add_field(name="[**Credly**]", value="https://www.credly.com/", inline=False)
    embed6.add_field(name="[**LinkedIn**]", value="https://www.linkedin.com/", inline=False)
    embed6.add_field(name="[**Postman Student Program**]", value="https://www.postman.com/student-program/student-expert/", inline=False)

    embeds.append(embed6)

    # Seventh and final embed for a final message
    embed7 = discord.Embed(
        title="Last but still...",
        description="",
        color=discord.Color.blue()
    )
    
    embed7.add_field(name="ASK!", value="You can always ask if someone has something more ;) (Some stuff isn't given away for free, so to say)", inline=False)

    embeds.append(embed7)

    # Send all embeds
    for embed in embeds:
        await ctx.send(embed=embed)

######### Create a Ticket ######### 

# Function to create a new ticket
async def create_ticket(guild, category_id, user, channel_name=None):
    category = discord.utils.get(guild.categories, id=category_id)
    if not category:
        return None

    if not channel_name:
        ticket_number = random.randint(1000, 9999)
        channel_name = f"ticket-{ticket_number}"

    channel = await guild.create_text_channel(channel_name, category=category)
    await channel.send(f"Hello {user.mention}, thank you for creating a ticket. Please describe your issue.")
    asyncio.create_task(check_inactivity(channel))

    return channel

async def close_ticket(channel):
    await channel.send("This ticket is now being closed.")
    await channel.delete()

async def check_inactivity(channel, timeout=60):
    last_activity_time = datetime.now(datetime.UTC)()
    while True:
        await asyncio.sleep(timeout * 60)
        if (datetime.now(datetime.UTC)() - last_activity_time) >= timedelta(minutes=timeout):
            await channel.send("Closing this ticket due to inactivity.")
            await channel.delete()
            break
        last_activity_time = max((await channel.history(limit=1).flatten())[0].created_at, last_activity_time)

################### GET AN RFC ###################

def get_rfc(rfc_number):
    """
    Retrieves an RFC from the IETF data tracker based on RFC number.
    
    :param rfc_number: The RFC number to retrieve.
    :return: A string with the RFC title and link, or an error message.
    """
    if not isinstance(rfc_number, int) or rfc_number <= 0:
        return "Error: Invalid RFC number. Please provide a positive integer."
    
    # Build the URL for the RFC
    url = f"https://datatracker.ietf.org/doc/html/rfc{rfc_number}"
    
    try:
        # Send an HTTP GET request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for status codes 4xx or 5xx
        
        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get the RFC title from the HTML
        title_tag = soup.find('title')
        if title_tag and "RFC" in title_tag.text:
            title = title_tag.text
        else:
            title = "RFC title could not be found or the provided RFC number is invalid."

        # Return the RFC title and link
        return f"{title}\nLink: {url}"
    
    except requests.RequestException as e:
        return f"Error retrieving RFC: {e}"

############### Create a BGP neighbor ###################

# Function to configure BGP on a specific router
def configure_bgp_neighbor(neighbor_ip, neighbor_as):
    router_ip = _Router_Conf.ROUTER_IP
    username = _Router_Conf.SSH_USERNAME
    password = _Router_Conf.SSH_PASSWORD
    
    try:
        # Connect to the router via Telnet
        tn = telnetlib.Telnet(router_ip)

        # Log in with username and password
        tn.read_until(b"Username: ")
        tn.write(username.encode('ascii') + b"\n")
        
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

        # Wait for the prompt
        
        # Send commands to configure BGP
        commands = [
            "enable",  # Assuming no enable password is needed
            "configure terminal",
            f"router bgp 64512",
            f"neighbor {neighbor_ip} remote-as {neighbor_as}",
            f"neighbor {neighbor_ip} ebgp-multihop 30",
            f"neighbor {neighbor_ip} update-source GigabitEthernet0/0",
            f"address-family ipv4",
            f"neighbor {neighbor_ip} activate",
            "exit-address-family",
            "exit",
            "interface gi0/0",
            "do show ip interface brief | include GigabitEthernet0/0",
            "do show running-config | include router bgp"
        ]

        output = ""
        for cmd in commands:
            tn.write(cmd.encode('ascii') + b"\n")
            time.sleep(1)  # Wait for the command to execute
            output += tn.read_very_eager().decode('ascii')

        # Extract information about IP address and existing AS number
        interface_output = output.splitlines()
        gi0_ip = ""
        as_number = ""
        for line in interface_output:
            if "GigabitEthernet0/0" in line:
                gi0_ip = line.split()[1]  # Extract the IP address from the correct line
            if "router bgp" in line:
                as_number = line.split()[2]  # Extract the AS number from the correct line

        return gi0_ip, as_number

    except Exception as e:
        return f"An error occurred: {str(e)}", None

    finally:
        # Close the Telnet connection
        tn.write(b"exit\n")
        tn.close()

############### Moderation of Members ###################

async def kick_user(ctx, user: discord.Member, reason=None):
    try:
        await user.kick(reason=reason)
        await report_action(ctx, user, "kick", reason)
    except discord.Forbidden:
        await ctx.send("I do not have permission to kick this user.")
    except Exception as e:
        await ctx.send(f"An error occurred while kicking the user: {str(e)}")

async def ban_user(ctx, user: discord.Member, reason=None):
    try:
        await user.ban(reason=reason)
        await report_action(ctx, user, "ban", reason)
    except discord.Forbidden:
        await ctx.send("I do not have permission to ban this user.")
    except Exception as e:
        await ctx.send(f"An error occurred while banning the user: {str(e)}")

async def mute_user(ctx, user: discord.Member, duration_in_hours: int, reason=None):
    try:
        duration_in_seconds = duration_in_hours * 3600
        await user.timeout(discord.utils.utcnow() + discord.timedelta(seconds=duration_in_seconds), reason=reason)
        await report_action(ctx, user, "mute", reason, duration_in_hours)
    except discord.Forbidden:
        await ctx.send("I do not have permission to mute this user.")
    except Exception as e:
        await ctx.send(f"An error occurred while muting the user: {str(e)}")

async def report_action(ctx, user: discord.Member, action: str, reason=None, duration=None):
    report_channel_id = Admin_Channel_id  # Replace with the actual channel ID for reports
    report_channel = ctx.guild.get_channel(report_channel_id)

    if not report_channel:
        return

    admin_name = ctx.author.name
    user_name = user.name
    if action == "mute":
        report_message = f"**{admin_name}** muted **{user_name}** for {duration} hours. Reason: {reason}"
    else:
        report_message = f"**{admin_name}** {action}ed **{user_name}**. Reason: {reason}"

    await report_channel.send(report_message)

################################_XP_Handler_####################################

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

xp_data = load_xp_data()

def xp_needed_for_level(level):
    if level < 11:
        return 100
    elif level < 101:
        return 1000
    else:
        return 2500

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
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                # Iterate through the message history
                async for message in channel.history(limit=None):
                    await handle_xp(message, XP_UPDATE_CHANNEL_ID, send_notifications=False)
                    
                    # Handle reactions
                    for reaction in message.reactions:
                        # Replace flatten() with an async comprehension
                        users = [user async for user in reaction.users()]
                        for user in users:
                            if user != message.author:
                                await handle_reaction_xp(message, XP_UPDATE_CHANNEL_ID, send_notifications=False)
            except Exception as e:
                print(f"Could not process channel {channel.name}: {str(e)}")

    print("Finished processing historical data.")

########### Get Job Listings ###############

# API URL and API key for Indeed
INDEED_API_URL = "https://api.indeed.com/ads/apisearch"
INDEED_API_KEY = botConfig._YOUR_INDEED_API_KEY()

def fetch_jobs():
    jobs = []
    params = {
        'publisher': INDEED_API_KEY,
        'q': 'Network Technician',
        'l': 'Sweden',
        'sort': 'date',
        'format': 'json',
        'v': '2'
    }
    try:
        response = requests.get(INDEED_API_URL, params=params)
        response.raise_for_status()
        job_data = response.json()

        for job in job_data.get('results', []):
            jobs.append({
                'title': job['jobtitle'],
                'company': job['company'],
                'location': job['formattedLocation'],
                'url': job['url']
            })
    except Exception as e:
        print(f"Error fetching jobs: {str(e)}")

    return jobs

async def fetch_and_post_jobs(bot, job_channel_id):
    jobs = fetch_jobs()

    if not jobs:
        print("No jobs found.")
        return

    channel = bot.get_channel(job_channel_id)

    if not channel:
        print(f"Channel with ID {job_channel_id} not found.")
        return

    for job in jobs:
        embed = discord.Embed(
            title=job['title'],
            description=f"{job['company']} - {job['location']}",
            url=job['url'],
            color=discord.Color.blue()
        )
        await channel.send(embed=embed)

################# Role Assignments #################

async def check_and_initialize_roles(bot):
    if not os.path.exists(ROLE_JSON_FILE) or os.path.getsize(ROLE_JSON_FILE) == 0:
        print("Role JSON file is missing or empty. Initializing...")
        await fetch_and_save_roles(bot)

async def fetch_and_save_roles(bot):
    for guild in bot.guilds:
        roles_data = {}
        for role in guild.roles:
            roles_data[role.name] = role.id
        with open(ROLE_JSON_FILE, "w") as f:
            json.dump(roles_data, f, indent=4)
        print("Roles have been saved to roles.json")

async def assign_role(ctx, role_name=None):
    await check_and_initialize_roles(ctx.bot)

    with open(ROLE_JSON_FILE, "r") as f:
        roles_data = json.load(f)

    if role_name is None:
        available_roles = [role for role in roles_data if role not in EXCLUDED_ROLES]
        if available_roles:
            roles_list = "\n".join(available_roles)
            await ctx.send(f"Available roles:\n{roles_list}")
        else:
            await ctx.send("No available roles to assign.")
        return

    if role_name not in roles_data:
        await ctx.send(f"The role '{role_name}' does not exist.")
        return

    if role_name in EXCLUDED_ROLES:
        await ctx.send(f"You cannot assign the role '{role_name}'.")
        return

    role_id = roles_data[role_name]
    role = discord.utils.get(ctx.guild.roles, id=role_id)

    if not role:
        await ctx.send(f"The role '{role_name}' could not be found on the server.")
        return

    if role in ctx.author.roles:
        await ctx.send(f"You already have the role '{role_name}'.")
    else:
        await ctx.author.add_roles(role)
        await ctx.send(f"The role '{role_name}' has been assigned to you.")

########################################################################################

class RoleButton(Button):
    def __init__(self, label, style, role_id=None):
        super().__init__(label=label, style=style)
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        # If role_id is provided, fetch the role by ID; otherwise, fetch it by name
        role = interaction.guild.get_role(int(self.role_id)) if self.role_id else discord.utils.get(interaction.guild.roles, name=self.label)
        
        if role:
            if role in interaction.user.roles:
                await interaction.response.send_message(f"You already have the role {role.name}.", ephemeral=True)
            else:
                try:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"The role {role.name} has been assigned to you.", ephemeral=True)
                except discord.Forbidden:
                    await interaction.response.send_message("I do not have permission to assign roles.", ephemeral=True)
        else:
            await interaction.response.send_message(f"The role for {self.label} could not be found on the server.", ephemeral=True)

def create_role_buttons_view():
    view = View()
    # Define the button styles and labels; using STATIC_ROLES if role_id is provided
    ROLE_BUTTONS = [
        {"label": "NIT_24", "style": discord.ButtonStyle.blurple, "role_id": STATIC_ROLES.get("NIT_24")},
        {"label": "NIT_23", "style": discord.ButtonStyle.blurple, "role_id": STATIC_ROLES.get("NIT_23")},
        {"label": "NIT_22", "style": discord.ButtonStyle.blurple, "role_id": STATIC_ROLES.get("NIT_22")},
        {"label": "Another Start Year", "style": discord.ButtonStyle.gray, "role_id": STATIC_ROLES.get("Another Start Year")},
        {"label": "3rd Year!", "style": discord.ButtonStyle.green, "role_id": STATIC_ROLES.get("3rd Year!")},
        {"label": "Union Member", "style": discord.ButtonStyle.red, "role_id": STATIC_ROLES.get("Union Member")},
    ]
    
    # Create buttons and add them to the view
    for button_info in ROLE_BUTTONS:
        button = RoleButton(label=button_info['label'], style=button_info['style'], role_id=button_info['role_id'])
        view.add_item(button)
    return view

def get_welcome_message_id():
    if os.path.exists(WELCOME_MESSAGE_FILE):
        with open(WELCOME_MESSAGE_FILE, "r") as f:
            data = json.load(f)
            return data.get("message_id", None)
    return None

def save_welcome_message_id(message_id):
    with open(WELCOME_MESSAGE_FILE, "w") as f:
        json.dump({"message_id": message_id}, f)

async def post_welcome_message(channel):
    embed = discord.Embed(
        title="Welcome to the HV - NIT + The Additional Year",
        description=(
            "Hello!\n"
            "This is the NIT program's Discord server! (Welcome to the NIT Church)\n"
            "We have a unique year channel that you can access through roles.\n\n"
            "In the 'PLUGG' category, we have Course Chat Channels for Year 1, Year 2, and Year 3 (The Additional Year). "
            "And a forum for labs (Practical moments in the program).\n"
            "So, if you are in the lab or with PT and struggling, "
            "you can create a thread or read to see if there is something that can help you!\n\n"
            "We also want to keep the NIT alumni who have moved on and started working. "
            "They may have some tips for working life or may one day be looking for staff or summer workers. "
            "#life-after-nit"
        ),
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="The Server is for You",
        value=(
            "* The server is run and owned by students, for students in the NIT program and The Additional Year.\n"
            "* Students are the primary audience.\n"
            "* Remember that the server is open; anyone can join (do not write anything inappropriate or \"secret\").\n"
            "* The server will only be as good as we make it.\n"
            "* Contribute to a positive environment."
        ),
        inline=False
    )
    
    embed.add_field(
        name="Moderation",
        value="Mods [Privilege 10] and Admins [Privilege 15] keep an extra eye on this Discord, "
              "but we mainly believe that everyone is an adult and can behave accordingly!",
        inline=False
    )
    
    embed.add_field(
        name="Welcome!",
        value="Click a button below to set your year and get started.\n\n"
              "Welcome!\n//Admins",
        inline=False
    )
    
    view = create_role_buttons_view()
    message = await channel.send(embed=embed, view=view)
    save_welcome_message_id(message.id)

async def ensure_welcome_message(bot, channel_id):
    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"Channel with ID {channel_id} not found.")
        return
    
    message_id = get_welcome_message_id()
    
    if message_id:
        try:
            message = await channel.fetch_message(message_id)
            return
        except discord.NotFound:
            pass
    
    await post_welcome_message(channel)

########################################################################################
