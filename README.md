Overview
NIT-BOT is a versatile Discord bot designed for various network-related functionalities, including BGP configuration, subnet games, and more. This bot integrates with Discord to provide a range of commands for network management and educational purposes.

Features
BGP Configuration: Configure BGP neighbors on a router.
Subnet Game: Engage in a subnetting quiz to test your networking knowledge.
RFC Retrieval: Fetch and display information about RFCs.
Role Management: Assign and remove roles using reactions.
Bot Management: Admin commands for bot maintenance and updates.

The bot requires specific configuration files and environment variables. You need to create and configure the following:

botConfig.py: Contains sensitive bot token and configuration details. Create this file with the following structure:

python
_Bot_Token = 'YOUR_BOT_TOKEN_HERE'
_Router_Conf.py: Contains router configuration details. Create this file with the following structure:

python
ROUTER_IP = 'ROUTER_IP_ADDRESS'
SSH_USERNAME = 'YOUR_SSH_USERNAME'
SSH_PASSWORD = 'YOUR_SSH_PASSWORD'
Additional Server Configuration: Ensure the server where the bot runs has the following:

Python 3.7+ installed.
Required Python packages as listed in requirements.txt.
Network accessibility to the router for BGP configuration if applicable.
Running the Bot
Start the Bot

Run the bot using:
python3 main.py

Interact with the Bot

Once the bot is running, you can interact with it using the command prefix ./. For a list of available commands, use ./h.

Commands
Help: ./h

Version: ./version

Git Repository: ./git

Hello: ./hello

About: ./about

Ping: ./ping [IP_ADDRESS]

RFC: ./rfc [NUMBER]

Subnet Game: ./subnet

BGP Setup: ./BGP-Setup [IP_ADDRESS] [AS_NUMBER]

Admin Commands:

Reboot: ./Reboot (requires Bot-Master role)
