# ParadoxiBox

A Music Player on a Server with web controller

- Tested on a Raspberry Pi 3B+ (need to install rust [rust install](https://www.rust-lang.org/tools/install) for one python dependcy)

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

## USAGE (manual)

1. Create Virtualenv + Install dependencies

:warning: Change the PYTHON argument to your latest python :warning:

```bash
make install PYTHON=python
```

2. Run the server

*feel free to modify the arguments values*

```bash
make runserver-prod                                         \
    HOST='0.0.0.0'                                          \
    PORT='8000'                                             \
    ALLOWED_HOST='*'                                        \
    LANGUAGE_CODE='en-us'                                   \
    TIME_ZONE='Europe/Paris'                                \
    SECRET_KEY='django-secret-key-wow-so-random0123456789'
```

## USAGE (service)

`./paradoxibox.service` is provided if you want to launch it as a service

1. Setup the file

this action need rott privilige (it copy the file to `/etc/systemd/user/paradoxibox.service`

:warning: modify the value you want :warning:

```bash
sudo make service-setup                                     \
    PYTHON=python                                           \
    HOST='0.0.0.0'                                          \
    PORT='8000'                                             \
    ALLOWED_HOST='*'                                        \
    LANGUAGE_CODE='en-us'                                   \
    TIME_ZONE='Europe/Paris'                                \
    SECRET_KEY='django-secret-key-wow-so-random0123456789'
```

2. enable the service as user

(don't need any privilege)

```bash
make service-enable
# under the hood, it is just a `systemctl --user enable --now paradoxibox.service`
```

## USAGE (docker)

:warning: modify the value you want :warning:

```bash
HOST=0.0.0.0
PORT=8000
ALLOWED_HOST='*'
LANGUAGE_CODE='en-us'
TIME_ZONE='Europe/Paris'
SECRET_KEY='django-secret-key-wow-so-random0123456789'
docker run                                              \
    -it                                                 \
    -p $PORT:$PORT                                      \
    ghcr.io/saverio976/paradoxibox:main                 \
    HOST=$HOST                                          \
    PORT=$PORT                                          \
    ALLOWED_HOST=$ALLOWED_HOST                          \
    LANGUAGE_CODE=$LANGUAGE_CODE                        \
    TIME_ZONE=$TIME_ZONE                                \
    SECRET_KEY=$SECRET_KEY
```
