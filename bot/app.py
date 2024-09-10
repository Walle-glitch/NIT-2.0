from flask import Flask, render_template, jsonify, request
import threading
import _Bot_Config
import requests
from main import bot  # Import bot instance from main.py

app = Flask(__name__)

# Discord OAuth2 credentials (replace with your own)
CLIENT_ID = _Bot_Config._Client_ID()
CLIENT_SECRET = _Bot_Config._Client_Secret()
REDIRECT_URI = 'http://172.20.0.10/callback'  # Replace with your server IP
DISCORD_API_BASE_URL = 'https://discord.com/api'

# Discord OAuth2 URL for authorization
OAUTH2_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20email%20guilds"


# Route to display the bot's status
@app.route('/')
def home():
    return render_template('index.html', status="Bot is running!")


# API route to check bot status
@app.route('/api/status')
def bot_status():
    return jsonify({"status": "running"})


# Route for Discord OAuth2 login
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
