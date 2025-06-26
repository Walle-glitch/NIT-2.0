# Internal_Modules/_Member_Moderation.py
"""
Module to handle member moderation: kick, ban, mute actions with logging and reporting.
"""
import logging
from datetime import datetime, timedelta

import discord
from discord.ext import commands

import _Bot_Config  # type: ignore
from _logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

# Admin channel ID (to be set by main)
ADMIN_CHANNEL_ID: int = None


def setup(admin_channel_id: int):
    """Configure the admin channel ID for reporting moderation actions."""
    global ADMIN_CHANNEL_ID
    ADMIN_CHANNEL_ID = admin_channel_id
    logger.info(f"MemberModeration: set ADMIN_CHANNEL_ID={ADMIN_CHANNEL_ID}")


def has_privileged_role(member: discord.Member) -> bool:
    """Return True if member has admin, mod, or bot-admin role."""
    role_names = [role.name for role in member.roles]
    return (
        _Bot_Config._Admin_Role_Name() in role_names or
        _Bot_Config._Mod_Role_Name() in role_names or
        _Bot_Config._Bot_Admin_Role_Name() in role_names
    )


async def report_action(ctx: commands.Context, user: discord.Member, action: str,
                        reason: str = None, duration: int = None):
    """Send a report of the moderation action to the admin channel."""
    if not ADMIN_CHANNEL_ID:
        logger.warning("Admin channel ID not set; skipping report_action.")
        return

    guild = ctx.guild
    report_channel = guild.get_channel(ADMIN_CHANNEL_ID) if guild else None
    if not report_channel:
        logger.error(f"Cannot find admin channel {ADMIN_CHANNEL_ID}")
        return

    admin = ctx.author.name
    target = user.name
    if action == "mute":
        msg = f"**{admin}** muted **{target}** for {duration}h. Reason: {reason}"
    else:
        msg = f"**{admin}** {action}ed **{target}**. Reason: {reason}"

    try:
        await report_channel.send(msg)
        logger.info(f"Reported {action} action: {msg}")
    except Exception as e:
        logger.error(f"Failed to send report: {e}")


@commands.check(lambda ctx: has_privileged_role(ctx.author))
@commands.has_permissions(kick_members=True)
async def kick_user(ctx: commands.Context, user: discord.Member, *, reason: str = None):
    """Kick a user from the guild."""
    try:
        await user.kick(reason=reason)
        await report_action(ctx, user, "kick", reason)
        await ctx.send(f"Kicked {user.mention}. Reason: {reason}")
        logger.info(f"{ctx.author} kicked {user} for: {reason}")
    except discord.Forbidden:
        await ctx.send("I lack permission to kick this user.")
        logger.warning(f"Kick forbidden: {ctx.author} -> {user}")
    except Exception as e:
        await ctx.send(f"Error kicking user: {e}")
        logger.error(f"Exception kicking {user}: {e}")


@commands.check(lambda ctx: has_privileged_role(ctx.author))
@commands.has_permissions(ban_members=True)
async def ban_user(ctx: commands.Context, user: discord.Member, *, reason: str = None):
    """Ban a user from the guild."""
    try:
        await user.ban(reason=reason)
        await report_action(ctx, user, "ban", reason)
        await ctx.send(f"Banned {user.mention}. Reason: {reason}")
        logger.info(f"{ctx.author} banned {user} for: {reason}")
    except discord.Forbidden:
        await ctx.send("I lack permission to ban this user.")
        logger.warning(f"Ban forbidden: {ctx.author} -> {user}")
    except Exception as e:
        await ctx.send(f"Error banning user: {e}")
        logger.error(f"Exception banning {user}: {e}")


@commands.check(lambda ctx: has_privileged_role(ctx.author))
@commands.has_permissions(moderate_members=True)
async def mute_user(ctx: commands.Context, user: discord.Member,
                    duration: int, *, reason: str = None):
    """Timeout (mute) a user for a specified duration in hours."""
    try:
        until = datetime.utcnow() + timedelta(hours=duration)
        await user.timeout(until, reason=reason)
        await report_action(ctx, user, "mute", reason, duration)
        await ctx.send(f"Muted {user.mention} for {duration}h. Reason: {reason}")
        logger.info(f"{ctx.author} muted {user} for {duration}h: {reason}")
    except discord.Forbidden:
        await ctx.send("I lack permission to mute this user.")
        logger.warning(f"Mute forbidden: {ctx.author} -> {user}")
    except Exception as e:
        await ctx.send(f"Error muting user: {e}")
        logger.error(f"Exception muting {user}: {e}")