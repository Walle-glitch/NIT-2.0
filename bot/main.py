import os
import discord
import sys
import subprocess
import asyncio
from discord.ext import commands, tasks
from urllib.request import urlopen
import botConfig  # Bot-token and Bot info exists Localy on the server, This Mod contains that info. 
import _Bot_Modul # use this if you want to write functions. 

# Make sure to update this =) We use YY/MM/DD.VERSION-NR
verson_nr = "Current Version is 24/08/17.11"

# Setup for intents
intents = discord.Intents.all()
intents.message_content = True
# The following line makes sure all commands in the server neds to use "./" in fromt of the command
bot = commands.Bot(command_prefix="./", intents=intents)

# The wollowing roles have access to "Sudo commands" 
BOT_ADMIN_ROLE_NAME = "Bot-Master"

# a verification on the server that the bot is alive. 
@bot.event
async def on_ready():
    print(f'Vi har loggat in som {bot.user}')





###########################################_Below this line_##########################################
#############################################_All users_##############################################
###########################################_can run the code_#########################################
#
#           Example for a Simple Command: 
#@bot.command()
#async def NAME_OF_THE_COMMAND(ctx):
#    Reply = 'String Output' 
#    await ctx.send(Reply)  # This sends the reply
#

@bot.command()  # UPDATE THIS ONE WHEN YOU ADD A NEW FUNCTION
async def help(ctx):
    Reply = 'you can use the following: ./git , ./Hello , ./about ./ping [and a IP if you wish] The role "Bot-Master" can reboot and initiate a "git pull" using ./reboot'
    await ctx.send(Reply)
    
@bot.command()
async def git(ctx):
    Reply = 'https://github.com/Walle-glitch/NIT-2.0.git'
    await ctx.send(Reply)

@bot.command()
async def hello(ctx):
    Reply = 'Hello?'
    await ctx.send(Reply)

@bot.command()
async def about(ctx):
    Reply = verson_nr
    await ctx.send(Reply, 'The NIT-BOT is a for fun bot here on our Diacord, Its Public on github and anyone is free to contribiute to it, ether for fun or another (non malicious) projects. The Server its hosted on is at my home so its behind a normal (NAT Gateway) Contact Walle/Nicklas for more info Use ./git for the link to Github repo') 
#
@bot.command()
async def ping(ctx, ip: str = "8.8.8.8"):
    """
    Gör ett ping-test till en given IP-adress. Om ingen IP-adress anges,
    används 8.8.8.8 som standard.
    """
    try:
        # Do the ping Command + a IP addr (If no IP is specified it will default to 8.8.8.8)
        result = subprocess.run(["ping", "-c", "4", ip], capture_output=True, text=True)
        
        # Sends The output of Ping to the server.
        await ctx.send(f"Ping resultat för {ip}:\n```\n{result.stdout}\n```")
    except subprocess.CalledProcessError as e:
        # If somthing goes wrong:
        await ctx.send(f"ERROR:\n```\n{e.stderr}\n```")

@bot.command()
async def rfc(ctx, rfc_number: int):
    """
    Hämtar och visar information om en RFC baserat på nummer.
    
    :param rfc_number: RFC-nummer att hämta.
    """
    result = _Bot_Modul.get_rfc(rfc_number)
    await ctx.send(result)


###########################################_Below this line_##########################################
###########################################_Only Admin Code_##########################################

# Command does a `git pull` reboots the bot (only the role "Bot-Master")
@bot.command(name="Reboot")
@commands.has_role(BOT_ADMIN_ROLE_NAME)  # Verify that the user has the correct role
async def reboot(ctx):
    await ctx.send("Kör `git pull` och startar om boten...")

    # Executes "git pull" directory
    try:
        result = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
        await ctx.send(f"`git pull` utförd:\n```\n{result.stdout}\n```")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"Fel vid `git pull`:\n```\n{e.stderr}\n```")
        return

    # Saves current Python."exe" file 
    python = sys.executable

    # Reboots the Python Script 
    os.execl(python, python, *sys.argv)

# Manages Errors if a none "Bot-Master" tries the command.
@reboot.error
async def reboot_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Du har inte behörighet att använda detta kommando.")

# Exe the bot using its token. 
bot.run(botConfig._Bot_Token())

