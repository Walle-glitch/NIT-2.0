# This is _Bot_Modul.py

###########################################_Import_Modules_##########################################

import requests
import telnetlib
from bs4 import BeautifulSoup
import paramiko
import _Router_Conf
import time
import discord
import asyncio
import random
from discord.ext import commands
import json
import os
import botConfig  # Bot-token and Bot info exists locally on the server; this module contains that info.
from discord.ui import Button, View

################  Global Refs ################

ROLE_JSON_FILE = "roles.json"  # Fil där roller sparas
WELCOME_MESSAGE_FILE = "welcome_message_id.json" # Fil där Välkommst meddelandet sparas

# Roller som inte ska kunna tilldelas via kommandot ./roll
EXCLUDED_ROLES = ["Admin", "Moderator", "Administrator"]

######### The resourses ############ 

async def send_resource_embed(ctx):
    # Skapa en lista för att hålla flera embeds
    embeds = []

    # Första embed
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

    # Lägg till det första embed till listan
    embeds.append(embed)

    # Andra embed för resten av informationen
    embed2 = discord.Embed(
        title="Bloogs and fun stuff",
        description="",
        color=discord.Color.blue()
    )
    
    embed2.add_field(name="[**Cloudflare Blog**]", value="https://blog.cloudflare.com/making-phishing-defense-seamless-cloudflare-yubico/", inline=False)
    embed2.add_field(name="[**Study tips**]", value="https://www-freecodecamp-org.cdn.ampproject.org/c/s/www.freecodecamp.org/news/supercharged-studying-with-python-anki-chatgpt/amp/", inline=False)
    embed2.add_field(name="[**BEST cheat-sheets in the world**]", value="https://packetlife.net/library/cheat-sheets/", inline=False)
    
    embed7 = discord.Embed(
        title="YouTube resources",
        description="",
        color=discord.Color.blue()
    )
    
    embed7.add_field(name="[**CCNA**]", value="https://youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ&si=Z_ApQ1TJtE1EJqhB", inline=False)
    embed7.add_field(name="[**Cybersäkerhet**]", value="https://www.youtube.com/watch?v=IQZXqUggR8w&list=PL1U-z6tCj5WBwy4WoMS3jSi7WE4AGOUcY", inline=False)
    embed7.add_field(name="[**Blandat inför GDA kursen och lite för Internettjänster**]", value="https://www.youtube.com/watch?v=bYjQakUxeVY&list=PLdz-iDPGfMEJWW0JdbWwP0bCkBnJGP5q4", inline=False)
    embed7.add_field(name="[**CCNA (Kompletteras bra med Jeremy)**]", value="https://www.youtube.com/watch?v=S7MNX_UD7vY&list=PLIhvC56v63IJVXv0GJcl9vO5Z6znCVb1P", inline=False)
    embed7.add_field(name="[**CCNA**]", value="https://www.youtube.com/playlist?list=PLIhvC56v63IKrRHh3gvZZBAGvsvOhwrRF", inline=False)
    
    embeds.append(embed7)

    # Tredje embed för Content Creators och Downloads
    embed3 = discord.Embed(
        title="**Content creators on YouTube**",
        description="",
        color=discord.Color.blue()
    )
    
    embed3.add_field(name="[**Indently**]", value="https://www.youtube.com/@Indently", inline=False)
    embed3.add_field(name="[**Ccieordie**]", value="https://www.youtube.com/@Ccieordie_arteq", inline=False)
    embed3.add_field(name="[**INE**]", value="https://www.youtube.com/@INEtraining", inline=False)
    embed3.add_field(name="[**Art of Network Engineering**]", value="https://www.youtube.com/@artofneteng", inline=False)
    embed3.add_field(name="[**Keith Barker**]", value="https://www.youtube.com/@KeithBarker", inline=False)
    embed3.add_field(name="[**Chris Greer**]", value="https://www.youtube.com/@ChrisGreer", inline=False)
    embed3.add_field(name="[**David Bombal**]", value="https://www.youtube.com/@davidbombal", inline=False)
    embed3.add_field(name="[**Jeremy's IT Lab**]", value="https://www.youtube.com/@JeremysITLab", inline=False)
    embed3.add_field(name="[**Arthur Salmon**]", value="https://www.youtube.com/@arthursalmon3414", inline=False)
    embed3.add_field(name="[**PowerCert Animated Videos**]", value="https://www.youtube.com/@PowerCertAnimatedVideos", inline=False)
    embed3.add_field(name="[**NetworkChuck**]", value="https://www.youtube.com/@NetworkChuck", inline=False)

    embeds.append(embed3)

      # Fjärde embed för konton och avslutande meddelande
    embed4 = discord.Embed(
        title="Good Downloads",
        description="",
        color=discord.Color.blue()
    )
   
    embed4.add_field(name="[**(note taking) Notepad++**]", value="https://notepad-plus-plus.org/", inline=False)
    embed4.add_field(name="[**(note taking) Obsidian**]", value="https://obsidian.md/", inline=False)
    embed4.add_field(name="[**(Programming/ IDE) Visual Studio Code**]", value="https://code.visualstudio.com/", inline=False)
    embed4.add_field(name="[**(Your best friend) Putty**]", value="https://www.putty.org/", inline=False)
    embed4.add_field(name="[**(Flash Cards) Anki**]", value="https://apps.ankiweb.net/", inline=False)
    embed4.add_field(name="[**(Packet Capture & Analyzer) Wireshark**]", value="https://www.wireshark.org/", inline=False)
    embed4.add_field(name="[**(GNS3)**]", value="https://gns3.teachable.com/courses/", inline=False)
    embed4.add_field(name="[**(Eve-ng)**]", value="https://www.eve-ng.net/", inline=False)
    
    embeds.append(embed4)

    # femte embed för konton och avslutande meddelande
    embed5 = discord.Embed(
        title="Get an account",
        description="",
        color=discord.Color.blue()
    )
    
    embed5.add_field(name="[**GitHub**]", value="https://github.com/", inline=False)
    embed5.add_field(name="[**Credly**]", value="https://www.credly.com/", inline=False)
    embed5.add_field(name="[**LinkedIn**]", value="https://www.linkedin.com/", inline=False)
    embed5.add_field(name="[**Postman Student Program**]", value="https://www.postman.com/student-program/student-expert/", inline=False)


    embeds.append(embed5)

    # sista embed för konton och avslutande meddelande
    embed6 = discord.Embed(
        title="Last but still...",
        description="",
        color=discord.Color.blue()
    )
    
    embed6.add_field(name="ASK!", value="You can always ask if someone has something more ;) (Some stuff isn't given away for free, so to say)", inline=False)

    embeds.append(embed6)

    # Skicka alla embeds
    for embed in embeds:
        await ctx.send(embed=embed)

