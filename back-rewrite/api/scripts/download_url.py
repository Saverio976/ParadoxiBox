#!/usr/bin/env python3
from typing import Optional, List, Dict, Any

from dataclasses import dataclass
from datetime import timedelta

from argparse import ArgumentParser

import sys
import orjson

import logging

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)

import yt_dlp

@dataclass
class Song:
    path: str
    title: str
    artists: str
    source_url: str
    duration: int
    thumbnail_url: str

    def __json__(self):
        return {
            "path": self.path,
            "title": self.title,
            "artists": self.artists,
            "source_url": self.source_url,
            "duration": self.duration,
            "thumbnail_url": self.thumbnail_url
        }

def download_song_ytdl(
    home_path: str, url: str, noplaylist: bool = False, format: str = "mp3"
) -> Optional[List[Song]]:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": f"{format}/bestaudio/best",
        "noplaylist": noplaylist,
        "logger": logger,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": f"{format}",
            }
        ],
        "paths": {
            "home": f"{home_path}",
        },
    }
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
            artists=artist,
            source_url=source_link,
            path=path_music,
            duration=int(duration.total_seconds()),
            thumbnail_url=thumbnail,
        )
        saved.append(song)
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
        "--home", type=str, help="The folder where to download"
    )
    result = parser.parse_args()
    songs = download_song_ytdl(
        home_path=result.home,
        url=result.url,
        noplaylist=result.noplaylist,
    )
    if not songs:
        return 1
    print(orjson.dumps({"songs": list(map(lambda x: x.__json__(), songs))}).decode('utf-8'))
    return 0

if __name__ == "__main__":
    sys.exit(main())
