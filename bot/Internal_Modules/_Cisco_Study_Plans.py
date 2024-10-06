import discord
import json
import os
import _Bot_Config  # type: ignore


class _CCNA_Study_Plan:
    @staticmethod
    def get_current_week():
        current_week_file = _Bot_Config._Current_Week_CCNA()
        if os.path.exists(current_week_file):
            try:
                with open(current_week_file, "r") as f:
                    data = json.load(f)
                    return data.get("current_week", 1)
            except json.JSONDecodeError:
                print("JSON file is empty or invalid. Initializing to week 1.")
                return 1
        return 1

    @staticmethod
    def save_current_week(week_number):
        with open(_Bot_Config._Current_Week_CCNA(), "w") as f:
            json.dump({"current_week": week_number}, f)

    @staticmethod
    def get_weekly_goal(week_number):
        if os.path.exists(_Bot_Config._Study_Plan_CCNA()):
            try:
                with open(_Bot_Config._Study_Plan_CCNA(), "r") as f:
                    study_plan = json.load(f)
                    return study_plan.get(str(week_number), None)
            except json.JSONDecodeError:
                print("Study plan file is empty or invalid.")
                return None
        else:
            print(f"Study plan file not found.")
            return None

    @staticmethod
    async def post_weekly_goal(bot, channel_id):
        current_week = _CCNA_Study_Plan.get_current_week()
        goal = _CCNA_Study_Plan.get_weekly_goal(current_week)

        if goal:
            channel = bot.get_channel(channel_id)
            if not channel:
                print(f"Channel with ID {channel_id} not found.")
                return

            embed = discord.Embed(
                title=f"Week {current_week}: {goal['title']}",
                description="This week's study plan",
                color=discord.Color.green()
            )
            embed.add_field(name="Reading", value="\n".join(goal['reading']), inline=False)
            embed.add_field(name="Labs", value="\n".join(goal['labs']), inline=False)

            await channel.send(embed=embed)

            # Increase the week and save it, or reset if it's the last week
            if str(current_week + 1) in goal:
                current_week += 1
            else:
                current_week = 1
            
            _CCNA_Study_Plan.save_current_week(current_week)
        else:
            print("No study plan available for this week.")


class _CCNP_Study_Plan:
    @staticmethod
    def get_current_week():
        current_week_file = _Bot_Config._Current_Week_CCNP()
        if os.path.exists(current_week_file):
            try:
                with open(current_week_file, "r") as f:
                    data = json.load(f)
                    return data.get("current_week", 1)
            except json.JSONDecodeError:
                print("JSON file is empty or invalid. Initializing to week 1.")
                return 1
        return 1

    @staticmethod
    def save_current_week(week_number):
        with open(_Bot_Config._Current_Week_CCNP(), "w") as f:
            json.dump({"current_week": week_number}, f)

    @staticmethod
    def get_weekly_goal(week_number):
        if os.path.exists(_Bot_Config._Study_Plan_CCNP()):
            try:
                with open(_Bot_Config._Study_Plan_CCNP(), "r") as f:
                    study_plan = json.load(f)
                    return study_plan.get(str(week_number), None)
            except json.JSONDecodeError:
                print("Study plan file is empty or invalid.")
                return None
        else:
            print(f"Study plan file not found.")
            return None

    @staticmethod
    async def post_weekly_goal(bot, channel_id):
        current_week = _CCNP_Study_Plan.get_current_week()
        goal = _CCNP_Study_Plan.get_weekly_goal(current_week)

        if goal:
            channel = bot.get_channel(channel_id)
            if not channel:
                print(f"Channel with ID {channel_id} not found.")
                return

            embed = discord.Embed(
                title=f"Week {current_week}: {goal['title']}",
                description="This week's study plan",
                color=discord.Color.green()
            )
            embed.add_field(name="Reading", value="\n".join(goal['reading']), inline=False)
            embed.add_field(name="Labs", value="\n".join(goal['labs']), inline=False)

            await channel.send(embed=embed)

            # Increase the week and save it, or reset if it's the last week
            if str(current_week + 1) in goal:
                current_week += 1
            else:
                current_week = 1
            
            _CCNP_Study_Plan.save_current_week(current_week)
        else:
            print("No study plan available for this week.")


class _CCIE_Study_Plan:
    @staticmethod
    def get_current_week():
        current_week_file = _Bot_Config._Current_Week_CCIE()
        if os.path.exists(current_week_file):
            try:
                with open(current_week_file, "r") as f:
                    data = json.load(f)
                    return data.get("current_week", 1)
            except json.JSONDecodeError:
                print("JSON file is empty or invalid. Initializing to week 1.")
                return 1
        return 1

    @staticmethod
    def save_current_week(week_number):
        with open(_Bot_Config._Current_Week_CCIE(), "w") as f:
            json.dump({"current_week": week_number}, f)

    @staticmethod
    def get_weekly_goal(week_number):
        if os.path.exists(_Bot_Config._Study_Plan_CCIE()):
            try:
                with open(_Bot_Config._Study_Plan_CCIE(), "r") as f:
                    study_plan = json.load(f)
                    return study_plan.get(str(week_number), None)
            except json.JSONDecodeError:
                print("Study plan file is empty or invalid.")
                return None
        else:
            print(f"Study plan file not found.")
            return None

    @staticmethod
    async def post_weekly_goal(bot, channel_id):
        current_week = _CCIE_Study_Plan.get_current_week()
        goal = _CCIE_Study_Plan.get_weekly_goal(current_week)

        if goal:
            channel = bot.get_channel(channel_id)
            if not channel:
                print(f"Channel with ID {channel_id} not found.")
                return

            embed = discord.Embed(
                title=f"Week {current_week}: {goal['title']}",
                description="This week's study plan",
                color=discord.Color.green()
            )
            embed.add_field(name="Reading", value="\n".join(goal['reading']), inline=False)
            embed.add_field(name="Labs", value="\n".join(goal['labs']), inline=False)

            await channel.send(embed=embed)

            # Increase the week and save it, or reset if it's the last week
            if str(current_week + 1) in goal:
                current_week += 1
            else:
                current_week = 1
            
            _CCIE_Study_Plan.save_current_week(current_week)
        else:
            print("No study plan available for this week.")
