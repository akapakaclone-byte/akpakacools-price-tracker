import discord
from discord.ext import commands
import sqlite3
from datetime import datetime

import os

TOKEN = os.getenv("DISCORD_TOKEN")

# Create the database
db = sqlite3.connect("prices.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT NOT NULL,
    price REAL NOT NULL,
    timestamp TEXT NOT NULL
)
""")

db.commit()

# Discord setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    print(f"Message received: {message.content}")

    if ":" in message.content:
        parts = message.content.split(":", 1)

        item = parts[0].strip()
        price_text = parts[1].strip().lower().replace(",", "")

        try:
            if price_text.endswith("k"):
                price = float(price_text[:-1]) * 1_000

            elif price_text.endswith("m"):
                price = float(price_text[:-1]) * 1_000_000

            elif price_text.endswith("b"):
                price = float(price_text[:-1]) * 1_000_000_000

            else:
                price = float(price_text)

            timestamp = datetime.now().isoformat()

            cursor.execute(
                "INSERT INTO prices (item, price, timestamp) VALUES (?, ?, ?)",
                (item, price, timestamp)
            )

            db.commit()

            print(f"Saved: {item} = {price}")

        except ValueError:
            print(f"Could not understand price: {price_text}")

    await bot.process_commands(message)


bot.run(TOKEN)