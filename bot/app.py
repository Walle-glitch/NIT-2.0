from flask import Flask, render_template, jsonify
import threading
import main as bot # Import bot.py
import __Modules as _M # All Bot specific Moduels 

app = Flask(__name__)

# A route to display the bot status
@app.route('/')
def home():
    return render_template('index.html', status="Bot is running!")

# API route to check bot status
@app.route('/api/status')
def bot_status():
    return jsonify({"status": "running"})

# Start the Flask server
def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    # Use threading to run Flask and Discord bot in parallel
    flask_thread = threading.Thread(target=run_flask_app)
    discord_bot_thread = threading.Thread(target=bot.run_discord_bot)

    # Start the threads
    flask_thread.start()
    discord_bot_thread.start()
