#!/bin/bash
from typing import Tuple

from argparse import ArgumentParser

import sys

from ytmusicapi.ytmusic import YTMusic

def logger_print(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def video_id_to_url(video_id: str) -> str:
    return f"https://music.youtube.com/watch?v={video_id}"

def search_song(query: str) -> Tuple[str, str]:
    yt = YTMusic()
    results = yt.search(query, filter="songs", limit=1)
    videoId = results[0]["videoId"]
    return video_id_to_url(videoId), videoId


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument(
        "query", type=str, help="The query to search."
    )
    result = parser.parse_args()
    song_url, _ = search_song(result.query)
    print(song_url)
    return 0

if __name__ == "__main__":
    sys.exit(main())
