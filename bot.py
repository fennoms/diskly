"""This file holds all the main bot commands."""

from discord.ext import commands


class Bot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        commands = [
            "- ❓ `?help` - Show this message.",
            "- 🏓 `?ping` - Check if the bot is online and check latency.",
            "- ▶️ `?play` - Play a song from a YouTube URL.",
            "- ⏸️ `?pause` - Pause the current song.",
            "- ▶️ `?resume` - Resume the current song.",
            "- ⏹️ `?stop` - Stop the current song.",
            "- 👋 `?leave` - Leave the voice channel.",
            "- 📝 `?queue` - Show the current queue.",
            "- ⏭️ `?skip` - Skip the current song.",
            "- 🗑️ `?clear` - Clear the queue.",
            "- ❌ `?remove` - Remove a song from the queue.",
        ]
        message = "\n".join(commands)
        await ctx.send(message)
