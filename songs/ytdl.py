import yt_dlp
from datetime import timedelta
from .models import Song

def download_song_ytdl(home_path: str, search: str, noplaylist: bool = False):
    print(noplaylist)
    ydl_opts = {
        "format": "mp3/bestaudio/best",
        "noplaylist": noplaylist,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
        "paths": {
            "home": f"{home_path}",
        },
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        infos = ydl.extract_info(f"{search}", download=True)
    if not infos:
        return None
    if noplaylist:
        infos["entries"] = infos["entries"][:1]
    for entry in infos["entries"]:
        source_link = entry["webpage_url"]
        path_music = entry["requested_downloads"][0]["filepath"]
        duration = timedelta(seconds=entry["duration"])
        thumbnail = entry["thumbnail"]
        artist = entry["channel"]
        title = entry["title"]
        song = Song(
            title=title,
            artist=artist,
            source_link=source_link,
            path_music=path_music,
            duration=duration,
            thumbnail=thumbnail,
        )
        song.save()
