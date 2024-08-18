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
verson_nr = "Current Version is 24/08/18.1"

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
# Help = h  #
async def h(ctx):
    Reply = 'you can use the following: ./h , ./git , ./hello , ./about ./ping [and a IP if you wish] , ./rfc [number] , ./version for the Bot version.  The role "Bot-Master" can reboot and initiate a "git pull" using ./Reboot'
    await ctx.send(Reply)
# Version Number # 
@bot.command()
async def version(ctx):
    Reply = verson_nr
    await ctx.send(Reply)
# git #
@bot.command()
async def git(ctx):
    Reply = 'https://github.com/Walle-glitch/NIT-2.0.git'
    await ctx.send(Reply)
# hello #
@bot.command()
async def hello(ctx):
    Reply = 'Hello?'
    await ctx.send(Reply)
# Version number # 
@bot.command()
async def about(ctx):
    Reply = 'The NIT-BOT is a for fun bot here on our Diacord, Its Public on github and anyone is free to contribiute to it, ether for fun or another (non malicious) projects. The Server its hosted on is at my home so its behind a normal (NAT Gateway) Contact Walle/Nicklas for more info Use ./git for the link to Github repo'
    await ctx.send(Reply) 
# PING # 
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
# Get an RFC # 
@bot.command()
async def rfc(ctx, rfc_number: str = None):
    """
    Hämtar och visar information om en RFC baserat på nummer.
    
    :param rfc_number: RFC-nummer att hämta. Om inget anges, visas ett felmeddelande.
    """
    if rfc_number is None:
        await ctx.send("Fel: Ingen RFC-nummer angivet. Vänligen ange ett RFC-nummer efter kommandot.")
        return

    try:
        # Konvertera rfc_number till heltal
        rfc_number = int(rfc_number)
        result = _Bot_Modul.get_rfc(rfc_number)
    except ValueError:
        # Hantera fallet där rfc_number inte kan konverteras till heltal
        result = "Fel: Ogiltigt RFC-nummer. Vänligen ange ett giltigt heltal."

    await ctx.send(result)

# Kommandot för att konfigurera BGP-peering
@bot.command()
async def BGP(ctx, bgp_neighbor_ip: str = "8.8.8.8", bgp_as_number: str = "65000", neighbor_as_number: str = "65001"):
    """
    Kör kommandot för att konfigurera en BGP-nabo via SSH på Cisco-routern.
    
    :param bgp_neighbor_ip: IP-adressen till BGP-nabon (default 8.8.8.8)
    :param bgp_as_number: Ditt lokala AS-nummer (default 65000)
    :param neighbor_as_number: AS-numret för din BGP-nabo (default 65001)
    """
    router_ip = "172.31.255.1"  # Cisco-routerns IP-adress
    
    await ctx.send(f"Försöker konfigurera BGP-peering med nabon {bgp_neighbor_ip}...")
    
    # Anropa funktionen för att konfigurera BGP
    result = _Bot_Modul.configure_bgp_neighbor(router_ip, bgp_neighbor_ip, bgp_as_number, neighbor_as_number)
    
    # Skicka tillbaka resultatet till användaren
    await ctx.send(result)




###########################################_Below this line_##########################################
###########################################_Work In progress_##########################################

# Rollnamn som ska tilldelas av boten
ROLE_NAME = "YourRoleName"  # Ändra detta till din roll som du vill att boten ska tilldela

@bot.command()
async def addrole(ctx):
    """
    Tilldelar en specifik roll till den användare som kör kommandot.
    Använder ett inbäddat meddelande för att ge feedback.
    """
    role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
    
    if role is None:
        await ctx.send(f"Roll '{ROLE_NAME}' kunde inte hittas på servern.")
        return

    if role in ctx.author.roles:
        embed = discord.Embed(title="Roll tilldelad", description=f"Du har redan rollen **{ROLE_NAME}**.", color=discord.Color.orange())
    else:
        try:
            await ctx.author.add_roles(role)
            embed = discord.Embed(title="Roll tilldelad", description=f"Rollen **{ROLE_NAME}** har tilldelats dig!", color=discord.Color.green())
        except discord.Forbidden:
            embed = discord.Embed(title="Fel", description="Jag har inte tillräckliga rättigheter för att tilldela denna roll.", color=discord.Color.red())
    
    # Skicka ett inbäddat meddelande som svar
    await ctx.send(embed=embed)

