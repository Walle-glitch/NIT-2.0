import discord
import json
import os
import _Bot_Config # type: ignore


'''
CCNA Study Plan: 
'''

# Paths to the current week and study plan JSON files
CURRENT_WEEK_CCNA = _Bot_Config._Current_Week_CCNA()
STUDY_PLAN_CCNA = _Bot_Config._Study_Plan_CCNA()


# Function to fetch the current week from a file
def get_current_week_CCNA():
    if os.path.exists(CURRENT_WEEK_CCNA):
        try:
            with open(CURRENT_WEEK_CCNA, "r") as f:
                data = json.load(f)
                return data.get("current_week", 1)
        except json.JSONDecodeError:
            print("JSON file is empty or invalid. Initializing to week 1.")
            return 1
    return 1

# Function to save the current week to a file
def save_current_week_CCNA(week_number):
    with open(CURRENT_WEEK_CCNA, "w") as f:
        json.dump({"current_week": week_number}, f)

# Function to fetch the study plan for the current week from a JSON file
def get_weekly_goal_CCNA(week_number):
    if os.path.exists(STUDY_PLAN_CCNA):
        try:
            with open(STUDY_PLAN_CCNA, "r") as f:
                study_plan = json.load(f)
                return study_plan.get(str(week_number), None)
        except json.JSONDecodeError:
            print("Study plan file is empty or invalid.")
            return None
    else:
        print(f"Study plan file {STUDY_PLAN_CCNA} not found.")
        return None

# Function to check if there was any previous post in the channel
async def check_previous_post(channel):
    async for message in channel.history(limit=1):
        if message.author == channel.guild.me:  # Check if the bot posted the last message
            return True
    return False

# Function to post the weekly goal in a specific channel
async def post_weekly_goal_CCNA(bot, CCNA_STUDY_CHANNEL_ID):
    # Fetch the current week
    current_week = get_current_week_CCNA()

    # Fetch study plan data
    study_plan = None
    if os.path.exists(STUDY_PLAN_CCNA):
        with open(STUDY_PLAN_CCNA, "r") as f:
            study_plan = json.load(f)

    if not study_plan:
        print("Study plan file is missing or invalid.")
        return

    # Check if current week exists in the study plan
    if str(current_week) not in study_plan:
        current_week = 1  # If current week exceeds the plan, reset to week 1

    # Fetch the current study goal
    goal = study_plan.get(str(current_week), None)

    if goal:
        channel = bot.get_channel(CCNA_STUDY_CHANNEL_ID)
        
        if not channel:
            print(f"Channel with ID {CCNA_STUDY_CHANNEL_ID} not found.")
            return

        # Check if there's a previous post by the bot, if not, start from week 1
        if not await check_previous_post(channel):
            current_week = 1
            goal = study_plan.get(str(current_week), None)

        embed = discord.Embed(
            title=f"Week {current_week}: {goal['title']}",
            description="This week's study plan",
            color=discord.Color.green()
        )
        embed.add_field(name="Reading", value="\n".join(goal['reading']), inline=False)
        embed.add_field(name="Labs", value="\n".join(goal['labs']), inline=False)

        await channel.send(embed=embed)

        # Increase the week and save it, or reset if it's the last week
        if str(current_week + 1) in study_plan:
            current_week += 1
        else:
            current_week = 1  # Reset to week 1 if no more weeks in plan
        
        save_current_week_CCNA(current_week)
    else:
        print("No study plan available for this week.")


'''
CCNP Study Plan: 
'''

# Paths to the current week and study plan JSON files
CURRENT_WEEK_CCNP = _Bot_Config._Current_Week_CCNP()
STUDY_PLAN_CCNP = _Bot_Config._Study_Plan_CCNP()

# Function to fetch the current week from a file
def get_current_week_CCNP():
    if os.path.exists(CURRENT_WEEK_CCNP):
        try:
            with open(CURRENT_WEEK_CCNP, "r") as f:
                data = json.load(f)
                return data.get("current_week", 1)
        except json.JSONDecodeError:
            print("JSON file is empty or invalid. Initializing to week 1.")
            return 1
    return 1

# Function to save the current week to a file
def save_current_week_CCNP(week_number):
    with open(CURRENT_WEEK_CCNP, "w") as f:
        json.dump({"current_week": week_number}, f)

# Function to fetch the study plan for the current week from a JSON file
def get_weekly_goal_CCNP(week_number):
    if os.path.exists(STUDY_PLAN_CCNP):
        try:
            with open(STUDY_PLAN_CCNP, "r") as f:
                study_plan = json.load(f)
                return study_plan.get(str(week_number), None)
        except json.JSONDecodeError:
            print("Study plan file is empty or invalid.")
            return None
    else:
        print(f"Study plan file {STUDY_PLAN_CCNP} not found.")
        return None

# Function to check if there was any previous post in the channel
async def check_previous_post(channel):
    async for message in channel.history(limit=1):
        if message.author == channel.guild.me:  # Check if the bot posted the last message
            return True
    return False

