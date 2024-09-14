import discord  # Main Discord library for building bots
from datetime import datetime  # For handling date and time operations
import json  # For handling JSON data
import os  # For interacting with the operating system
import asyncio  # Asynchronous I/O handling, used extensively in Discord bots
import aiohttp  # For making HTTP requests to the GitHub API
import sys  # System-specific parameters and functions

sys.path.append(os.path.join(os.path.dirname(__file__), 'Internal_Modules'))

import _Bot_Config 

# Global variables
GITHUB_TOKEN = _Bot_Config._GITHUB_TOKEN()  # Replace with your GitHub token
MENTOR_ROLE = _Bot_Config._Mentor_Role_Name() # Role to ping in the ticket system
TICKET_CATEGORY_ID = _Bot_Config._Ticket_Category_ID()  # Ticket Category ID
ARCHIVE_CATEGORY_ID = _Bot_Config._Archive_Category_ID() # Archive Category ID
TICKET_COUNTER_FILE = _Bot_Config._ticket_counter_File()  # File to store last ticket number
GITHUB_API_URL = _Bot_Config._Github_API_URL()

INACTIVITY_TIMEOUT_DAYS = 2  # Timeout for ticket inactivity before archiving

def setup(bot):
    # Function to load the last ticket number from the file
    def load_ticket_counter():
        if os.path.exists(TICKET_COUNTER_FILE):
            with open(TICKET_COUNTER_FILE, "r") as file:
                data = json.load(file)
                return data.get("last_ticket_number", 0)
        else:
            return 0

    # Function to save the current ticket number to the file
    def save_ticket_counter(ticket_number):
        with open(TICKET_COUNTER_FILE, "w") as file:
            json.dump({"last_ticket_number": ticket_number}, file)

    # Function to generate the next ticket number (incrementing)
    def get_next_ticket_number():
        last_ticket_number = load_ticket_counter()
        next_ticket_number = (last_ticket_number + 1) % 10000  # Reset to 0001 after 9999
        save_ticket_counter(next_ticket_number)
        return f"{next_ticket_number:04d}"  # Zero-padded 4-digit number

    # Function to create a new ticket
    async def create_ticket(guild, category_id, user, channel_name=None):
        category = discord.utils.get(guild.categories, id=category_id)
        if not category:
            return None

        if not channel_name:
            ticket_number = get_next_ticket_number()  # Get the next ticket number
            channel_name = f"ticket-{ticket_number}"

        # Create the ticket in the category
        channel = await guild.create_text_channel(channel_name, category=category)

        # Send the welcome message in the ticket
        await channel.send(f"Hello {user.mention}, thank you for creating a ticket. Please describe your issue. Use `/close_ticket` to close it.")

        # Ping the Mentor role
        mentor_role = discord.utils.get(guild.roles, name=MENTOR_ROLE)
        if mentor_role:
            await channel.send(f"{mentor_role.mention}, please assist with this ticket.")

        # Check inactivity and handle it asynchronously
        asyncio.create_task(check_inactivity(channel))

        return channel

    # Slash command to create a ticket
    @bot.tree.command(name="ticket", description="Create a support ticket")
    async def create_ticket_command(interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        channel = await create_ticket(guild, TICKET_CATEGORY_ID, user)

        if channel:
            await interaction.response.send_message(f"Your ticket has been created: {channel.mention}", ephemeral=True)
        else:
            await interaction.response.send_message("Failed to create the ticket. Please contact an administrator.", ephemeral=True)

    # Slash command to close a ticket
    @bot.tree.command(name="close_ticket", description="Close your ticket")
    async def close_ticket_command(interaction: discord.Interaction):
        channel = interaction.channel
        user = interaction.user

        # Check if the channel is a ticket
        if channel.name.startswith('ticket-'):
            # Check if the user is a Mentor or the ticket creator
            mentor_role = discord.utils.get(interaction.guild.roles, name=MENTOR_ROLE)
            if mentor_role in user.roles or interaction.channel.permissions_for(user).manage_channels:
                await close_ticket(channel)
                await interaction.response.send_message("This ticket has been closed.", ephemeral=True)
            else:
                await interaction.response.send_message("You don't have permission to close this ticket.", ephemeral=True)
        else:
            await interaction.response.send_message("This command can only be used in ticket channels.", ephemeral=True)

    # Function to close the ticket
    async def close_ticket(channel):
        await channel.send("This ticket is now being closed.")
        await archive_ticket(channel)

    # Check for inactivity and archive the ticket after the specified timeout
    async def check_inactivity(channel):
        last_activity_time = datetime.now()
        while True:
            await asyncio.sleep(3600)  # Check every hour
            if (datetime.now() - last_activity_time).days >= INACTIVITY_TIMEOUT_DAYS:
                await archive_ticket(channel)
                break
            last_message = (await channel.history(limit=1).flatten())[0]
            last_activity_time = last_message.created_at

    # Archive the ticket
    async def archive_ticket(channel):
        archive_category = discord.utils.get(channel.guild.categories, id=ARCHIVE_CATEGORY_ID)
        if archive_category:
            await channel.edit(category=archive_category)
            await channel.send("This ticket has been archived.")
        else:
            await channel.send("Failed to archive the ticket. Archive category not found.")

    # Function to create a GitHub issue
    async def create_github_issue(title, body, labels=None):
        url = GITHUB_API_URL.format(owner="your_github_username", repo="your_repository")
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        data = {
            "title": title,
            "body": body,
            "labels": labels or []
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 201:
                    return await response.json()  # Issue successfully created
                else:
                    return await response.json()  # Handle errors

    # Slash command to create a GitHub issue
    @bot.tree.command(name="issue", description="Create a GitHub issue")
    async def create_github_issue_command(interaction: discord.Interaction, title: str, *, description: str):
        await interaction.response.send_message(f"Creating GitHub issue: {title}...", ephemeral=True)
        issue = await create_github_issue(title, description)

        if issue.get("html_url"):
            await interaction.followup.send(f"Issue created successfully: {issue['html_url']}", ephemeral=True)
        else:
            await interaction.followup.send(f"Failed to create issue: {issue.get('message', 'Unknown error')}", ephemeral=True)

    # Help Command
    def load_help_commands():
        help_commands = "Json_Files/Help_Commands.json"
        if os.path.exists(help_commands):
            with open(help_commands, "r") as file:
                return json.load(file)
        else:
            print(f"Error: {help_commands} not found.")
            return None

    @bot.tree.command(name="help", description="Get information on what commands are available")
    async def help_command(interaction: discord.Interaction):
        try:
            help_data = load_help_commands()
            if help_data:
                version_nr = help_data.get("version", "Unknown Version")
                commands_list = help_data.get("commands", {})

                embed = discord.Embed(
                    title="Available Commands",
                    description=f"Current version: {version_nr}\n\nHere is a list of all available commands:",
                    color=discord.Color.blue()
                )

                for command, description in commands_list.items():
                    embed.add_field(name=command, value=description, inline=False)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message("Error loading help commands.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)
