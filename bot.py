"""This file holds all the main bot commands. It holds
the commands to add songs to the queue, play, skip,
pause, resume and so on. The help command shows all the
currently available commands."""

import discord
from discord.ext import commands

from songqueue import Queue
from sources.youtube import YouTubeHandler


class Bot(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client
        self._queue: Queue = Queue()

    @commands.command()
    async def skip(self, ctx: commands.Context):
        """Skip the current song, play the next one.

        Args:
            ctx (commands.Context): The context of the command.
        """
        if ctx.voice_client is None:
            return await ctx.send("I'm not in a voice channel! ❌")

        ctx.voice_client.stop()
        await self._play_song(ctx)

    @commands.command()
    async def queue(self, ctx: commands.Context):
        """Print the current queue. Implemented by
        Queue dunder method.

        Args:
            ctx (commands.Context): The context of the command.
        """
        await ctx.send(str(self._queue))

    @commands.command()
    async def clear(self, ctx: commands.Context):
        """Clear the queue.

        Args:
            ctx (commands.Context): The context of the command.
        """
        await self._queue.clear()
        await ctx.send("Queue cleared! ✅")

    @commands.command()
    async def stop(self, ctx: commands.Context):
        """Stop the bot. This means stopping the
        music, and clearing the queue.

        Args:
            ctx (commands.Context): _description_
        """
        if ctx.voice_client is None:
            return await ctx.send("I'm not in a voice channel! ❌")

        await self.clear(ctx)
        ctx.voice_client.stop()

    @commands.command()
    async def leave(self, ctx: commands.Context):
        """Leave the voice channel.

        Args:
            ctx (commands.Context): The context of the command.
        """
        if ctx.voice_client is None:
            return await ctx.send("I'm not in a voice channel! ❌")

        await self.stop(ctx)
        await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx: commands.Context):
        """Pause the current song.

        Args:
            ctx (commands.Context): The context of the command.
        """
        ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx: commands.Context):
        """Resume the current song.

        Args:
            ctx (commands.Context): The context of the command.
        """
        ctx.voice_client.resume()

    async def _join_voice_channel(self, ctx: commands.Context):
        """Join the voice channel of the user. Can fail, and
        sends a message if it does.

        Args:
            ctx (commands.Context): The context of the command.
        """
        voice_channel = ctx.author.voice.channel
        try:
            await voice_channel.connect()
            return None
        except Exception as e:
            return str(e)

    async def _search_song(self, ctx: commands.Context, query: str):
        """Search a song (now only on YouTube) and return its
        url and title. Can fail, and sends a message and returns
        None if it does.

        Args:
            ctx (commands.Context): _description_
            query (str): _description_

        Returns:
            _type_: _description_
        """
        await ctx.send(f"🔍 Searching for: {query}")

        ## Fetch URL
        # Attempt all types of URLs, the functions we call here
        # will return if the URL is invalid for that search engine.
        url, title = await YouTubeHandler.get_youtube_url(query)
        if url is None:
            await ctx.send("No song found! ❌")

        return url, title

    @commands.command()
    async def play(self, ctx, *, query: str):
        """Play a song from a query (str or URL).
        If the bot is not in a voice channel, it will join
        the voice channel. Can fail if it doesn't find the song,
        and sends a message if it does.

        Args:
            ctx (commands.Context): The context of the command.
            query (str): The query entered by the user.
        """
        # User must be inside of a voice channel
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel is None:
            return await ctx.send("Join a voice channel first! ❌")

        if error := await self._join_voice_channel(ctx) and ctx.voice_client is None:
            return await ctx.send(f"Failed to join voice channel: {error} ❌")

        url, title = await self._search_song(ctx, query)
        if url is None:
            return

        ## Everything is always added to the queue
        await self._queue.add(url, title)
        await ctx.send(f"🎵 Added to queue: {title}")

        if not ctx.voice_client.is_playing():
            await self._play_song(ctx)

    async def _play_song(self, ctx: commands.Context):
        """Plays the next song in the queue. Also
        sends a message to the channel.

        Args:
            ctx (commands.Context): The context of the command.
        """
        if len(self._queue.queue) == 0:
            return

        url, title = await self._queue.pop(0)
        source = discord.FFmpegPCMAudio(url, **YouTubeHandler._params_ffmpeg)
        ctx.voice_client.play(
            source, after=lambda x: self.client.loop.create_task(self._play_song(ctx))
        )
        await ctx.send(f"🎵 Now playing: {title}")

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Send a ping message and send latency to bot.

        Args:
            ctx (commands.Context): The context of the command.
        """
        latency = round(self.client.latency * 1000)
        await ctx.send(f"Bot is online! ✅ Latency: {latency}ms")

    @commands.command()
    async def help(self, ctx: commands.Context):
        """Print the help message.

        Args:
            ctx (commands.Context): The context of the command.
        """
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
