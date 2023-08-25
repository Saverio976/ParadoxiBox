import datetime
from argparse import ArgumentParser
from typing import Any

from django.core.management.base import BaseCommand

from songs.models import Song


class Command(BaseCommand):
    help = "Remove songs last used more than x days ago"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument("x", action="store", nargs=1, type=int)
        parser.add_argument("-y", action="store_true", default=False)

    def handle(self, *_: Any, **options: Any):
        x = options["x"][0]
        y = options["y"]
        songs_remove = Song.objects.filter(
            date_used__lte=datetime.datetime.now() - datetime.timedelta(days=x),
        )
        songs_remove_str = "||".join([str(song) for song in songs_remove])
        if not y:
            print("songs that will be deleted:", songs_remove_str)
            yy = input("Do you want to continue? (y/N) ")
            if yy.lower().strip() != "y":
                return
        songs_remove.delete()
        print("songs removed:", songs_remove_str)
