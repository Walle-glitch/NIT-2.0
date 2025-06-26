# NIT-BOT

## Overview

NIT-BOT is a versatile Discord bot containerized via Docker Compose, designed for network-related utilities, educational study planning, community engagement, and moderation. It integrates with Discord, OpenAI, and external APIs to provide a rich set of commands and background tasks.

## Features

### Networking & System Utilities
- **Subnet Quiz Game**: Interactive subnetting quiz with network, broadcast, and host-count questions.  
- **Ping Command**: Test connectivity by pinging a specified IP (`!ping <ip>`).  
- **RFC Lookup**: Retrieve RFC title and link via `/rfc <number>`.

### AI Integration
- **ChatGPT Sessions**: `/AI` initiates up to five-turn conversations with OpenAI's GPT model.

### Study Plans
- **CCNA / CCNP / CCIE**: Weekly Cisco study goals posted automatically on Sundays in configured channels; cycles through JSON-defined plans.

### Role Management
- **Dynamic Role Buttons**: `/addrole` shows interactive buttons; users click to self-assign static roles.  
- **Password-Protected Roles**: Certain roles require a DM-reply password.  
- **Remove Roles**: `/removerole` lists and removes roles via commands.

### Job Listings
- **Daily Job Fetching**: Retrieves network-engineering job posts from Indeed and publishes embeds daily.

### XP & Leveling
- **Activity-Based XP**: Users gain XP for messages and reactions; levels increase at thresholds (1k, 10k, 20k).  
- **Late-Night Role**: Assign/remove a `LateNightCrew` role based on activity between 20:00–05:00 and 24h inactivity.

### Media Posting
- **YouTube & Podcast Poster**: Configurable channels list; periodic embeds of latest entries.

### Ticket System & GitHub Integration
- **Slash-Based Tickets**: `/ticket` creates numbered support channels, auto-archives inactive tickets.  
- **GitHub Issues**: `/issue <title> <body>` opens issues via GitHub API.

### Moderation & Administration
- **Kick / Ban / Mute**: Commands for privileged roles with logging and reporting.  
- **Module Reload**: `!reload_module <name>` reloads internal Python modules at runtime.

## Architecture & Modules

All custom logic resides in `Internal_Modules/`:

- `_Bot_Config.py` — Environment/config helper functions.  
- `_logging_setup.py` — Centralized logging to `logs/`.  
- `_Role_Management.py` — Role buttons & command handlers.  
- `_XP_Handler.py` — XP system & late-night role management.  
- `_Member_Moderation.py` — Kick/ban/mute with reports.  
- `_Game.py` — Subnet/network quiz game engine.  
- `_Bot_Modul.py` — Resource embeds & job posting.  
- `_Auction.py` — Auction creation with bid/buy buttons.  
- `_Cisco_Study_Plans.py` — Unified CCNA/CCNP/CCIE plan posting.  
- `_Media_Handler.py` — Periodic media (YouTube/Podcast) posters.  
- `_Ticket_System.py` — Ticket channel creation/archiving & GitHub issues.  
- `_Slash_Commands.py` — (Optional) shared slash command scaffolding.  
- `_Activity_Tracking.py` — Legacy activity tracking (superseded by XP handler).

## Configuration

### Environment Variables

Store secrets in a `.env` file and load via Docker Compose.

```dotenv
DISCORD_TOKEN=your_discord_bot_token
OPENAI_API_KEY=your_openai_key
GITHUB_TOKEN=your_github_token
REDIRECT_URI=http://localhost:5000/callback