# ParadoxiBox

Work In Progress

Available now:
- Show downloaded musics
- Download new music (thanks to [yt-dlp](https://github.com/yt-dlp/yt-dlp))
- Play one music in the server
- Play a queue in the server
- Pause/Resume the music
- Skip a song
- Automatically play a new song if option turned on (thanks to [ytmusicapi](https://ytmusicapi.readthedocs.io))

TODO:
- Better way to add song to the queue (throuht a search autocomplete for already downloaded songs and download it otherwise) [i.e.: not 2 distinct pages]

## USAGE

1. Create Virtualenv + Install dependencies

:warning: Change the PYTHON argument to your latest python :warning:

```bash
make install PYTHON=python
```

2. Run the server

*feel free to modify the arguments values*

```
make runserver-prod                                         \
    HOST='0.0.0.0'                                          \
    PORT='8000'                                             \
    ALLOWED_HOST='*'                                        \
    LANGUAGE_CODE='en-us'                                   \
    TIME_ZONE='Europe/Paris'                                \
    SECRET_KEY='django-secret-key-wow-so-random0123456789'
```