@bot.command()
async def removerole(ctx):
    """
    Tar bort en specifik roll från den användare som kör kommandot.
    Använder ett inbäddat meddelande för att ge feedback.
    """
    role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
    
    if role is None:
        await ctx.send(f"Roll '{ROLE_NAME}' kunde inte hittas på servern.")
        return

    if role not in ctx.author.roles:
        embed = discord.Embed(title="Roll borttagen", description=f"Du har inte rollen **{ROLE_NAME}**.", color=discord.Color.orange())
    else:
        try:
            await ctx.author.remove_roles(role)
            embed = discord.Embed(title="Roll borttagen", description=f"Rollen **{ROLE_NAME}** har tagits bort från dig.", color=discord.Color.green())
        except discord.Forbidden:
            embed = discord.Embed(title="Fel", description="Jag har inte tillräckliga rättigheter för att ta bort denna roll.", color=discord.Color.red())
    
    # Skicka ett inbäddat meddelande som svar
    await ctx.send(embed=embed)

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


# Roll-ID:n för roller som ska tilldelas
ROLE_EMOJI_MAP = {
    "🟢": "Role1_ID",  # Grön emoji motsvarar roll 1
    "🔵": "Role2_ID",  # Blå emoji motsvarar roll 2
    "🔴": "Role3_ID",  # Röd emoji motsvarar roll 3
}

# Kommandot för att skapa ett inbäddat meddelande med reaktionsroller
@bot.command()
@commands.has_permissions(administrator=True)  # Endast administratörer kan köra detta kommando
async def setup_roles(ctx):
    """
    Skapar ett inbäddat meddelande för rolltilldelning via reaktioner.
    """
    embed = discord.Embed(
        title="Välj din roll!",
        description="Reagera med en emoji för att få motsvarande roll:\n\n"
                    "🟢 - Grön Roll\n"
                    "🔵 - Blå Roll\n"
                    "🔴 - Röd Roll\n",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Klicka på en emoji för att få en roll tilldelad.")
    
    # Skicka det inbäddade meddelandet
    message = await ctx.send(embed=embed)
    
    # Lägg till reaktionerna (emoji) till meddelandet
    for emoji in ROLE_EMOJI_MAP.keys():
        await message.add_reaction(emoji)

# Event för att lyssna på reaktioner och tilldela roller
@bot.event
async def on_raw_reaction_add(payload):
    """
    Event som hanterar rolltilldelning när en användare reagerar på ett meddelande.
    """
    if payload.message_id == MESSAGE_ID:  # Byt ut detta mot meddelande-ID för ditt inbäddade meddelande
        guild = bot.get_guild(payload.guild_id)
        role_id = ROLE_EMOJI_MAP.get(str(payload.emoji))
        
        if role_id:
            role = guild.get_role(int(role_id))
            member = guild.get_member(payload.user_id)
            
            if role and member:
                await member.add_roles(role)
                try:
                    await member.send(f"Du har tilldelats rollen: {role.name}")
                except discord.Forbidden:
                    pass  # Ignorera om användaren har stängt av direktmeddelanden

# Event för att hantera borttagning av roller när en användare tar bort sin reaktion
@bot.event
async def on_raw_reaction_remove(payload):
    """
    Event som hanterar borttagning av roller när en användare tar bort sin reaktion.
    """
    if payload.message_id == MESSAGE_ID:  # Byt ut detta mot meddelande-ID för ditt inbäddade meddelande
        guild = bot.get_guild(payload.guild_id)
        role_id = ROLE_EMOJI_MAP.get(str(payload.emoji))
        
        if role_id:
            role = guild.get_role(int(role_id))
            member = guild.get_member(payload.user_id)
            
            if role and member:
                await member.remove_roles(role)
                try:
                    await member.send(f"Rollen {role.name} har tagits bort från dig.")
                except discord.Forbidden:
                    pass  # Ignorera om användaren har stängt av direktmeddelanden

# Exe the bot using its token. 
bot.run(botConfig._Bot_Token())

