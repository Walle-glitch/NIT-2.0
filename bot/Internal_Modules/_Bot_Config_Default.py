'''
Replace with respective Tokens and Keys 
Rename the file to _Bot_Config.py

mv _Bot_Config_Default.py _Bot_Config.py

'''

# Used in main.py





# Roles with access to "Sudo commands"
def _Bot_Admin_Role_Name():
    """Returns the name of the role that manages the bot."""
    return "Role for bot management"  # Replace with actual role name

def _Admin_Role_Name():
    """Returns the name of the admin role."""
    return "Admin role name"  # Replace with actual role name

def _Mod_Role_Name():
    """Returns the name of the moderator role."""
    return "Moderator role name"  # Replace with actual role name

def _Mentor_Role_Name():
    """Returns the name of the mentor role."""
    return "Mentor role name"  # Replace with actual role name

# Channel IDs
def _XP_Update_Channel_ID():
    """Returns the channel ID for XP updates."""
    return "XP update channel ID"  # Replace with actual channel ID

def _Job_Channel_ID():
    """Returns the channel ID for external job postings."""
    return "Job posting channel ID"  # Replace with actual channel ID

def _CCIE_Study_Channel_ID():
    """Returns the channel ID for CCIE study discussions."""
    return "CCIE study channel ID"  # Replace with actual channel ID

def _CCNP_Study_Channel_ID():
    """Returns the channel ID for CCNP study discussions."""
    return "CCNP study channel ID"  # Replace with actual channel ID

def _Welcome_Channel_ID():
    """Returns the channel ID for the welcome channel."""
    return "Welcome channel ID"  # Replace with actual channel ID

def _Log_Channel_ID():
    """Returns the channel ID for logging events."""
    return "Log channel ID"  # Replace with actual channel ID

def _Ticket_Category_ID():
    """Returns the category ID for support tickets."""
    return "Ticket category ID"  # Replace with actual category ID

def _Gen_Channel_ID():
    """Returns the general chat channel ID."""
    return "General chat channel ID"  # Replace with actual channel ID

def _YouTube_Channel_ID():
    """Returns the YouTube announcements channel ID."""
    return "YouTube channel ID"  # Replace with actual channel ID

def _Podcast_Channel_ID():
    """Returns the podcast announcements channel ID."""
    return "Podcast channel ID"  # Replace with actual channel ID

# Discord OAuth2 credentials
def _Client_ID():
    """Returns the Discord client ID for the bot."""
    return "Discord client ID"  # Replace with actual client ID

def _Client_Secret():
    """Returns the Discord client secret."""
    return "Discord client secret"  # Replace with actual client secret

def _Redirect_URI():
    """Returns the URI used for OAuth2 redirects."""
    return "Redirect URI"  # Replace with actual redirect URI

def _Discord_API_Base_URL():
    """Returns the base URL for Discord API."""
    return "https://discord.com/api"

# Media and Study Plan Files
def _Media_File():
    """Returns the path to the media channels JSON file."""
    return "./Json_Files/media_channels.json"

def _Current_Week_CCNP():
    """Returns the path to the current week CCNP JSON file."""
    return "./Json_Files/current_week_CCNP.json"

def _Study_Plan_CCNP():
    """Returns the path to the CCNP study plan JSON file."""
    return "./Json_Files/CCNP_Study_Plan.json"

def _Current_Week_CCIE():
    """Returns the path to the current week CCIE JSON file."""
    return "./Json_Files/current_week_CCIE.json"

def _Study_Plan_CCIE():
    """Returns the path to the CCIE study plan JSON file."""
    return "./Json_Files/CCIE_Study_Plan.json"

# Global Refs for the Bot Module
def _Role_Json_File():
    """Returns the path to the roles JSON file."""
    return "./Json_Files/roles.json"

def _Welcome_Message_File():
    """Returns the path to the welcome message ID JSON file."""
    return "./Json_Files/welcome_message_id.json"

def _XP_File():
    """Returns the path to the XP data JSON file."""
    return "./Json_Files/xp_data.json"

def _Excluded_Roles():
    """Returns a list of role names that are excluded from certain operations."""
    return ["Admin", "Moderator", "Administrator"]  # Replace with actual roles to exclude

def _Static_Roles():
    """Returns a dictionary of static role names and their corresponding IDs."""
    return {
        "NIT_24": "Role ID for NIT 24",
        "NIT_23": "Role ID for NIT 23",
        "NIT_22": "Role ID for NIT 22",
        "Another Start Year": "Role ID for another year",
        "3rd Year!": "Role ID for 3rd year",
        "Union Member": "Role ID for union member",
        "Arkiv-enjoyer": "Role ID for Arkiv enjoyer",
    }  # Replace with actual role IDs

def _Log_To_Channel_ID():
    """Returns the channel ID for logging events."""
    return "Log to channel ID"  # Replace with actual log channel ID

def _Admin_Channel_ID():
    """Returns the channel ID for admin-related events."""
    return "Admin channel ID"  # Replace with actual admin channel ID

# Auction Module
def _Auctions_File():
    """Returns the path to the auctions JSON file."""
    return "Json_Files/auctions.json"

# GitHub API settings
def _GitHub_API_URL():
    """Returns the base GitHub API URL for issues."""
    return "GitHub API URL for issues"  # Replace with actual API URL

def _GitHub_Token():
    """Returns the GitHub access token."""
    return "GitHub access token"  # Replace with actual token


