# Internal_Modules/_Member_Moderation.py
import discord
from discord import app_commands
from discord.ext import commands
import _Bot_Config              # CORRECTED IMPORT
from _logging_setup import setup_logging  # CORRECTED IMPORT

logger = setup_logging()

# --- CORRECTED SETUP FUNCTION ---
def setup(bot: commands.Bot):
    """Initializes the moderation module and registers its slash commands."""

    admin_channel_id = _Bot_Config._Admin_Channel_ID()

    # The command definition MUST be inside the setup function
    @bot.tree.command(name="moderate", description="Moderates a member (kick or ban).")
    @app_commands.describe(action="The moderation action to take.", member="The member to moderate.", reason="The reason for the moderation action.")
    @app_commands.choices(action=[
        app_commands.Choice(name="Kick", value="kick"),
        app_commands.Choice(name="Ban", value="ban"),
    ])
    async def moderate(interaction: discord.Interaction, action: app_commands.Choice[str], member: discord.Member, reason: str):
        # A proper permission check is crucial for moderation commands
        if not interaction.user.guild_permissions.administrator and not discord.utils.get(interaction.user.roles, name=_Bot_Config._Bot_Admin_Role_Name()):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        embed = discord.Embed(title=f"User {action.name.capitalize()}", color=discord.Color.red())
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)

        try:
            if action.value == "kick":
                await member.kick(reason=reason)
                await interaction.response.send_message(embed=embed)
            elif action.value == "ban":
                await member.ban(reason=reason)
                await interaction.response.send_message(embed=embed)

        except discord.Forbidden:
            await interaction.response.send_message("I don't have the required permissions to perform this action.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An unexpected error occurred: {e}", ephemeral=True)
            logger.error(f"Error during moderation command: {e}", exc_info=True)

    logger.info("Member Moderation module setup complete.")