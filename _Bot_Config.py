# Internal_Modules/_Bot_Config.py
"""
Central configuration module for the bot.
It's recommended to load sensitive data like tokens from environment variables.
"""
import os
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()

# --- Essential Bot Credentials ---

def _Bot_Token() -> str:
    """Returns the bot's Discord token from the environment."""
    return os.getenv("DISCORD_TOKEN")

def _Gemini_API_Key() -> str:
    """Returns the Gemini API key from the environment."""
    return os.getenv("GOOGLE_API_KEY")

def _GitHub_Token() -> str:
    """Returns the GitHub token from the environment."""
    return os.getenv("GITHUB_TOKEN")

# --- Generic Bot Info ---

def _Guild_ID() -> int:
    """Returns the main Discord server/guild ID."""
    return 1012026430470766813  # Your Server ID

def _Client_ID() -> str:
    """Returns the bot's application client ID."""
    return "1017514463697584169"  # Your Client ID

VERSION_NR = "v2.6.0" # Version bump for config fix

# --- Role Names & IDs ---

def _Bot_Admin_Role_Name() -> str:
    """Role allowed to run bot admin commands."""
    return "Code_Knight"

def _Admin_Role_Name() -> str:
    """Domain administrator role name."""
    return "Privilege 15"

def _Mod_Role_Name() -> str:
    """Moderator role name."""
    return "Privilege 10"

def _Mentor_Role_Name() -> str:
    """Mentor role name."""
    return "Mentor"

def _Late_Night_Role_ID() -> int:
    """ID for the late-night activity role."""
    return 1290474446859276298

def _Excluded_Roles() -> list[str]:
    """Roles to be excluded from certain actions."""
    return ["Admin", "Moderator", "Administrator", "Code_Knight"]

# --- Channel IDs ---

def _XP_Update_Channel_ID() -> int:
    return 1012067343452622949

def _Job_Channel_ID() -> int:
    return 1290666654044258326

def _CCIE_Study_Channel_ID() -> int:
    return 1277674142686248971

def _CCNP_Study_Channel_ID() -> int:
    return 1277675077428842496

def _CCNA_Study_Channel_ID() -> int:
    return 1289257448263254037

def _Welcome_Channel_ID() -> int:
    return 1293300247824568422

def _Log_Channel_ID() -> int:
    return 1277567653765976074

def _Admin_Channel_ID() -> int:
    return 1012447677880995920

def _Ticket_Category_ID() -> int:
    return 1012026430932127925

# --- Absolute File Paths for Docker ---
# Using absolute paths inside the container is crucial for reliability.

def _XP_File() -> str:
    """Returns the absolute path to the XP data file."""
    return "/app/Json_Files/xp_data.json"

def _Role_Json_File() -> str:
    """Returns the absolute path to the roles data file."""
    return "/app/Json_Files/roles.json"

def _Auctions_File() -> str:
    """Returns the absolute path to the auctions data file."""
    return "/app/Json_Files/auctions.json"

def _Media_File() -> str:
    """Returns the absolute path to the media channels file."""
    return "/app/Json_Files/media_channels.json"

def _Current_Week_CCNA() -> str:
    """Returns the absolute path to the CCNA current week file."""
    return "/app/Json_Files/current_week_CCNA.json"

def _Study_Plan_CCNA() -> str:
    """Returns the absolute path to the CCNA study plan file."""
    return "/app/Json_Files/CCNA_Study_Plan.json"

def _Current_Week_CCNP() -> str:
    """Returns the absolute path to the CCNP current week file."""
    return "/app/Json_Files/current_week_CCNP.json"

def _Study_Plan_CCNP() -> str:
    """Returns the absolute path to the CCNP study plan file."""
    return "/app/Json_Files/CCNP_Study_Plan.json"

def _Current_Week_CCIE() -> str:
    """Returns the absolute path to the CCIE current week file."""
    return "/app/Json_Files/current_week_CCIE.json"

def _Study_Plan_CCIE() -> str:
    """Returns the absolute path to the CCIE study plan file."""
    return "/app/Json_Files/CCIE_Study_Plan.json"

def _Ticket_Counter_File() -> str:
    """Returns the absolute path to the ticket counter file."""
    return "/app/Json_Files/Ticket_counter_file.json"

def _Welcome_Message_File() -> str:
    """Returns the absolute path to the welcome message ID file."""
    return "/app/Json_Files/welcome_message_id.json"

def _Question_File() -> str:
    """Returns the absolute path to the network questions file."""
    return "/app/Json_Files/network_questions.json"

# --- Versioning ---
VERSION_NR = "v2.6.0"