######### Create an Ticket ######### 

# Function to create a new ticket
async def create_ticket(guild, category_id, user, channel_name=None):
    category = discord.utils.get(guild.categories, id=category_id)
    if not category:
        return None

    # Use the provided channel name or generate a random 4-digit number
    if not channel_name:
        ticket_number = random.randint(1000, 9999)
        channel_name = f"ticket-{ticket_number}"

    # Create the new channel in the specified category
    channel = await guild.create_text_channel(channel_name, category=category)

    # Add a message in the new ticket channel
    await channel.send(f"Hello {user.mention}, thank you for creating a ticket. Please describe your issue.")

    # Start the inactivity timer
    asyncio.create_task(check_inactivity(channel))

    return channel

# Function to check inactivity and close the ticket after 2 days
async def check_inactivity(channel):
    def check_message(m):
        return m.channel == channel

    try:
        # Wait for any message in the channel for 2 days (172800 seconds)
        await channel.bot.wait_for('message', check=check_message, timeout=172800)
    except asyncio.TimeoutError:
        await channel.send("This ticket has been inactive for 2 days and will now be closed.")
        await close_ticket(channel)

# Function to close the ticket
async def close_ticket(channel):
    await channel.delete()


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
        # Handle any HTTP errors
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
#        tn.read_until(b">")
        
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
        # Handle any errors that might occur
        return f"An error occurred: {str(e)}", None

    finally:
        # Close the Telnet connection
        tn.write(b"exit\n")
        tn.close()

############### Moderation of Members ###################

