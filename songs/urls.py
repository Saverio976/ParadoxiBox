from django.urls import path, re_path

from . import views

app_name = "songs"
urlpatterns = [
    path("", views.index, name="index"),
    path("downloaded_songs", views.downloaded_songs, name="downloaded_songs"),
    path("playlists", views.playlists, name="playlists"),
    path("newsong", views.new_song, name="new_song"),
    path("api/newsong", views.new_song_api, name="new_song_api"),
    path("song/<int:song_id>", views.song, name="song"),
    path("media/songs/<path>", views.download_song, name="media_songs"),
]
