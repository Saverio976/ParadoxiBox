# ParadoxiBox

Work In Progress

Available now:
- Show downloaded musics
- Download new music (download first result of {artist} {title} in youtube)
- Play one music in the server
- Play a queue in the server
- Pause/Resume the music
- Skip a song

TODO:
- Better way to add song to the queue (throuht a search autocomplete for already downloaded songs and download it otherwise) [i.e.: not 2 distinct pages]

## USAGE

```bash
make install
# feel free to modify this values
make runserver-prod                                         \
    HOST=127.0.0.1                                          \
    PORT=8000                                               \
    ALLOWED_HOST='*'                                        \
    LANGUAGE_CODE=en-us                                     \
    TIME_ZONE=Europe/Paris                                  \
    SECRET_KEY=django-secret-key-wow-so-random0123456789
```