# Function to kick a user
async def kick_user(ctx, user: discord.Member, reason=None):
    await user.kick(reason=reason)
    await report_action(ctx, user, "kick", reason)

# Function to ban a user
async def ban_user(ctx, user: discord.Member, reason=None):
    await user.ban(reason=reason)
    await report_action(ctx, user, "ban", reason)

# Function to mute a user (timeout)
async def mute_user(ctx, user: discord.Member, duration_in_hours: int, reason=None):
    duration_in_seconds = duration_in_hours * 3600
    await user.timeout(discord.utils.utcnow() + discord.timedelta(seconds=duration_in_seconds), reason=reason)
    await report_action(ctx, user, "mute", reason, duration_in_hours)

# Function to report the action to the specified report channel
async def report_action(ctx, user: discord.Member, action: str, reason=None, duration=None):
    report_channel_id = 1012447677880995920  # Replace with the actual channel ID for reports
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

XP_FILE = "xp_data.json"

# Funktioner för att ladda och spara XP-data
def load_xp_data():
    if os.path.exists(XP_FILE):
        with open(XP_FILE, "r") as f:
            return json.load(f)
    return {}

def save_xp_data(data):
    with open(XP_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Ladda XP-data när modulen importeras
xp_data = load_xp_data()

# Hantera XP-systemet för inkommande meddelanden
async def handle_xp(message, xp_update_channel_id):
    user = message.author

    # Om användaren inte finns i datan, skapa en ny post
    if str(user.id) not in xp_data:
        xp_data[str(user.id)] = {"xp": 0, "level": 1}

    # Ge användaren en slumpmässig mängd XP och spara datan
    xp_data[str(user.id)]["xp"] += random.randint(5, 15)
    save_xp_data(xp_data)

    # Kontrollera om användaren ska gå upp i nivå
    await check_level_up(user, xp_update_channel_id)

# Hantera när en användare får en reaktion på sitt meddelande
async def handle_reaction_xp(message, xp_update_channel_id):
    user = message.author

    # Om användaren inte finns i datan, skapa en ny post
    if str(user.id) not in xp_data:
        xp_data[str(user.id)] = {"xp": 0, "level": 1}

    # Ge användaren 10 extra XP och spara datan
    xp_data[str(user.id)]["xp"] += 10
    save_xp_data(xp_data)

    # Kontrollera om användaren ska gå upp i nivå
    await check_level_up(user, xp_update_channel_id)

# Kontrollera om användaren har tillräckligt med XP för att gå upp i nivå
async def check_level_up(user, xp_update_channel_id):
    user_data = xp_data.get(str(user.id), {})
    xp_needed = 100 * user_data.get("level", 1)

    if user_data["xp"] >= xp_needed:
        user_data["level"] += 1
        save_xp_data(xp_data)  # Spara data efter nivåuppgradering
        
        # Hämta kanalen och skicka uppdateringen där
        channel = user.guild.get_channel(xp_update_channel_id)
        if channel:
            await channel.send(f"{user.mention} has leveled up to level {user_data['level']}!")

# Visa en användares nivå och XP
async def show_level(ctx, member):
    user_data = xp_data.get(str(member.id))
    if user_data:
        await ctx.send(f"{member.mention} is at level {user_data['level']} with {user_data['xp']} XP.")
    else:
        await ctx.send(f"{member.mention} has no XP data yet.")

# Bearbeta alla historiska meddelanden och reaktioner när boten startar
async def process_historical_data(bot, xp_update_channel_id):
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                # Hämta alla meddelanden i kanalen
                async for message in channel.history(limit=None):
                    await handle_xp(message, xp_update_channel_id)
                    
                    # Hämta alla reaktioner för varje meddelande
                    for reaction in message.reactions:
                        users = await reaction.users().flatten()
                        for user in users:
                            if user != message.author:  # Exkludera författaren själv från att reagera på sitt eget inlägg
                                await handle_reaction_xp(message, xp_update_channel_id)
            except Exception as e:
                print(f"Could not process channel {channel.name}: {str(e)}")

########### Get Job Listings ###############

# API URL och API-nyckel för Indeed
INDEED_API_URL = "https://api.indeed.com/ads/apisearch"
INDEED_API_KEY = botConfig._YOUR_INDEED_API_KEY()  # API-Key in botConfig file

def fetch_jobs():
    jobs = []
    
    # API-parametrar för Indeed
    params = {
        'publisher': INDEED_API_KEY,
        'q': 'Nätverkstekniker',
        'l': 'Sweden',
        'sort': 'date',
        'format': 'json',
        'v': '2'
    }
    
    try:
        response = requests.get(INDEED_API_URL, params=params)
        response.raise_for_status()  # Kasta ett undantag om statuskoden inte är 200
        job_data = response.json()

        # Exempel på hur jobbdata kan extraheras från API:et
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

# Posta jobb i en specifik kanal
async def fetch_and_post_jobs(bot, job_channel_id):
    jobs = fetch_jobs()
    
    if not jobs:
        print("No jobs found.")
        return
    
    channel = bot.get_channel(job_channel_id)
    
    if not channel:
        print(f"Channel with ID {job_channel_id} not found.")
        return
    
    # Skicka jobb till kanalen
    for job in jobs:
        embed = discord.Embed(
            title=job['title'],
            description=f"{job['company']} - {job['location']}",
            url=job['url'],
            color=discord.Color.blue()
        )
        await channel.send(embed=embed)

################# Role Asigniments #################

# Funktion för att kontrollera om JSON-filen finns och är giltig
async def check_and_initialize_roles(bot):
    if not os.path.exists(ROLE_JSON_FILE) or os.path.getsize(ROLE_JSON_FILE) == 0:
        print("Role JSON file is missing or empty. Initializing...")
        await fetch_and_save_roles(bot)  # Hämta och spara roller om filen saknas eller är tom

# Funktion för att hämta alla roller från servern och spara dem i en JSON-fil
async def fetch_and_save_roles(bot):
    for guild in bot.guilds:
        roles_data = {}
        for role in guild.roles:
            roles_data[role.name] = role.id  # Spara rollnamn och roll-ID
        # Spara roller i en JSON-fil
        with open(ROLE_JSON_FILE, "w") as f:
            json.dump(roles_data, f, indent=4)
        print("Roles have been saved to roles.json")

# Funktion för att ge en användare en roll baserat på rollnamnet
async def assign_role(ctx, role_name=None):
    # Kontrollera om rollen finns i den sparade JSON-filen
    await check_and_initialize_roles(ctx.bot)  # Kontrollera om filen behöver initialiseras

    # Läs roller från JSON-filen
    with open(ROLE_JSON_FILE, "r") as f:
        roles_data = json.load(f)

    # Om ingen roll specificeras, lista alla tillgängliga roller
    if role_name is None:
        available_roles = [role for role in roles_data if role not in EXCLUDED_ROLES]
        if available_roles:
            roles_list = "\n".join(available_roles)
            await ctx.send(f"Available roles:\n{roles_list}")
        else:
            await ctx.send("No available roles to assign.")
        return

    # Kontrollera om den begärda rollen finns
    if role_name not in roles_data:
        await ctx.send(f"The role '{role_name}' does not exist.")
        return

    # Kontrollera om rollen är en av de exkluderade rollerna
    if role_name in EXCLUDED_ROLES:
        await ctx.send(f"You cannot assign the role '{role_name}'.")
        return

    # Hämta rollen från servern baserat på dess ID
    role_id = roles_data[role_name]
    role = discord.utils.get(ctx.guild.roles, id=role_id)

    if not role:
        await ctx.send(f"The role '{role_name}' could not be found on the server.")
        return

    # Tilldela rollen till användaren
    if role in ctx.author.roles:
        await ctx.send(f"You already have the role '{role_name}'.")
    else:
        await ctx.author.add_roles(role)
        await ctx.send(f"The role '{role_name}' has been assigned to you.")

########################################################################################

# Definiera roller och knapparnas utseende (text och färg)
ROLE_BUTTONS = [
    {"label": "NIT_24", "style": discord.ButtonStyle.green},
    {"label": "NIT_23", "style": discord.ButtonStyle.blurple},
    {"label": "NIT_22", "style": discord.ButtonStyle.red},
    {"label": "Annat start-år", "style": discord.ButtonStyle.gray},
    {"label": "Påbyggnadsåret!", "style": discord.ButtonStyle.green},
    {"label": "Kårfrälst", "style": discord.ButtonStyle.gray},
]

# Skapar eller laddar JSON-filen som lagrar meddelande-ID
def get_welcome_message_id():
    if os.path.exists(WELCOME_MESSAGE_FILE):
        with open(WELCOME_MESSAGE_FILE, "r") as f:
            data = json.load(f)
            return data.get("message_id", None)
    return None

def save_welcome_message_id(message_id):
    with open(WELCOME_MESSAGE_FILE, "w") as f:
        json.dump({"message_id": message_id}, f)

# Hantera rolltilldelning när en knapp klickas
class RoleButton(Button):
    def __init__(self, label, style):
        super().__init__(label=label, style=style)

    async def callback(self, interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name=self.label)
        if role:
            # Kolla om användaren redan har rollen
            if role in interaction.user.roles:
                await interaction.response.send_message(f"You already have the role {role.name}.", ephemeral=True)
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"The role {role.name} has been assigned to you.", ephemeral=True)
        else:
            await interaction.response.send_message(f"The role {self.label} could not be found on the server.", ephemeral=True)

