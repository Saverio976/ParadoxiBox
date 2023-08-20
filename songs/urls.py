from django.urls import path

from songs import views

app_name = "songs"
urlpatterns = [
    path("", views.index, name="index"),
    path("library_used", views.library_used, name="library_used"),
]
