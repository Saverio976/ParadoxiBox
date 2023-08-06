# Generated by Django 4.2.4 on 2023-08-05 19:48

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Song",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("artist", models.CharField(max_length=255)),
                ("source_link", models.URLField(max_length=255)),
                ("path_music", models.FileField(upload_to="songs/")),
                ("duration", models.DurationField()),
                ("thumbnail", models.URLField(max_length=500)),
            ],
        ),
    ]
