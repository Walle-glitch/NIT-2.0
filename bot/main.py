import os , discord , time , asyncio , sys , bot , asyncio
# Bot is BOT-INFO, Token key etc in that modul. 
#
from urllib.request import urlopen
from discord.ext import tasks
#
# Set up a Discord client
intents = discord.Intents.all()
intents.message_content = True
#
client = discord.Client(intents=intents)
#
# confermaton that bot is online;
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
#
#
@client.event
async def on_message(message):
    if message.author == client.user: # Making sure the bot dose not reply to it self. 
        return    
#
@client.event
async def on_message(message):
    if message.author == client.user: # Making sure the bot dose not reply to it self. 
        return 
    if message.content.startswith('./git'):
        Reply = 'https://github.com/Walle-glitch/NIT-2.0.git'
        await message.channel.send(Reply)
        return
    if message.content.startswith('./who'):
        Reply = 'I am the NIT-BOT, use ./bot to get my GitHub link.'
        await message.channel.send(Reply)
        return
    if message.content.startswith('./hello'):
        Reply = 'Hello! I am the NIT-Bot and exists on GitHub, Feel free to Commit to me ;) Curently only ./git , ./who and ./hello exits... Feal free to add more !' 
        await message.channel.send(Reply)
        return    
    return
#
#@client.event   
#async def on_message(message):
#    if message.author == client.user:
#        channel =  client.get_channel(CHANAL_ID)
#        return   
#    await channel.send(message)
#
# this line authenticats the bot, The Token string coms from the module bot. 
client.run(bot._Bot_Token())
#
