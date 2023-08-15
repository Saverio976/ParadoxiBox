import uuid

from django.db import models

# Create your models here.


class Song(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    source_link = models.URLField(max_length=255)
    path_music = models.FileField(upload_to="songs/")
    duration = models.DurationField()
    thumbnail = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.artist} - {self.title} ({self.duration})"
