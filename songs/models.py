from django.db import models
import datetime

# Create your models here.

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    source_link = models.URLField(max_length=255)
    path_music = models.FileField(upload_to='songs/')
    duration = models.DurationField()
    thumbnail = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.artist} - {self.title} ({self.duration})"

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        all_songs = self.songs.all()
        duration = datetime.timedelta(0)
        for dur in [song.duration for song in all_songs]:
            duration = duration + dur
        return f"{self.name} [{len(all_songs)} song(s) = {duration}]"
