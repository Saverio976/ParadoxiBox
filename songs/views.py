from django.urls import reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.views.static import serve
import os
from pathlib import Path
import datetime

import yt_dlp

from .models import Song, Playlist

def index(request):
    template = loader.get_template("songs/index.html")
    context = {}
    return HttpResponse(template.render(context, request))

def downloaded_songs(request):
    all_songs = Song.objects.all()
    template = loader.get_template("songs/downloaded_songs.html")
    context = {"songs": all_songs}
    return HttpResponse(template.render(context, request))

def playlists(_):
    output = "".join([f"- {playlist}\n" for playlist in Playlist.objects.all()])
    if output:
        return HttpResponse(output)
    return HttpResponse("No Playlists for now")

def song(request, song_id):
    song = Song.objects.get(id=song_id)
    template = loader.get_template("songs/song.html")
    context = {"song": song}
    return HttpResponse(template.render(context, request))

def new_song_api(request):
    title = request.POST["title"]
    artist = request.POST["artist"]
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        "paths": {
            "home": f"{os.environ['HOME']}/Music",
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
