from pathlib import Path
from threading import Thread

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.static import serve

from .models import Song
from .player import PLAYER
from .song_download_helper import download_song_helper


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


def new_song_api_search(request):
    search = request.POST["search"]
    to_queue = True if request.POST.get("to_queue", False) else False
    download_song_helper(f"ytsearch:{search}", noplaylist=True, threaded=True, add_to_queue=to_queue)
    if to_queue:
        return HttpResponseRedirect(reverse("songs:queue"))
    return HttpResponseRedirect(reverse("songs:downloaded_songs"))

def new_song_api_url(request):
    url = request.POST["url"]
    to_queue = True if request.POST.get("to_queue", False) else False
    download_song_helper(f"{url}", noplaylist=True, threaded=True, add_to_queue=to_queue)
    if to_queue:
        return HttpResponseRedirect(reverse("songs:queue"))
    return HttpResponseRedirect(reverse("songs:downloaded_songs"))


def new_song_api_url_playlist(request):
    url = request.POST["url"]
    to_queue = True if request.POST.get("to_queue", False) else False
    download_song_helper(f"{url}", noplaylist=False, threaded=True, add_to_queue=to_queue)
    if to_queue:
        return HttpResponseRedirect(reverse("songs:queue"))
    return HttpResponseRedirect(reverse("songs:downloaded_songs"))


def new_song(request):
    template = loader.get_template("songs/new_song.html")
    context = {}
    return HttpResponse(template.render(context, request))


def download_song(request, path):
    path_song = Path("songs") / path
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
    context = {
        "playlists": playlist,
        "song_curr": current_song,
        "song_curr_id": str(current_song.id),
        "paused": PLAYER.get_paused(),
        "improvised": PLAYER.get_improvise(),
    }
    return HttpResponse(template.render(context, request))

def pause_api(_):
    PLAYER.pause()
    return HttpResponseRedirect(reverse("songs:queue"))

def resume_api(_):
    PLAYER.resume()
    return HttpResponseRedirect(reverse("songs:queue"))

def skip_api(_):
    PLAYER.next()
    return HttpResponseRedirect(reverse("songs:queue"))

def improvise_api(_):
    PLAYER.toggle_improvise()
    return HttpResponseRedirect(reverse("songs:queue"))
