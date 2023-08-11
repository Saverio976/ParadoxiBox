from typing import Tuple, List
import yt_dlp
from ytmusicapi.ytmusic import YTMusic
from datetime import timedelta
from .models import Song
from .logger import logger_print

def video_id_to_url(video_id: str) -> str:
    return f"https://music.youtube.com/watch?v={video_id}"

def search_song(query: str) -> Tuple[str, str]:
    yt = YTMusic()
    results = yt.search(query, filter = "songs")
    videoId = results[0]["videoId"]
    return search_song(videoId), videoId

def get_next_related(query: str, limit: int = -1) -> List[str]:
    _, videoId = search_song(query)
    logger_print(videoId)
    yt = YTMusic()
    playlist = yt.get_watch_playlist(videoId)
    logger_print("result from watch list")
    nexts = yt.get_song_related(playlist["related"])
    logger_print("result from related list")
    res = []
    if limit <= 0:
        limit = len(nexts[0]["contents"])
    res = [item["videoId"] for item in nexts[0]["contents"][:limit]]
    return res

def download_song_ytdl(home_path: str, search: str, noplaylist: bool = False):
    if search.startswith("ytsearch:"):
        search = search[:len("ytsearch:")]
        search, _ = search_song(search)
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
        datas = ydl.extract_info(f"{search}", download=True)
    if not datas:
        return None
    infos = {"entries": []}
    if noplaylist:
        infos["entries"] = [datas]
    else:
        infos["entries"] = datas["entries"]
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
