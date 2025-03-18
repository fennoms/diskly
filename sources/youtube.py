import yt_dlp as ytdlp


class YouTubeHandler:
    _params_ytdlp = {
        "format": "bestaudio",
        "noplaylist": True,
        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False,
    }
    _params_ffmpeg = {
        "options": "-vn"  # This removes video giving only audio
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
