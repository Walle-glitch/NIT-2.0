# Internal_Modules/_Cisco_Study_Plans.py
"""
Unified module for CCNA, CCNP, and CCIE study plan management.
Each class provides static methods to load current week, fetch weekly goals,
post to Discord, and cycle weeks automatically.
"""
import discord
import json
import os
from datetime import datetime
from _logging_setup import setup_logging # CORRECTED IMPORT

import _Bot_Config  # type: ignore
from _logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

# Ensure JSON directory exists
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JSON_DIR = os.path.join(PROJECT_ROOT, 'Json_Files')
os.makedirs(JSON_DIR, exist_ok=True)


def _load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Study plan file not found: {path}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {path}")
    return {}


def _save_json(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Unable to save JSON to {path}: {e}")


class _BaseStudyPlan:
    def __init__(self, current_week_file, plan_file):
        self.current_week_file = current_week_file
        self.plan_file = plan_file

    def get_current_week(self) -> int:
        data = _load_json(self.current_week_file)
        week = data.get('current_week', 1)
        logger.debug(f"Loaded current week {week} from {self.current_week_file}")
        return week

    def save_current_week(self, week: int):
        _save_json(self.current_week_file, {'current_week': week})
        logger.debug(f"Saved current week {week} to {self.current_week_file}")

    def _all_weeks(self) -> list:
        raw = _load_json(self.plan_file)
        # Support two formats: dict of week=>info or list under 'weeks'
        if isinstance(raw, dict) and 'weeks' in raw:
            return raw['weeks']
        if isinstance(raw, dict):
            return [dict(week=int(k), **v) for k, v in raw.items() if k.isdigit()]
        if isinstance(raw, list):
            return raw
        return []

    def get_total_weeks(self) -> int:
        total = len(self._all_weeks())
        return total

    def get_weekly_goal(self, week: int) -> dict:
        weeks = self._all_weeks()
        for entry in weeks:
            if entry.get('week') == week:
                return entry
        logger.warning(f"No goal found for week {week} in {self.plan_file}")
        return {}

    async def post_weekly_goal(self, bot, channel_id: int):
        week = self.get_current_week()
        goal = self.get_weekly_goal(week)
        if not goal:
            logger.info(f"Skipping post: no goal for week {week}")
            return

        channel = bot.get_channel(channel_id)
        if not channel:
            logger.error(f"Channel {channel_id} not found.")
            return

        title = goal.get('title', f"Week {week}")
        embed = discord.Embed(
            title=title,
            description=goal.get('description', ""),
            color=discord.Color.green()
        )
        # Add dynamic fields
        for field in ['reading', 'labs', 'tips', 'resources']:
            if goal.get(field):
                embed.add_field(name=field.capitalize(), value="\n".join(goal[field]), inline=False)

        await channel.send(embed=embed)
        logger.info(f"Posted study plan for week {week} to channel {channel_id}")

        # Cycle week
        next_week = week + 1 if week < self.get_total_weeks() else 1
        self.save_current_week(next_week)


# Instantiate each study plan with config paths
_CCNA = _BaseStudyPlan(_Bot_Config._Current_Week_CCNA(), _Bot_Config._Study_Plan_CCNA())
_CCNP = _BaseStudyPlan(_Bot_Config._Current_Week_CCNP(), _Bot_Config._Study_Plan_CCNP())
_CCIE = _BaseStudyPlan(_Bot_Config._Current_Week_CCIE(), _Bot_Config._Study_Plan_CCIE())

# Expose static interfaces
class _CCNA_Study_Plan(_CCNA.__class__):
    post_weekly_goal = staticmethod(_CCNA.post_weekly_goal)
    get_current_week = staticmethod(_CCNA.get_current_week)
    save_current_week = staticmethod(_CCNA.save_current_week)
    get_weekly_goal = staticmethod(_CCNA.get_weekly_goal)

class _CCNP_Study_Plan(_CCNP.__class__):
    post_weekly_goal = staticmethod(_CCNP.post_weekly_goal)
    get_current_week = staticmethod(_CCNP.get_current_week)
    save_current_week = staticmethod(_CCNP.save_current_week)
    get_weekly_goal = staticmethod(_CCNP.get_weekly_goal)

class _CCIE_Study_Plan(_CCIE.__class__):
    post_weekly_goal = staticmethod(_CCIE.post_weekly_goal)
    get_current_week = staticmethod(_CCIE.get_current_week)
    save_current_week = staticmethod(_CCIE.save_current_week)
    get_weekly_goal = staticmethod(_CCIE.get_weekly_goal)
