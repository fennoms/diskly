import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot import Bot

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = commands.Bot(command_prefix="?", intents=intents, help_command=None)


async def load_cogs():
    cogs = [Bot]
    for cog in cogs:
        await client.add_cog(cog(client))


async def main():
    await load_cogs()
    await client.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
