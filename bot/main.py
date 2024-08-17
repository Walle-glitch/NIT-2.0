import os
import discord
import sys
import subprocess
import asyncio
from discord.ext import commands, tasks
from urllib.request import urlopen
import botConfig  # Bot-token och annan konfiguration kommer från denna modul

# Make sure to update this =) We use YY/MM/DD.VERSION-NR
verson_nr = "Current Version is 24/08/17.10"

# Setup för intents
intents = discord.Intents.all()
intents.message_content = True
#client = discord.Client(intents=intents)
# Skapa en bot med ett specifikt kommando-prefix
bot = commands.Bot(command_prefix="./", intents=intents)

# Full Access to the Bot... 
BOT_ADMIN_ROLE_NAME = "Bot-Master"

# Bekräftelse att boten är online
@bot.event
async def on_ready():
    print(f'Vi har loggat in som {bot.user}')

#
#           Example for a Simple Command: 
#@bot.command()
#async def NAME_OF_THE_COMMAND(ctx):
#    Reply = 'String Output' 
#    await ctx.send(Reply)  # This sends the reply
#

# Kommandon som användaren kan använda
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
        # Kör ping-kommandot till den angivna IP-adressen (eller standard: 8.8.8.8)
        result = subprocess.run(["ping", "-c", "4", ip], capture_output=True, text=True)
        
        # Skicka utdata från ping-kommandot till Discord-kanalen
        await ctx.send(f"Ping resultat för {ip}:\n```\n{result.stdout}\n```")
    except subprocess.CalledProcessError as e:
        # Hantera fel och skicka ett meddelande om något går fel
        await ctx.send(f"Fel vid körning av ping:\n```\n{e.stderr}\n```")

# Kommandot som kör en `git pull` och startar om boten (endast för administratörer)
@bot.command(name="Reboot")
@commands.has_role(BOT_ADMIN_ROLE_NAME)  # Kontrollera om användaren har adminrollen
async def reboot(ctx):
    await ctx.send("Kör `git pull` och startar om boten...")

    # Kör git pull i botens directory
    try:
        result = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
        await ctx.send(f"`git pull` utförd:\n```\n{result.stdout}\n```")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"Fel vid `git pull`:\n```\n{e.stderr}\n```")
        return

    # Spara nuvarande python-exekveringsfil (dvs scriptets namn)
    python = sys.executable

    # Starta om processen genom att köra om samma script
    os.execl(python, python, *sys.argv)

# Hantera fel om någon utan adminrollen försöker använda kommandot
@reboot.error
async def reboot_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Du har inte behörighet att använda detta kommando.")

# Kör boten med token från modulen bot
bot.run(botConfig._Bot_Token())
