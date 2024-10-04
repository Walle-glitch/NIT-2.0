import os  # For interacting with the operating system, like file paths
import requests  # For making HTTP requests
import threading  # To run multiple tasks concurrently (Flask and Discord bot together)
from flask import Flask, render_template, jsonify, request  # Flask web framework for building the GUI
from markupsafe import Markup  # Safely handles string injection for HTML content
import sys  # System-specific parameters and functions

sys.path.append(os.path.join(os.path.dirname(__file__), 'Internal_Modules'))

import _Bot_Config # type: ignore
from main import bot # Imports the bot instance from the main.py file to run it

app = Flask(__name__)

# Discord OAuth2 credentials (replace with your own)
CLIENT_ID = _Bot_Config._Client_ID()
CLIENT_SECRET = _Bot_Config._Client_Secret()
REDIRECT_URI = _Bot_Config._Redirect_URI()  # Or you can keep it as is if it's a static URI
DISCORD_API_BASE_URL = _Bot_Config._Discord_API_Base_URL()

# Discord OAuth2 URL for authorization
OAUTH2_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20emailguilds"

# Function to load README.md content from the root directory
def get_readme_content():
    with open(os.path.join(os.getcwd(), '/home/bot/NIT-2.0/README.md'), 'r', encoding='utf-8') as readme_file:
        return Markup(readme_file.read().replace("\n", "<br>"))

# Simulate user data for the 'users' view
users_data = [
    {"id": 1, "name": "John Doe", "role": "Admin"},
    {"id": 2, "name": "Jane Smith", "role": "Moderator"},
    {"id": 3, "name": "Alice Johnson", "role": "Member"}
]

# Route to display the bot's status and README.md content
@app.route('/')
def home():
    readme_content = get_readme_content()
    return render_template('home.html', readme_content=readme_content)

# API route to check bot status
@app.route('/api/status')
def bot_status():
    return jsonify({"status": "running"})

# Route for displaying user list
@app.route('/users')
def users():
    return render_template('users.html', users=users_data)

# OAuth2 login route
@app.route('/login')
def login():
    return f'<a href="{OAUTH2_URL}">Login with Discord</a>'

# OAuth2 callback route
@app.route('/callback')
def callback():
    code = request.args.get('code')

    # Exchange authorization code for access token
    token_url = f"{DISCORD_API_BASE_URL}/oauth2/token"
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify email guilds'
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    token_response = requests.post(token_url, data=data, headers=headers)
    token_json = token_response.json()

    access_token = token_json.get('access_token')

    if access_token:
        # Use access token to fetch user info
        user_info_url = f"{DISCORD_API_BASE_URL}/users/@me"
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info_json = user_info_response.json()

        # Return user info as JSON
        return jsonify(user_info_json)
    else:
        return "Error getting access token", 400

# Start the Flask server in a separate thread
def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    # Start the Discord bot in the main thread to avoid asyncio issues
    bot_token = _Bot_Config._Bot_Token()
    bot.run(bot_token)
