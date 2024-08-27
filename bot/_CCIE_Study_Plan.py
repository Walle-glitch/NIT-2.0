import datetime
import discord
import json
import os

# Path to the current week and study plan JSON files
_Current_Week_CCIE = "Json_Files/current_week_CCIE.json"
_Study_Plan_CCIE = "Json_Files/CCIE_Study_Plan.json"

# Function to fetch the current week from a file
def get_current_week_CCIE():
    if os.path.exists(_Current_Week_CCIE):
        try:
            with open(_Current_Week_CCIE, "r") as f:
                data = json.load(f)
                return data.get("current_week", 1)
        except json.JSONDecodeError:
            # Handle the case where the JSON file is empty or corrupted
            print("JSON file is empty or invalid. Initializing to week 1.")
            return 1
    return 1

# Function to save the current week to a file
def save_current_week_CCIE(week_number):
    with open(_Current_Week_CCIE, "w") as f:
        json.dump({"current_week": week_number}, f)

# Function to fetch the study plan for the current week from a JSON file
def get_weekly_goal_CCIE(week_number):
    if os.path.exists(_Study_Plan_CCIE):
        try:
            with open(_Study_Plan_CCIE, "r") as f:
                study_plan = json.load(f)
                return study_plan.get(str(week_number), None)
        except json.JSONDecodeError:
            print("Study plan file is empty or invalid.")
            return None
    else:
        print(f"Study plan file {_Study_Plan_CCIE} not found.")
        return None

# Function to post the weekly goal in a specific channel
async def post_weekly_goal_CCIE(bot, CCIE_STUDY_CHANNEL_ID):
    # Fetch the current week
    current_week = get_current_week_CCIE()

    goal = get_weekly_goal_CCIE(current_week)

    if goal:
        channel = bot.get_channel(CCIE_STUDY_CHANNEL_ID)
        
        if not channel:
            print(f"Channel with ID {CCIE_STUDY_CHANNEL_ID} not found.")
            return

        embed = discord.Embed(
            title=f"Week {current_week}: {goal['title']}",
            description="This week's study plan",
            color=discord.Color.green()
        )
        embed.add_field(name="Reading", value="\n".join(goal['reading']), inline=False)
        embed.add_field(name="Labs", value="\n".join(goal['labs']), inline=False)
        
        await channel.send(embed=embed)

        # Increase the week and save
        current_week += 1
        save_current_week_CCIE(current_week)
    else:
        print("No study plan available for this week.")
