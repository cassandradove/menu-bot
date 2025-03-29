import discord
import os
import asyncio
from flask import Flask, jsonify # type: ignore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Flask app setup
app = Flask(__name__)

# Store the latest message
latest_message = {"message": "No messages yet", "author": "Unknown"}

# Discord bot setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Required to read messages

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    """Updates latest_message when a new message is sent in the target channel."""
    global latest_message
    if message.channel.id == CHANNEL_ID and not message.author.bot:
        latest_message["message"] = message.content
        latest_message["author"] = message.author.name
        print(f"Updated latest message: {latest_message}")

@app.route("/latest-message", methods=["GET"])
def get_latest_message():
    """API endpoint to return the latest message."""
    return jsonify(latest_message)

def run_discord_bot():
    """Runs the Discord bot."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start(TOKEN))

# Run the bot in a separate thread
import threading
threading.Thread(target=run_discord_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use Railway's assigned port
    app.run(host="0.0.0.0", port=port)