"""This file holds all the main bot commands."""

import discord
from discord.ext import commands

from sources.youtube import YouTubeHandler


class Bot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def play(self, ctx, *, query: str):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel is None:
            return await ctx.send("Join a voice channel first! ❌")

        if ctx.voice_client is None:
            await voice_channel.connect()
        elif ctx.voice_client.channel != voice_channel:
            return await ctx.send("You are in the wrong voice channel! ❌")

        await ctx.send(f"🔍 Searching for: {query}")

        # Attempt all types of URLs, the functions we call here
        # will return if the URL is invalid for that search engine.
        url, title = await YouTubeHandler.get_youtube_url(query)

        if url is None:
            return await ctx.send("No song found! ❌")

        await ctx.send(f"Playing: {title}")
        source = await discord.FFmpegOpusAudio.from_probe(
            url, **YouTubeHandler._params_ffmpeg
        )
        ctx.voice_client.play(source)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(
            f"Bot is online! ✅ Latency: {round(self.client.latency * 1000)}ms"
        )

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
