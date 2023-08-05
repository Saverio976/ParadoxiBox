from django.urls import reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.views.static import serve
from pathlib import Path
import datetime

import yt_dlp

from .models import Song
from .player import PLAYER

def index(request):
    template = loader.get_template("songs/index.html")
    context = {}
    return HttpResponse(template.render(context, request))

def downloaded_songs(request):
    all_songs = Song.objects.all()
    template = loader.get_template("songs/downloaded_songs.html")
    context = {"songs": all_songs}
    return HttpResponse(template.render(context, request))

def song(request, song_id):
    song = Song.objects.get(id=song_id)
    template = loader.get_template("songs/song.html")
    context = {"song": song, "song_id": song_id}
    return HttpResponse(template.render(context, request))

def new_song_api(request):
    title = request.POST["title"]
    artist = request.POST["artist"]
    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        "paths": {
            "home": f"{settings.MEDIA_ROOT / 'songs'}",
        },
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        infos = ydl.extract_info(f"ytsearch:{artist} {title}", download=True)
    if not infos:
        return HttpResponse("No songs found")
    source_link = infos["entries"][0]["webpage_url"]
    path_music = infos["entries"][0]["requested_downloads"][0]["filepath"]
    duration = datetime.timedelta(seconds=infos["entries"][0]["duration"])
    thumbnail = infos["entries"][0]["thumbnail"]
    song = Song(title=title, artist=artist, source_link=source_link, path_music=path_music, duration=duration, thumbnail=thumbnail)
    song.save()
    return HttpResponseRedirect(reverse("songs:downloaded_songs"))

def new_song(request):
    template = loader.get_template("songs/new_song.html")
    context = {}
    return HttpResponse(template.render(context, request))

def download_song(request, path):
    path_song = Path("songs") / path
    print(path_song)
    return serve(request, path_song, document_root=settings.MEDIA_ROOT)

def queue_add_song_api(_, song_id):
    song = Song.objects.get(id=song_id)
    PLAYER.queue(song)
    return HttpResponseRedirect(reverse("songs:queue"))

def queue(request):
    playlist = PLAYER.get_list_song()
    current_song = PLAYER.get_current_song()
    if current_song is None:
        template = loader.get_template("songs/queue_empty.html")
        context = {}
        return HttpResponse(template.render(context, request))
    template = loader.get_template("songs/queue.html")
    context = {"playlists": playlist, "song_curr": current_song, "song_curr_id": str(current_song.id)}
    return HttpResponse(template.render(context, request))