# Skapa en vy med knappar för roller
def create_role_buttons_view():
    view = View()
    for button_info in ROLE_BUTTONS:
        button = RoleButton(label=button_info["label"], style=button_info["style"])
        view.add_item(button)
    return view

# Funktion för att skapa välkomstmeddelandet
async def post_welcome_message(channel):
    embed = discord.Embed(
        title="Welcome to the HV - NIT + Påbyggnadsår",
        description=(
            "Hej!\n"
            "Detta är NIT programmets Discord server! (Välkommen in i NIT kyrkan)\n"
            "Vi har en unik årgångs kanal som man får tillgång till genom roller.\n\n"
            "I kategorin PLUGG! har vi Kurssnack Kanaler där det är en för år 1, en för år 2, och en för år 3 (påbyggnadsåret). "
            "Och ett forum för labb (Praktiska moment i programmet).\n"
            "Så sitter ni i labbsalen eller med PT och svär över att ni inte får till det, "
            "så kan ni skapa en tråd eller läsa om det finns något där som kan hjälpa er!\n\n"
            "Vi vill även kunna behålla de nitare som gått vidare och börjat jobba. "
            "De kanske har lite tips inför jobblivet, eller en vacker dag kanske söker de personal eller sommarjobbare. "
            "#livet-efter-nit"
        ),
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="Servern är för dig",
        value=(
            "* Serverns drivs och ägs av studenter, för studenter på NIT-programmet och Påbyggnadsåret.\n"
            "* Studenterna är den huvudsakliga målgruppen.\n"
            "* Tänk på att servern är öppen, vem som helst kan hoppa in här (skriv inget olämpligt eller \"hemligt\").\n"
            "* Servern blir bara så bra som vi gör den till.\n"
            "* Bidra till ett trevligt klimat."
        ),
        inline=False
    )
    
    embed.add_field(
        name="Moderation",
        value="Mods [Privilage 10] och Admins [Privilage 15] håller ett extra öga på denna Discord, "
              "men i huvudsak anser vi att alla är vuxna och kan bete sig därefter!",
        inline=False
    )
    
    embed.add_field(
        name="Välkommen!",
        value="Tryck på en knapp nedan för att sätta din årskurs och komma igång.\n\n"
              "Välkommen!\n//Admins",
        inline=False
    )
    
    # Skicka det inbäddade meddelandet med knapparna
    view = create_role_buttons_view()
    message = await channel.send(embed=embed, view=view)
    
    # Spara meddelande-ID
    save_welcome_message_id(message.id)

# Funktion för att kontrollera och säkerställa att välkomstmeddelandet finns
async def ensure_welcome_message(bot, channel_id):
    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"Channel with ID {channel_id} not found.")
        return
    
    message_id = get_welcome_message_id()
    
    if message_id:
        try:
            # Försök att hämta det befintliga meddelandet
            message = await channel.fetch_message(message_id)
            return  # Meddelandet finns, inget mer behövs göra
        except discord.NotFound:
            pass  # Meddelandet hittades inte, vi postar om det
    
    # Skapa ett nytt välkomstmeddelande
    await post_welcome_message(channel)

    ########################################################################################