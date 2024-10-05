# NIT-BOT

## Overview
NIT-BOT is a versatile Discord bot designed for various network-related functionalities, including BGP configuration, subnet games, AI integration, study plans for CCIE and CCNP, and more. The bot integrates with Discord to provide a range of commands that facilitate network management, educational purposes, and fun activities.

## Features

### Networking & System Utilities
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

## Setup Guide

### 1. Clone the Repository
bash
```
Copy code
git clone https://github.com/yourusername/NIT-2.0.git
cd NIT-2.0/bot
```

2. Install the Required Dependencies
Ensure you have Python 3 installed. Install the necessary packages using the requirements.txt file:

bash
```
pip3 install -r requirements.txt
```

### Alternatively, you can install the dependencies manually:

bash:
```
sudo pip3 install discord.py
sudo pip3 install pypresence
sudo pip3 install beautifulsoup4
sudo pip3 install paramiko
sudo pip3 install openai
sudo pip3 install flask
```

### 3. Configure the Bot
Copy the _Bot_Config.py.example file to _Bot_Config.py:
bash
```
cp _Bot_Config.py.example _Bot_Config.py
```
Open _Bot_Config.py and add your bot's token, client ID, and client secret:
python
```
def _Bot_Token():
    return 'your_discord_bot_token'

def _Client_ID():
    return 'your_discord_client_id'

def _Client_Secret():
    return 'your_discord_client_secret'
```
### 4. Run the Bot
You can now run the bot along with the Flask server for a GUI and landing page:

bash
```
python3 app.py
```
To run the bot only:

bash
```
python3 main.py
```

The Flask server will be available on http://localhost:5000, and the bot will also be running on your Discord server.

### 5. Set the Bot to Run on Startup
For running the bot and Flask server continuously, you can set up a systemd service.

Create a new service file:

bash
```
sudo nano /etc/systemd/system/discord-bot.service
```
Add the following content:

ini
```
[Unit]
Description=Discord Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/youruser/NIT-2.0/bot/app.py
WorkingDirectory=/home/youruser/NIT-2.0/bot/
Restart=always
User=youruser

[Install]
WantedBy=multi-user.target
```

Reload systemd and enable the service:
bash
```
sudo systemctl daemon-reload
sudo systemctl enable discord-bot
sudo systemctl start discord-bot
```

