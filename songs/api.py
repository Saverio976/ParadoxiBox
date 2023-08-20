from typing import List, Literal, Optional
from ninja import NinjaAPI, Schema
from songs.player import PLAYER
from songs.models import Song
from songs.song_download_helper import download_song_helper

api = NinjaAPI(title="ParadoxiBox")

class SongSchema(Schema):
    id: str
    title: str
    artist: str
    source_link: str
    duration_second: float
    thumbnail_url: str
    file_url: str

class CurrentSongSchema(Schema):
    song: Optional[SongSchema] = None
    song_pos: Optional[float] = None

class CurrentSongPosPercent(Schema):
    pos: Optional[int] = None # between 0 and 100
    """
    between 0 and 100
    """

class QueueAddSchema(Schema):
    status: Literal["downloading", "added", "error"]

class PausedStatusSchema(Schema):
    paused: bool

class AutoImproviseStatusSchema(Schema):
    improvise: bool

class VolumeStatusSchema(Schema):
    volume: int
    """
    between 0 and 100
    """

# QUEUE / CURRENT

@api.get("/queue", response=List[SongSchema])
def get_queue(_):
    cur_song, _ = PLAYER.get_current_song()
    if cur_song is None:
        return {"queue": []}
    values = [cur_song.to_json()] + [
        song.to_json()
        for song in PLAYER.get_list_song()
    ]
    return {"queue": values}

@api.get("/queue/current", response=CurrentSongSchema)
def get_current(_):
    cur_song, timed = PLAYER.get_current_song()
    if cur_song is None:
        return {"current": None}
    return {"song": cur_song.to_json(), "song_pos": timed.total_seconds()}

@api.get("/queue/next")
def next(_):
    PLAYER.next()

@api.get("/queue/current/pos/set", response=CurrentSongPosPercent)
def set_current_pos(_, pos: int):
    """
    pos: int
        between 0 and 100
    """
    pos = max(0, min(100, pos))
    if PLAYER.get_current_song()[0] is None:
        return {"pos": None}
    PLAYER.set_song_time(pos)
    return {"pos": PLAYER.get_song_time()}

@api.get("/queue/current/pos", response=CurrentSongPosPercent)
def get_current_pos(_):
    if PLAYER.get_current_song()[0] is None:
        return {"pos": None}
    return {"pos": PLAYER.get_song_time()}

@api.get("/queue/add/song/url", response=QueueAddSchema)
def add_song_url(_, url: str):
    download_song_helper(
        f"{url}",
        noplaylist=True,
        to_execute=lambda song: PLAYER.queue(song),
        threaded=True,
    )
    return {"status": "downloading"}

@api.get("/queue/add/song/id")
def add_song_id(_, song_id: str):
    try:
        song = Song.objects.get(id=song_id)
    except:
        return {"status": "error"}
    PLAYER.queue(song)
    return {"status": "added"}

@api.get("/queue/add/song/search")
def add_song_search(_, search: str):
    download_song_helper(
        f"ytsearch:{search}",
        noplaylist=True,
        to_execute=lambda song: PLAYER.queue(song),
        threaded=True,
    )
    return {"status": "downloading"}

@api.get("/queue/add/playlist/url", response=QueueAddSchema)
def add_playlist_url(_, url: str):
    download_song_helper(
        f"{url}",
        noplaylist=False,
        to_execute=lambda song: PLAYER.queue(song),
        threaded=True,
    )
    return {"status": "downloading"}

# PAUSE / RESUME /STOP

@api.get("/pause")
def pause_true(_):
    PLAYER.pause()

@api.get("/resume")
def pause_false(_):
    PLAYER.resume()

@api.get("/is-paused", response=PausedStatusSchema)
def is_paused(_):
    return {"paused": PLAYER.get_paused()}

@api.get("/stop")
def stop(_):
    PLAYER.stop()

# IMPROVISE

@api.get("/improvise/now")
def improvise(_, n: int):
    PLAYER.improvise_now(n)

@api.get("/improvise/auto/toggle", response=AutoImproviseStatusSchema)
def improvise_auto_toggle():
    PLAYER.toggle_improvise()
    return {"improvise": PLAYER.get_improvise()}

@api.get("/improvise/auto", response=AutoImproviseStatusSchema)
def improvise_auto():
    return {"improvise": PLAYER.get_improvise()}

# VOLUME

@api.get("/volume", response=VolumeStatusSchema)
def get_volume(_):
    return {"volume": PLAYER.get_volume()}

@api.get("/volume/set", response=VolumeStatusSchema)
def set_volume(_, volume: int):
    """
    volume: int
        between 0 and 100
    """
    volume = max(0, min(100, volume))
    PLAYER.set_volume(volume)
    return {"volume": PLAYER.get_volume()}
