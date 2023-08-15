from django.urls import path

from songs import views

app_name = "songs"
urlpatterns = [
    path("", views.index, name="index"),
    path("downloaded_songs", views.downloaded_songs, name="downloaded_songs"),
    path("newsong", views.new_song, name="new_song"),
    path("api/newsong/url", views.new_song_api_url, name="new_song_api_url"),
    path(
        "api/newsong/url/playlist",
        views.new_song_api_url_playlist,
        name="new_song_api_url_playlist",
    ),
    path("api/newsong/search", views.new_song_api_search, name="new_song_api_search"),
    path("api/pause", views.pause_api, name="pause_api"),
    path("api/resume", views.resume_api, name="resume_api"),
    path("api/skip", views.skip_api, name="skip_api"),
    path("api/stop", views.stop_api, name="stop_api"),
    path("api/improvise", views.improvise_api, name="improvise_api"),
    path("api/improvise/now", views.improvise_now_api, name="improvise_now_api"),
    path("song/<song_id>", views.song, name="song"),
    path("media/songs/<path>", views.download_song, name="media_songs"),
    path("queue/add/<song_id>", views.queue_add_song_api, name="queue_song_api"),
    path("queue", views.queue, name="queue"),
    path("library_used", views.library_used, name="library_used"),
]
