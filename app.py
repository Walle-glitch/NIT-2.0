# flask_app.py - Flask GUI and OAuth2 integration

import os
import sys
import threading
from flask import Flask, render_template, jsonify, request
from markupsafe import Markup
import requests

# Add Internal_Modules to path for config
sys.path.append(os.path.join(os.path.dirname(__file__), 'Internal_Modules'))
import _Bot_Config  # type: ignore

# Import Discord bot instance from main.py
from main import bot

app = Flask(__name__, template_folder='templates')

# Load OAuth2 credentials from config
CLIENT_ID = _Bot_Config._Client_ID()
CLIENT_SECRET = _Bot_Config._Client_Secret()
REDIRECT_URI = _Bot_Config._Redirect_URI()
DISCORD_API_BASE_URL = _Bot_Config._Discord_API_Base_URL().rstrip('/')

# Build OAuth2 URL
SCOPES = ['identify', 'email', 'guilds']
OAUTH2_URL = (
    f"{DISCORD_API_BASE_URL}/oauth2/authorize"
    f"?client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    f"&response_type=code"
    f"&scope={'+'.join(SCOPES)}"
)

# Helper to load README.md from project root
def get_readme_content():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    readme_path = os.path.join(root, 'README.md')
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            text = f.read().replace('\n', '<br>')
        return Markup(text)
    except FileNotFoundError:
        return Markup('<p><em>README.md not found.</em></p>')

# Simulated user data (to replace with real data later)
users_data = [
    {"id": 1, "name": "John Doe", "role": "Admin"},
    {"id": 2, "name": "Jane Smith", "role": "Moderator"},
    {"id": 3, "name": "Alice Johnson", "role": "Member"}
]

@app.route('/')
def home():
    """Render homepage with bot status and README.md."""
    status = "running" if bot.is_ready() else "starting"
    readme = get_readme_content()
    return render_template('home.html', status=status, readme_content=readme)

@app.route('/api/status')
def api_status():
    """Return JSON status for health checks."""
    return jsonify({"status": "running" if bot.is_ready() else "starting"})

@app.route('/users')
def users():
    """Render a user list view."""
    return render_template('users.html', users=users_data)

@app.route('/login')
def login():
    """Redirect user to Discord OAuth2 login."""
    return f'<a href="{OAUTH2_URL}">Login with Discord</a>'

@app.route('/callback')
def callback():
    """Handle OAuth2 callback and fetch user info."""
    code = request.args.get('code')
    if not code:
        return "Missing code parameter", 400

    token_url = f"{DISCORD_API_BASE_URL}/oauth2/token"
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(SCOPES)
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post(token_url, data=payload, headers=headers)
    if not resp.ok:
        return jsonify(resp.json()), resp.status_code

    access_token = resp.json().get('access_token')
    if not access_token:
        return "Error obtaining access token", 400

    # Fetch user info
    user_url = f"{DISCORD_API_BASE_URL}/users/@me"
    auth_headers = {'Authorization': f'Bearer {access_token}'}
    user_resp = requests.get(user_url, headers=auth_headers)
    return jsonify(user_resp.json())

# Run Flask app in thread
def run_flask():
    app.run(host='0.0.0.0', port=int(os.getenv('FLASK_PORT', 5000)))

if __name__ == '__main__':
    # Start Flask
    threading.Thread(target=run_flask, daemon=True).start()
    # Start Discord bot
    token = os.getenv('DISCORD_TOKEN')
    bot.run(token)
