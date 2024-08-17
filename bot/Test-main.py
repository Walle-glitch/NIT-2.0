import os
import discord
import sys
import subprocess
import asyncio
from discord.ext import commands, tasks
from urllib.request import urlopen
import botConfig  # Bot-token och annan konfiguration kommer från denna modul

# Setup för intents
intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
# Skapa en bot med ett specifikt kommando-prefix
bot = commands.Bot(command_prefix="./", intents=intents)

# Full Access to the Bot... 
BOT_ADMIN_ROLE_NAME = "Bot-Master"

# Bekräftelse att boten är online
@bot.event
async def on_ready():
    print(f'Vi har loggat in som {bot.user}')

# Kommandon som användaren kan använda
@bot.command()
async def git(ctx):
    Reply = 'https://github.com/Walle-glitch/NIT-2.0.git'
    await ctx.send(Reply)
    
@bot.command()
async def who(ctx):
    Reply = 'I am the NIT-BOT, use ./git to get my GitHub link.'
    await ctx.send(Reply)

@bot.command()
async def hello(ctx):
    Reply = 'Hello! I am the NIT-Bot and exist on GitHub. Feel free to contribute! Current commands: ./git, ./who, ./hello... Add more if you wish!'
    await ctx.send(Reply)

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
client.run(botConfig._Bot_Token())
