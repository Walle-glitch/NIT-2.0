import discord
import logging

logger = logging.getLogger(__name__)

ADMIN_CHANNEL_ID = None  # This will be set in the main file by importing the value from your config

def set_admin_channel_id(channel_id):
    global ADMIN_CHANNEL_ID
    ADMIN_CHANNEL_ID = channel_id

def has_privileged_role(ctx):
    """Checks if the user has a privileged role."""
    roles = [role.name for role in ctx.author.roles]
    return "Privilege 15" in roles or "Privilege 10" in roles

async def kick_user(ctx, user: discord.Member, reason=None):
    """Kicks a user from the server."""
    try:
        await user.kick(reason=reason)
        await report_action(ctx, user, "kick", reason)
        logger.info(f"{ctx.author} kicked {user} for {reason}")
    except discord.Forbidden:
        await ctx.send("I do not have permission to kick this user.")
        logger.warning(f"Kick attempt failed for {user}: Forbidden")
    except Exception as e:
        await ctx.send(f"An error occurred while kicking the user: {str(e)}")
        logger.error(f"Error kicking user {user}: {str(e)}")

async def ban_user(ctx, user: discord.Member, reason=None):
    """Bans a user from the server."""
    try:
        await user.ban(reason=reason)
        await report_action(ctx, user, "ban", reason)
        logger.info(f"{ctx.author} banned {user} for {reason}")
    except discord.Forbidden:
        await ctx.send("I do not have permission to ban this user.")
        logger.warning(f"Ban attempt failed for {user}: Forbidden")
    except Exception as e:
        await ctx.send(f"An error occurred while banning the user: {str(e)}")
        logger.error(f"Error banning user {user}: {str(e)}")

async def mute_user(ctx, user: discord.Member, duration_in_hours: int, reason=None):
    """Mutes a user for a specific duration."""
    try:
        duration_in_seconds = duration_in_hours * 3600
        await user.timeout(discord.utils.utcnow() + discord.timedelta(seconds=duration_in_seconds), reason=reason)
        await report_action(ctx, user, "mute", reason, duration_in_hours)
        logger.info(f"{ctx.author} muted {user} for {duration_in_hours} hours for {reason}")
    except discord.Forbidden:
        await ctx.send("I do not have permission to mute this user.")
        logger.warning(f"Mute attempt failed for {user}: Forbidden")
    except Exception as e:
        await ctx.send(f"An error occurred while muting the user: {str(e)}")
        logger.error(f"Error muting user {user}: {str(e)}")

async def report_action(ctx, user: discord.Member, action: str, reason=None, duration=None):
    """Sends a report of the moderation action to the admin channel."""
    if not ADMIN_CHANNEL_ID:
        return

    report_channel = ctx.guild.get_channel(ADMIN_CHANNEL_ID)
    if not report_channel:
        return

    admin_name = ctx.author.name
    user_name = user.name

    if action == "mute":
        report_message = f"**{admin_name}** muted **{user_name}** for {duration} hours. Reason: {reason}"
    else:
        report_message = f"**{admin_name}** {action}ed **{user_name}**. Reason: {reason}"

    await report_channel.send(report_message)
    logger.info(f"Report sent to admin channel: {report_message}")
