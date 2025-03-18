# Diskly
A very simple Discord bot to play songs/YouTube videos in your voice channels

## Motivation
Most Discord bots require some sort of subscription to play songs/videos from YouTube, which is why I have created this simple bot to use with my friends.

## Setup project
The only thing you need to do is create an `.env` file with a singular line containing `DISCORD_TOKEN=<token>`, where `token` is your Discord bot token. If you don't know how to get this, see [Create a bot on Discord](#create-a-bot-on-discord).

## Dependencies
All you need is Docker! Once it is installed, you can use the `script.sh` bash script in order to start the docker container. 

Under the hood, the program uses:

- `Python 3.12`
- `uv` for package management
- `yt_dlp` for extracting youtube information
- `discord.py` for creating bots in Python



## Create a bot on Discord
Follow the instructions [here.](https://discordpy.readthedocs.io/en/stable/discord.html)

## Current Commands
- ❓ `?help` - Show this message.
- 🏓 `?ping` - Check if the bot is online and check latency.
- ▶️ `?play` - Play a song from a YouTube URL.
- ⏸️ `?pause` - Pause the current song.
- ▶️ `?resume` - Resume the current song.
- ⏹️ `?stop` - Stop the current song.
- 👋 `?leave` - Leave the voice channel.
- 📝 `?queue` - Show the current queue.
- ⏭️ `?skip` - Skip the current song.
- 🗑️ `?clear` - Clear the queue.


## Known Issues
- Currently, the formatting of printing the queue is not correct. While it is readable, it does not look good.
