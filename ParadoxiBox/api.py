from ninja import NinjaAPI
from songs.api import router as router_songs
from uuser.api import router as router_uuser

api = NinjaAPI(title="ParadoxiBox")
api.add_router("/songs/", router_songs)
api.add_router("/auth/", router_uuser)
