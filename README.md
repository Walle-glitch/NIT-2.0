# NIT-2.0
NIT-BOT is a versatile and fun Discord bot designed for managing and automating various tasks on your server. Built with Python and the Discord API, NIT-BOT provides a range of commands, including network utilities, role management, and more. It’s designed to be easily customizable and extendable for your needs.

Features
Network Utilities:

Ping Test: Check the network connectivity to any IP address.
RFC Lookup: Retrieve information about RFCs from IETF.
BGP Configuration: Configure BGP peering on a router.
Role Management:

Add/Remove Roles: Assign or remove roles from users based on commands or reactions.
Subnet Game:

Subnet Quiz: Test your knowledge of subnetting with random questions.
Administrative Commands:

Reboot: Update the bot and restart it with the latest changes.
Role Setup: Create an embedded message for role assignment through reactions.
Prerequisites
Python 3.10 or higher
Required Python packages: discord.py, requests, beautifulsoup4
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/Walle-glitch/NIT-2.0.git
Navigate to the project directory:

bash
Copy code
cd NIT-2.0
Install the required packages:

bash
Copy code
pip install -r requirements.txt
Configure the bot:

Edit botConfig.py to include your Discord bot token and any other necessary configurations.
Run the bot:

bash
Copy code
python3 main.py
Configuration
botConfig.py: Contains the bot token and other configuration details.
_Router_Conf.py: Holds the router credentials and IP configuration.
_Bot_Modul.py: Custom module with bot functions (e.g., BGP configuration).
_Subnet_Game.py: Contains logic for the subnet quiz game.
Commands
General Commands:

./h: List all available commands.
./version: Show the current bot version.
./git: Get the GitHub repository link.
./hello: Send a hello message.
./about: Get information about the bot.
Network Utilities:

./ping [IP]: Perform a ping test to the specified IP address.
./rfc [number]: Retrieve information about the specified RFC number.
BGP Configuration:

./BGP: Get information on how to use the BGP setup command.
./BGP_Setup [IP] [AS]: Configure BGP peering with the given IP and AS number.
Role Management:

./addrole: Assign a predefined role to the user.
./removerole: Remove a predefined role from the user.
./setup_roles: Create an embedded message for role assignment via reactions.
Subnet Game:

./subnet: Start a subnet quiz game.
Administrative Commands:

./Reboot: Update the bot with the latest code and restart it.
Contributing
Contributions are welcome! If you have any ideas, bug reports, or improvements, please open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For any questions or further information, you can contact Walle.
