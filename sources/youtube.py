"""This file handles youtube related tasks, using yt-dlp
to find the url of a song and then uses ffmped in the backend
to download it."""

import yt_dlp as ytdlp


class YouTubeHandler:
    _params_ytdlp = {
        "format": "bestaudio",
        "noplaylist": True,
        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False,
    }
    _params_ffmpeg = {
        "options": "-vn -filter:a loudnorm"  # Removes video.
        # This normalizes auto so it is always somewhat the
        # same volume.
    }

    @classmethod
    async def get_youtube_url(cls, query: str):
        with ytdlp.YoutubeDL(cls._params_ytdlp) as ytdl:
            try:
                info = ytdl.extract_info(f"ytsearch1:{query}", download=False)
                url = info["entries"][0]["url"]
                title = info["entries"][0]["title"]
                return (url, title)
            except Exception as e:
                print(e)
                return None
