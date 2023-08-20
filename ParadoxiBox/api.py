from typing import List, Optional
from ninja import NinjaAPI, Schema
from songs.api import router as router_songs
from uuser.api import router as router_uuser

from ParadoxiBox import __version__

api = NinjaAPI(title="ParadoxiBox")
api.add_router("/songs/", router_songs)
api.add_router("/auth/", router_uuser)


class IndexSchema(Schema):
    welcome: str
    version: str = __version__
    annoucement: Optional[str] = None


class CreditSchema(Schema):
    type: str
    s: str
    link: str

class CreditsSchema(Schema):
    credits: List[CreditSchema]


@api.get("/index", response=IndexSchema)
def index_page(_):
    return {"welcome": "Welcome to ParadoxiBox"}

@api.get("/credits", response=CreditsSchema)
def credits(_):
    return {
        "credits": [
            {
                "type": "python module",
                "s": "django",
                "link": "https://www.djangoproject.com/"
            },
            {
                "type": "python module",
                "s": "yt-dlp",
                "link": "https://github.com/yt-dlp/yt-dlp"
            },
            {
                "type": "python module",
                "s": "pygame",
                "link": "https://www.pygame.org/"
            },
            {
                "type": "python module",
                "s": "daphne",
                "link": "https://github.com/django/daphne"
            },
            {
                "type": "python module",
                "s": "ytmusicapi",
                "link": "https://ytmusicapi.readthedocs.io"
            },
            {
                "type": "python module",
                "s": "django-cleanup",
                "link": "https://github.com/un1t/django-cleanup"
            },
            {
                "type": "python module",
                "s": "twisted",
                "link": "https://twisted.org/"
            },
            {
                "type": "python module",
                "s": "django-ninja",
                "link": "https://django-ninja.rest-framework.com/"
            },
            {
                "type": "contributor",
                "s": "KitetsuK",
                "link": "https://github.com/KitetsuK/"
            },
            {
                "type": "contributor",
                "s": "Saverio976",
                "link": "https://github.com/Saverio976/"
            },
        ]
    }
