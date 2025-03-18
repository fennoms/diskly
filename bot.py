"""This file holds all the main bot commands."""

import discord
from discord.ext import commands

from songqueue import Queue
from sources.youtube import YouTubeHandler


class Bot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._queue: Queue = Queue()

    @commands.command()
    async def skip(self, ctx):
        await ctx.voice_client.stop()
        await self._play_song(ctx)

    @commands.command()
    async def queue(self, ctx):
        await ctx.send(str(self._queue))

    @commands.command()
    async def clear(self, ctx):
        await self._queue.clear()
        await ctx.send("Queue cleared! ✅")

    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I'm not in a voice channel! ❌")

        await self.stop(ctx)
        await self.clear(ctx)
        await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()

    @commands.command()
    async def play(self, ctx, *, query: str):
        ## Connect to voice channel
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel is None:
            return await ctx.send("Join a voice channel first! ❌")

        if ctx.voice_client is None:
            await voice_channel.connect()
        elif ctx.voice_client.channel != voice_channel:
            return await ctx.send("You are in the wrong voice channel! ❌")

        await ctx.send(f"🔍 Searching for: {query}")

        ## Fetch URL
        # Attempt all types of URLs, the functions we call here
        # will return if the URL is invalid for that search engine.
        url, title = await YouTubeHandler.get_youtube_url(query)
        if url is None:
            return await ctx.send("No song found! ❌")

        ## Everything is always added to the queue
        await self._queue.add(url, title)
        await ctx.send(f"🎵 Added to queue: {title}")

        if not ctx.voice_client.is_playing():
            await self._play_song(ctx)

    async def _play_song(self, ctx):
        if len(self._queue.queue) == 0:
            return

        url, title = await self._queue.pop(0)
        source = discord.FFmpegPCMAudio(url, **YouTubeHandler._params_ffmpeg)
        ctx.voice_client.play(
            source, after=lambda x: self.client.loop.create_task(self._play_song(ctx))
        )
        await ctx.send(f"🎵 Now playing: {title}")

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
        ]
        message = "\n".join(commands)
        await ctx.send(message)
