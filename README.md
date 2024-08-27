# NIT-BOT

## Overview
NIT-BOT is a versatile Discord bot designed for various network-related functionalities, including BGP configuration, subnet games, AI integration, study plans for CCIE and CCNP, and more. The bot integrates with Discord to provide a range of commands that facilitate network management, educational purposes, and fun activities.

## Features

### Networking & System Utilities
- **BGP Configuration:** Configure BGP neighbors on a router with ease.
- **Subnet Game:** Engage in a subnetting quiz to test and improve your networking knowledge.
- **Ping Command:** Perform a network ping test to check connectivity.
- **RFC Retrieval:** Fetch and display information about RFCs by specifying their number.

### AI Integration
- **OpenAI Integration:** Ask questions to ChatGPT, and the bot will respond in a conversation-like session for up to five questions.

### Study Plans
- **CCIE & CCNP Study Plans:** The bot posts weekly study goals to specific channels based on the latest Cisco blueprint. These study plans help prepare for the CCIE and CCNP exams with lab suggestions and reading materials.

### Role Management
- **Dynamic Role Assignment:** Users can assign and remove roles using reactions or buttons, including dynamically generated role lists from the server.
- **Welcome Message:** The bot ensures a persistent and interactive welcome message with role assignment options using buttons.

### Job Listings
- **Job Fetching:** The bot fetches job listings relevant to network engineers and posts them in a specified channel daily.

### XP & Leveling System
- **XP System:** Users earn XP for activity and reactions. The bot tracks user levels and announces level-ups in a specific channel.

### Bot Management
- **Admin Commands:** Admin-level commands allow bot maintenance, including rebooting and moderation functions (kick, ban, mute users).

## Configuration

To get the bot running, you need to configure certain files and environment variables. The required configuration files include:

### `botConfig.py`
This file contains sensitive bot token and configuration details. Create this file with the following structure:

```python
_Bot_Token = 'YOUR_BOT_TOKEN_HERE'
_Open_AI_Token = 'YOUR_OPENAI_API_KEY'
_YOUR_INDEED_API_KEY = 'YOUR_INDEED_API_KEY'
