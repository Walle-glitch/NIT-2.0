# Internal_Modules/_Ticket_System.py
import discord
from discord.ext import commands
from _logging_setup import setup_logging  # CORRECTED IMPORT

logger = setup_logging()

def setup(bot: commands.Bot):
    """Initializes the Ticket System module."""
    # The setup function registers the view so it persists across bot restarts.
    bot.add_view(TicketView())
    logger.info("Ticket System module setup complete.")

class TicketView(discord.ui.View):
    def __init__(self):
        # Setting a custom_id makes the view persistent
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.green, custom_id="create_ticket_button_persistent")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Creates a new private ticket channel for the user."""
        guild = interaction.guild
        # It's good practice to have a dedicated category for tickets
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            try:
                # Create the category if it doesn't exist
                category = await guild.create_category("Tickets")
            except discord.Forbidden:
                await interaction.response.send_message("I don't have permissions to create a category for tickets.", ephemeral=True)
                return

        # Permissions for the new ticket channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            # You can add roles for support staff here
            # For example, a role named "Support"
            # support_role = discord.utils.get(guild.roles, name="Support")
            # if support_role:
            #     overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        try:
            channel = await guild.create_text_channel(
                name=f"ticket-{interaction.user.name}",
                category=category,
                overwrites=overwrites,
                topic=f"Ticket created by {interaction.user.name} ({interaction.user.id})"
            )
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permissions to create a ticket channel.", ephemeral=True)
            return
        except Exception as e:
            logger.error(f"Failed to create ticket channel: {e}")
            await interaction.response.send_message("An error occurred while creating your ticket.", ephemeral=True)
            return

        await interaction.response.send_message(f"Your ticket has been created! Please go to {channel.mention}", ephemeral=True)
        
        # Send a welcome message in the new ticket channel
        await channel.send(f"Welcome {interaction.user.mention}! A staff member will be with you shortly. Please describe your issue in detail.")