# Function to post the weekly goal in a specific channel
async def post_weekly_goal_CCNP(bot, CCNP_STUDY_CHANNEL_ID):
    # Fetch the current week
    current_week = get_current_week_CCNP()

    # Fetch study plan data
    study_plan = None
    if os.path.exists(STUDY_PLAN_CCNP):
        with open(STUDY_PLAN_CCNP, "r") as f:
            study_plan = json.load(f)

    if not study_plan:
        print("Study plan file is missing or invalid.")
        return

    # Check if current week exists in the study plan
    if str(current_week) not in study_plan:
        current_week = 1  # If current week exceeds the plan, reset to week 1

    # Fetch the current study goal
    goal = study_plan.get(str(current_week), None)

    if goal:
        channel = bot.get_channel(CCNP_STUDY_CHANNEL_ID)
        
        if not channel:
            print(f"Channel with ID {CCNP_STUDY_CHANNEL_ID} not found.")
            return

        # Check if there's a previous post by the bot, if not, start from week 1
        if not await check_previous_post(channel):
            current_week = 1
            goal = study_plan.get(str(current_week), None)

        embed = discord.Embed(
            title=f"Week {current_week}: {goal['title']}",
            description="This week's study plan",
            color=discord.Color.green()
        )
        embed.add_field(name="Reading", value="\n".join(goal['reading']), inline=False)
        embed.add_field(name="Labs", value="\n".join(goal['labs']), inline=False)

        await channel.send(embed=embed)

        # Increase the week and save it, or reset if it's the last week
        if str(current_week + 1) in study_plan:
            current_week += 1
        else:
            current_week = 1  # Reset to week 1 if no more weeks in plan
        
        save_current_week_CCNP(current_week)
    else:
        print("No study plan available for this week.")

'''
CCIE Study Plan: 
'''

# Path to the current week and study plan JSON files
CURRENT_WEEK_CCNP = _Bot_Config._Current_Week_CCIE()
STUDY_PLAN_CCNP = _Bot_Config._Study_Plan_CCIE()

# Function to fetch the current week from a file
def get_current_week_CCIE():
    if os.path.exists(CURRENT_WEEK_CCNP):
        try:
            with open(CURRENT_WEEK_CCNP, "r") as f:
                data = json.load(f)
                return data.get("current_week", 1)
        except json.JSONDecodeError:
            print("JSON file is empty or invalid. Initializing to week 1.")
            return 1
    return 1

# Function to save the current week to a file
def save_current_week_CCIE(week_number):
    with open(CURRENT_WEEK_CCNP, "w") as f:
        json.dump({"current_week": week_number}, f)

# Function to fetch the study plan for the current week from a JSON file
def get_weekly_goal_CCIE(week_number):
    if os.path.exists(STUDY_PLAN_CCNP):
        try:
            with open(STUDY_PLAN_CCNP, "r") as f:
                study_plan = json.load(f)
                return study_plan.get(str(week_number), None)
        except json.JSONDecodeError:
            print("Study plan file is empty or invalid.")
            return None
    else:
        print(f"Study plan file {STUDY_PLAN_CCNP} not found.")
        return None

# Function to check if there was any previous post in the channel
async def check_previous_post_CCIE(channel):
    async for message in channel.history(limit=1):
        if message.author == channel.guild.me:  # Check if the bot posted the last message
            return True
    return False

# Function to post the weekly goal in a specific channel
async def post_weekly_goal_CCIE(bot, CCIE_STUDY_CHANNEL_ID):
    # Fetch the current week
    current_week = get_current_week_CCIE()

    # Fetch study plan data
    study_plan = None
    if os.path.exists(STUDY_PLAN_CCNP):
        with open(STUDY_PLAN_CCNP, "r") as f:
            study_plan = json.load(f)

    if not study_plan:
        print("Study plan file is missing or invalid.")
        return

    # Check if current week exists in the study plan
    if str(current_week) not in study_plan:
        current_week = 1  # If current week exceeds the plan, reset to week 1

    # Fetch the current study goal
    goal = study_plan.get(str(current_week), None)

    if goal:
        channel = bot.get_channel(CCIE_STUDY_CHANNEL_ID)
        
        if not channel:
            print(f"Channel with ID {CCIE_STUDY_CHANNEL_ID} not found.")
            return

        # Check if there's a previous post by the bot, if not, start from week 1
        if not await check_previous_post_CCIE(channel):
            current_week = 1
            goal = study_plan.get(str(current_week), None)

        embed = discord.Embed(
            title=f"Week {current_week}: {goal['title']}",
            description="This week's study plan",
            color=discord.Color.green()
        )
        embed.add_field(name="Reading", value="\n".join(goal['reading']), inline=False)
        embed.add_field(name="Labs", value="\n".join(goal['labs']), inline=False)

        await channel.send(embed=embed)

        # Increase the week and save it, or reset if it's the last week
        if str(current_week + 1) in study_plan:
            current_week += 1
        else:
            current_week = 1  # Reset to week 1 if no more weeks in plan
        
        save_current_week_CCIE(current_week)
    else:
        print("No study plan available for this week.")

