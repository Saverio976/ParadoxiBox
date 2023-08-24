from typing import List, Optional

import requests

import orjson
from ninja import NinjaAPI, Schema
from ninja.renderers import BaseRenderer

from ParadoxiBox import __version__
from songs.api import router as router_songs
from uuser.api import router as router_uuser
from uuser.api import AuthBearer


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)


api = NinjaAPI(title="ParadoxiBox", renderer=ORJSONRenderer())
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
                "link": "https://www.djangoproject.com/",
            },
            {
                "type": "python module",
                "s": "yt-dlp",
                "link": "https://github.com/yt-dlp/yt-dlp",
            },
            {"type": "python module", "s": "pygame", "link": "https://www.pygame.org/"},
            {
                "type": "python module",
                "s": "daphne",
                "link": "https://github.com/django/daphne",
            },
            {
                "type": "python module",
                "s": "ytmusicapi",
                "link": "https://ytmusicapi.readthedocs.io",
            },
            {
                "type": "python module",
                "s": "django-cleanup",
                "link": "https://github.com/un1t/django-cleanup",
            },
            {"type": "python module", "s": "twisted", "link": "https://twisted.org/"},
            {
                "type": "python module",
                "s": "django-ninja",
                "link": "https://django-ninja.rest-framework.com/",
            },
            {
                "type": "contributor",
                "s": "KitetsuK",
                "link": "https://github.com/KitetsuK/",
            },
            {
                "type": "contributor",
                "s": "Saverio976",
                "link": "https://github.com/Saverio976/",
            },
        ]
    }

@api.get("/quit", auth=AuthBearer(django_secret=True))
def quit(request):
    header = {"Authorization": f"Bearer {request.auth}"}
    res = requests.get(request.build_absolute_uri("/api/songs/stop"), headers=header)
    print(res.text)
    return {"status": "ok"}
