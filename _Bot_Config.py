# _Bot_Config.py
# Replace with respective Tokens and Keys and rename from _Bot_Config_Default.py

import os

# ------------------
# Bot Credentials
# ------------------

def _Bot_Token():
    """Returns the Discord bot token from environment."""
    return os.getenv("DISCORD_TOKEN")

def _Open_AI_Token():
    """Returns the OpenAI API key from environment."""
    return os.getenv("OPENAI_API_KEY")

# ------------------
# Role Names
# ------------------

def _Bot_Admin_Role_Name():
    """Role allowed to run bot admin commands."""
    return "Code_Knight"  # Replace with actual role name

def _Admin_Role_Name():
    """Domain administrator role name."""
    return "Privilege 15"  # Replace with actual role name

def _Mod_Role_Name():
    """Moderator role name."""
    return "Privilege 10"  # Replace with actual role name

def _Mentor_Role_Name():
    """Mentor role name."""
    return "Mentor"  # Replace with actual role name

# ------------------
# Channel IDs
# ------------------

def _Guild_ID():
    """Returns Discord-guild (server) ID where late-night–rollen ska hanteras."""
    return 1012026430470766813  # Ersätt med ditt faktiska guild-ID (heltal)

def _Archive_Category_ID():
    return 1012026430932127925  # Replace with actual category ID

def _XP_Update_Channel_ID():
    return 1012067343452622949  # Replace with actual channel ID

def _Job_Channel_ID():
    return 1290666654044258326  # Replace with actual channel ID

def _CCIE_Study_Channel_ID():
    return 1277674142686248971  # Replace with actual channel ID

def _CCNP_Study_Channel_ID():
    return 1277675077428842496  # Replace with actual channel ID

def _CCNA_Study_Channel_ID():
    return 1289257448263254037  # Replace with actual channel ID

def _Welcome_Channel_ID():
    return 1293300247824568422  # Replace with actual channel ID

def _Log_Channel_ID():
    return 1277567653765976074  # Replace with actual channel ID

def _Ticket_Category_ID():
    return 1012026430932127925  # Replace with actual category ID

def _Gen_Channel_ID():
    return 1012026430932127926  # Replace with actual channel ID

def _YouTube_Channel_ID():
    return 1293252143217639424  # Replace with actual channel ID

def _Podcast_Channel_ID():
    return 1293252143217639424  # Replace with actual channel ID

# ------------------
# OAuth2 / API Settings
# ------------------

def _Client_ID():
    return "1017514463697584169"  # Replace with actual client ID

def _Client_Secret():
    return os.getenv("DISCORD_CLIENT_SECRET") or ""  # Better to set via env

def _Redirect_URI():
    return os.getenv("REDIRECT_URI") or "http://localhost:5000/callback"

def _Discord_API_Base_URL():
    return "https://discord.com/api"

# ------------------
# File Paths
# ------------------

def _Media_File():
    return "./Json_Files/media_channels.json"

def _Current_Week_CCNP():
    return "./Json_Files/current_week_CCNP.json"

# Lägg under övriga Study Plan–funktioner i _Bot_Config.py

def _Current_Week_CCNA():
    """Path to CCNA current-week JSON."""
    return "./Json_Files/current_week_CCNA.json"

def _Study_Plan_CCNA():
    """Path to CCNA study-plan JSON."""
    return "./Json_Files/CCNA_Study_Plan.json"

def _Study_Plan_CCNP():
    return "./Json_Files/CCNP_Study_Plan.json"

def _Current_Week_CCIE():
    return "./Json_Files/current_week_CCIE.json"

def _Study_Plan_CCIE():
    return "./Json_Files/CCIE_Study_Plan.json"

def _Role_Json_File():
    return "./Json_Files/roles.json"

def _Welcome_Message_File():
    return "./Json_Files/welcome_message_id.json"

def _XP_File():
    return "./Json_Files/xp_data.json"

def _Question_File():
    """Returns the path to the network questions JSON file."""
    return "./Json_Files/network_questions.json"

def _Ticket_Counter_File():
    return "./Json_Files/Ticket_counter_file.json"


# ------------------
# Roles Configuration
# ------------------

def _Excluded_Roles():
    return ["Admin", "Moderator", "Administrator"]  # Replace with actual excludes

def _Static_Roles():
    return {
        "NIT_25": 1386591861292138556,
        "NIT_24": 1254895590567837776,
        "NIT_23": 1115331511848271942,
        "NIT_22": 1012047713610760383,
        "Union Member": 1079112794189865111,
        "Arkiv-enjoyer": 1160861563083837511,
    }

def _protected_Poles():
    """Static protected role IDs."""
    return {
        "NIT_25": 1386591861292138556,
        "NIT_24": 1254895590567837776,
        "NIT_23": 1115331511848271942,
        "NIT_22": 1012047713610760383,
    }

def _Late_Night_Role_ID():
    return 1290474446859276298

# ------------------
# Admin Channel
# ------------------

def _Admin_Channel_ID():
    return 1012447677880995920  # Replace with actual channel ID

# ------------------
# Auction Settings
# ------------------

def _Auctions_File():
    return "./Json_Files/auctions.json"

# ------------------
# GitHub API
# ------------------

def _GitHub_API_URL():
    return "https://api.github.com"

def _GitHub_Token():
    return os.getenv("GITHUB_TOKEN") or ""
