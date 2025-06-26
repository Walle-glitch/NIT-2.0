# Temporary stub module to satisfy Ticket_System import

import discord
from discord.ext import tasks


def setup_ticketer(bot):
    """
    Placeholder setup function for ticket system integration.
    Registers no-op commands and background tasks to allow the bot to start without errors.
    """
    # No-op: temporarily disable ticket commands
    @bot.tree.command(name="ticket", description="(Disabled) Create a support ticket temporarily")
    async def create_ticket_command(interaction: discord.Interaction):
        await interaction.response.send_message("Ticket system is temporarily disabled.", ephemeral=True)

    @bot.tree.command(name="close_ticket", description="(Disabled) Close the ticket temporarily")
    async def close_ticket_command(interaction: discord.Interaction):
        await interaction.response.send_message("Ticket system is temporarily disabled.", ephemeral=True)

    # Placeholder background task
    @tasks.loop(hours=24)
    async def dummy_task():
        pass

    dummy_task.start()
