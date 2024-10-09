# This is _Bot_Modul.py

###########################################_Import_Modules_##########################################

import requests
from bs4 import BeautifulSoup
import discord
import _Bot_Config # type: ignore
from datetime import datetime

################  Global Refs ################

LOG_TO_CHANNEL_ID = _Bot_Config._Log_To_Channel_ID()  # The Discord channel ID where logs are sent
ADMIN_CHANNEL_ID = _Bot_Config._Admin_Channel_ID()  # Admin Channel ID




######### Utility Functions for Logging #########

async def log_to_channel(bot, message):
    """
    Sends a message to the logging channel and prints to the server logs.
    """
    print(message)  # Print to server logs
    channel = bot.get_channel(LOG_TO_CHANNEL_ID)
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


########### Get Job Listings ###############

# API URL and API key for Indeed
INDEED_API_URL = "https://api.indeed.com/ads/apisearch"
INDEED_API_KEY = _Bot_Config._YOUR_INDEED_API_KEY()

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

########################################################################################

########################################################################################