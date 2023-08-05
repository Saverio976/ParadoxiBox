from django.urls import path

from . import views

app_name = "songs"
urlpatterns = [
    path("", views.index, name="index"),
    path("downloaded_songs", views.downloaded_songs, name="downloaded_songs"),
    path("newsong", views.new_song, name="new_song"),
    path("api/newsong", views.new_song_api, name="new_song_api"),
    path("song/<song_id>", views.song, name="song"),
    path("media/songs/<path>", views.download_song, name="media_songs"),
    path("queue/add/<song_id>", views.queue_add_song_api, name="queue_song_api"),
    path("queue", views.queue, name="queue"),
]
