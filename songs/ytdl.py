from typing import Tuple
import yt_dlp
from ytmusicapi.ytmusic import YTMusic
from datetime import timedelta
from .models import Song

def video_id_to_url(video_id: str) -> str:
    return f"https://music.youtube.com/watch?v={video_id}"

def search_song(query: str) -> Tuple[str, str]:
    yt = YTMusic()
    results = yt.search(query, filter = "songs")
    videoId = resuls[0]["videoId"]
    return search_song(videoId), videoId

def get_next_related(query: str, limit: int = -1) -> List[str]:
    _, videoId = search_song(query)
    yt = YTMusic()
    playlist = yt.get_watch_playlist(videoId)
    nexts = yt.get_song_related(playlist["related"])
    res = [item["videoId"] for item in nexts[0]["contents"]]
    if limit > 0:
        res = res[:limit]
    return res

def download_song_ytdl(home_path: str, search: str, noplaylist: bool = False):
    if search.startswith("ytsearch:"):
        search = search[:len("ytsearch:")]
        search = search_song(search)
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
    saved = []
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
        saved.append(song)
    return saved
