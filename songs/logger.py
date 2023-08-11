LOG_FILE = ".song.log"

def logger_print(*args, **kwargs):
    with open(LOG_FILE) as f:
        print(*args, **kwargs, file=f)
