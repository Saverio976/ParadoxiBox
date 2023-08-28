# ParadoxiBox

A Music Player on a Server with web controller

- Backend Tested on a Raspberry Pi 3B+ (need to install rust [rustup install](https://www.rust-lang.org/tools/install) for one python dependcy)

!! Work In Progress !!

## FEATURES

- Web API for the backend (using [django](https://www.djangoproject.com/) and [django-ninja](https://django-ninja.rest-framework.com/))
- Terminal User Interface to communicate with the backend (made in [vlang](https://www.vlang.io))
- Automatically play a new song based on the last played song if option is turned on (thanks to [ytmusicapi](https://ytmusicapi.readthedocs.io))
- Support variety of music/video providers (thanks to [yt-dlp](https://github.com/yt-dlp/yt-dlp))

## USAGE

- back-end: read the [readme](./back/README.md)
- fontend-cli: read the [readme](./front-cli/README.md)
