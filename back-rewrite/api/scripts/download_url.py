#!/usr/bin/env python3
from typing import Optional, List, Dict, Any

from dataclasses import dataclass
from datetime import timedelta

from argparse import ArgumentParser

import sys
import os

import yt_dlp

def logger_print(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)

@dataclass
class Song:
    title: str
    artist: List[str]
    source_link: str
    path_music: str
    duration: str
    thumbnail: str

def download_song_ytdl(
    output: str, url: str, noplaylist: bool = False, format: str = "mp3"
) -> Optional[List[Song]]:
    ydl_opts = {
        "format": f"{format}/bestaudio/best",
        "noplaylist": noplaylist,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": f"{format}",
            }
        ],
        "paths": {
            "home": f"{os.path.dirname(output)}",
        },
    }
    logger_print(f"YTDLP:: downloading:: noplaylist={noplaylist}: url={url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        datas = ydl.extract_info(f"{url}", download=True)
    if not datas:
        return None
    infos: Dict[str, List[Any]] = {"entries": []}
    if noplaylist:
        if "entries" in datas.keys():
            entries = datas["entries"][:1]
            if isinstance(entries, list):
                infos["entries"] = entries
        else:
            infos["entries"] = [datas]
    else:
        entries = datas["entries"]
        if isinstance(entries, list):
            infos["entries"] = entries
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
            duration=str(int(duration.total_seconds())),
            thumbnail=thumbnail,
        )
        saved.append(song)
    logger_print(f"YTDLP:: download finished:: url={url}")
    return saved

def main() -> int:
    parser = ArgumentParser()
    parser.add_argument(
        "url", type=str, help="The url to download."
    )
    parser.add_argument(
        "--noplaylist", action="store_true", default=False, help="Do not download a playlist."
    )
    parser.add_argument(
        "--format", type=str, default="mp3", help="The format to download."
    )
    parser.add_argument(
        "--output", type=str, help="The file output"
    )
    result = parser.parse_args()
    songs = download_song_ytdl(
        home_path=result.home,
        url=result.url,
        noplaylist=result.noplaylist,
    )
    if not songs:
        return 1
    for song in songs:
        print(song)
    return 0

if __name__ == "__main__":
    sys.exit(main())
