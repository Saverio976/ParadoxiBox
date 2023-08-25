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
    date_used = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.artist} - {self.title} ({self.duration})"

    def to_json(self):
        return {
            "id": str(self.id),
            "title": str(self.title),
            "artist": str(self.artist),
            "source_link": str(self.source_link),
            "duration_second": self.duration.total_seconds(),
            "thumbnail_url": str(self.thumbnail),
            "file_url": str(self.path_music.url),
        }
