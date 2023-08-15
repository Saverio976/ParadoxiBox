from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.static import serve

from .models import Song
from .player import PLAYER
from .song_download_helper import download_song_helper


def index(request: HttpRequest):
    template = loader.get_template("songs/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def downloaded_songs(request: HttpRequest):
    all_songs = Song.objects.all()
    template = loader.get_template("songs/downloaded_songs.html")
    context = {"songs": all_songs}
    return HttpResponse(template.render(context, request))


def song(request: HttpRequest, song_id: str):
    song = Song.objects.get(id=song_id)
    template = loader.get_template("songs/song.html")
    context = {"song": song, "song_id": song_id}
    return HttpResponse(template.render(context, request))


def new_song_api_search(request: HttpRequest):
    search = str(request.POST["search"])
    to_queue = True if request.POST.get("to_queue", False) else False
    download_song_helper(
        f"ytsearch:{search}",
        noplaylist=True,
        to_execute=lambda song: PLAYER.queue(song),
        threaded=True,
    )
    if to_queue:
        return HttpResponseRedirect(reverse("songs:queue"))
    return HttpResponseRedirect(reverse("songs:downloaded_songs"))


def new_song_api_url(request: HttpRequest):
    url = request.POST["url"]
    to_queue = True if request.POST.get("to_queue", False) else False
    download_song_helper(
        f"{url}",
        noplaylist=True,
        to_execute=lambda song: PLAYER.queue(song),
        threaded=True,
    )
    if to_queue:
        return HttpResponseRedirect(reverse("songs:queue"))
    return HttpResponseRedirect(reverse("songs:downloaded_songs"))


def new_song_api_url_playlist(request: HttpRequest):
    url = request.POST["url"]
    to_queue = True if request.POST.get("to_queue", False) else False
    download_song_helper(
        f"{url}",
        noplaylist=False,
        to_execute=lambda song: PLAYER.queue(song),
        threaded=True,
    )
    if to_queue:
        return HttpResponseRedirect(reverse("songs:queue"))
    return HttpResponseRedirect(reverse("songs:downloaded_songs"))


def new_song(request: HttpRequest):
    template = loader.get_template("songs/new_song.html")
    context = {}
    return HttpResponse(template.render(context, request))


def download_song(request: HttpRequest, path: str):
    path_song = Path("songs") / path
    return serve(request, path_song, document_root=settings.MEDIA_ROOT)


def queue_add_song_api(_, song_id: str):
    song = Song.objects.get(id=song_id)
    PLAYER.queue(song)
    return HttpResponseRedirect(reverse("songs:queue"))


def queue(request: HttpRequest):
    playlist = PLAYER.get_list_song()
    current_song, timed = PLAYER.get_current_song()
    if current_song is None:
        template = loader.get_template("songs/queue_empty.html")
        context = {}
        return HttpResponse(template.render(context, request))
    template = loader.get_template("songs/queue.html")
    context = {
        "playlists": playlist,
        "song_curr": current_song,
        "song_curr_id": str(current_song.id),
        "song_curr_timed": timed,
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


def improvise_now_api(_):
    PLAYER.improvise_now()
    return HttpResponseRedirect(reverse("songs:queue"))


def library_used(request: HttpRequest):
    template = loader.get_template("songs/library_used.html")
    context = {}
    return HttpResponse(template.render(context, request))


def stop_api(_):
    PLAYER.stop()
    return HttpResponseRedirect(reverse("songs:index"))
