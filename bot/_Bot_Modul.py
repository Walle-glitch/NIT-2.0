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

######### The resourses ############ 

async def send_resource_embed(ctx):
    embed = discord.Embed(
        title="Course Books and Resources",
        description="",
        color=discord.Color.blue()
    )

    # <Big header>Course Books and Stuff<Big header>
    embed.add_field(name="**Course Books and Stuff**", value="\u200b", inline=False)
    
    # -Klickabel links, one per row-
    embed.add_field(name="[**linux (ogl) (Might Be old)**]", value="https://dl.remilia.se/os/", inline=False)
    embed.add_field(name="[**linux (ogl-tenta) (Might Be old)**]", value="https://www.studocu.com/sv/document/hogskolan-vast/operativsystem-med-gnulinux/ogl202-tentafragor-en-sammanfattning-fran-gamla-tenta-fragor-och-fragor-som-kan-uppkomma/10085924", inline=False)
    embed.add_field(name="[**python (most of it)**]", value="https://files.catbox.moe/tj6k7c.zip", inline=False)
    embed.add_field(name="[**ekonomi Kursen (Might Be old)**]", value="http://libgen.rs/book/index.php?md5=78A08A5D5329DF2BE639849653A0E199", inline=False)

    # <Small header>CWNA-107 (Old version but still good):<Small header>
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

    # <Two empty rows>
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # <Big header>Bloogs and "fun stuff"<Big header>
    embed.add_field(name="**Bloogs and \"fun stuff\"**", value="\u200b", inline=False)
    
    # -Klickabel links, one per row-
    embed.add_field(name="[**Cloudflare Blog**]", value="https://blog.cloudflare.com/making-phishing-defense-seamless-cloudflare-yubico/", inline=False)
    embed.add_field(name="[**Study tips**]", value="https://www-freecodecamp-org.cdn.ampproject.org/c/s/www.freecodecamp.org/news/supercharged-studying-with-python-anki-chatgpt/amp/", inline=False)
    embed.add_field(name="[**BEST cheat-sheets in the world**]", value="https://packetlife.net/library/cheat-sheets/", inline=False)

    # <Two empty rows>
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # <Big header>YouTube resources<Big header>
    embed.add_field(name="**YouTube resources**", value="\u200b", inline=False)
    
    # -Klickabel links, one per row-
    embed.add_field(name="[**CCNA**]", value="https://youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ&si=Z_ApQ1TJtE1EJqhB", inline=False)
    embed.add_field(name="[**Cybersäkerhet**]", value="https://www.youtube.com/watch?v=IQZXqUggR8w&list=PL1U-z6tCj5WBwy4WoMS3jSi7WE4AGOUcY", inline=False)
    embed.add_field(name="[**Blandat inför GDA kursen och lite för Internettjänster**]", value="https://www.youtube.com/watch?v=bYjQakUxeVY&list=PLdz-iDPGfMEJWW0JdbWwP0bCkBnJGP5q4", inline=False)
    embed.add_field(name="[**CCNA (Kompletteras bra med Jeremy)**]", value="https://www.youtube.com/watch?v=S7MNX_UD7vY&list=PLIhvC56v63IJVXv0GJcl9vO5Z6znCVb1P", inline=False)
    embed.add_field(name="[**CCNA**]", value="https://www.youtube.com/playlist?list=PLIhvC56v63IKrRHh3gvZZBAGvsvOhwrRF", inline=False)

    # <Two empty rows>
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # <Big header>Content creators on YouTube<Big header>
    embed.add_field(name="**Content creators on YouTube**", value="\u200b", inline=False)
    
    # -Klickabel links, one per row-
    embed.add_field(name="[**Indently**]", value="https://www.youtube.com/@Indently", inline=False)
    embed.add_field(name="[**Ccieordie**]", value="https://www.youtube.com/@Ccieordie_arteq", inline=False)
    embed.add_field(name="[**INE**]", value="https://www.youtube.com/@INEtraining", inline=False)
    embed.add_field(name="[**Art of Network Engineering**]", value="https://www.youtube.com/@artofneteng", inline=False)
    embed.add_field(name="[**kevin Wallace**]", value="https://www.youtube.com/@kwallaceccie", inline=False)
    embed.add_field(name="[**Keith Barker**]", value="https://www.youtube.com/@KeithBarker", inline=False)
    embed.add_field(name="[**Chris Greer**]", value="https://www.youtube.com/@ChrisGreer", inline=False)
    embed.add_field(name="[**David Bombal**]", value="https://www.youtube.com/@davidbombal", inline=False)
    embed.add_field(name="[**Jeremy's IT Lab**]", value="https://www.youtube.com/@JeremysITLab", inline=False)
    embed.add_field(name="[**Arthur Salmon**]", value="https://www.youtube.com/@arthursalmon3414", inline=False)
    embed.add_field(name="[**PowerCert Animated Videos**]", value="https://www.youtube.com/@PowerCertAnimatedVideos", inline=False)
    embed.add_field(name="[**NetworkChuck**]", value="https://www.youtube.com/@NetworkChuck", inline=False)

    # <Two empty rows>
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # <Big header>Good Downloads<Big header>
    embed.add_field(name="**Good Downloads**", value="\u200b", inline=False)
    
    # -Klickabel links, one per row-
    embed.add_field(name="[**(note taking) Notepad++**]", value="https://notepad-plus-plus.org/", inline=False)
    embed.add_field(name="[**(note taking) Obsidian**]", value="https://obsidian.md/", inline=False)
    embed.add_field(name="[**(Programming/ IDE) Visual Studio Code**]", value="https://code.visualstudio.com/", inline=False)
    embed.add_field(name="[**(Your best friend) Putty**]", value="https://www.putty.org/", inline=False)
    embed.add_field(name="[**(Flash Cards) Anki**]", value="https://apps.ankiweb.net/", inline=False)
    embed.add_field(name="[**(Packet Capture & Analyzer) Wireshark**]", value="https://www.wireshark.org/", inline=False)
    embed.add_field(name="[**(GNS3)**]", value="https://gns3.teachable.com/courses/", inline=False)
    embed.add_field(name="[**(Eve-ng)**]", value="https://www.eve-ng.net/", inline=False)

    # <Two empty rows>
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    # <Big header>Get an account<Big header>
    embed.add_field(name="**Get an account**", value="\u200b", inline=False)
    
    # -Klickabel links, one per row-
    embed.add_field(name="[**GitHub**]", value="https://github.com/", inline=False)
    embed.add_field(name="[**Credly**]", value="https://www.credly.com/", inline=False)
    embed.add_field(name="[**LinkedIn**]", value="https://www.linkedin.com/", inline=False)
    embed.add_field(name="[**Postman Student Program**]", value="https://www.postman.com/student-program/student-expert/", inline=False)

    # <Big header>AND!<Big header>
    embed.add_field(name="**AND!**", value="You can always ask if someone has something more ;) (Some stuff isn't given away for free, so to say)", inline=False)

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
