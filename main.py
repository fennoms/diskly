import os

import discord
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    client.run(os.getenv("DISCORD_TOKEN"))
