from typing import Any

LOG_FILE = ".song.log"


def logger_print(*args: Any, **kwargs: Any) -> None:
    with open(LOG_FILE, mode="a") as f:
        print(*args, **kwargs, file=f)
