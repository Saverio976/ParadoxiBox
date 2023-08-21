FROM python:3.11-slim

RUN apt-get update                  \
    && apt-get install              \
        --no-install-recommends     \
        -y                          \
        curl                        \
        libsdl2-dev                 \
        libsdl2-image-dev           \
        libsdl2-mixer-dev           \
        libsdl2-ttf-dev             \
        libfreetype6-dev            \
        libportmidi-dev             \
        libjpeg-dev                 \
        ffmpeg                      \
        make                        \
        gcc                         \
        g++                         \
        python3-setuptools          \
        python3-dev                 \
        python3-numpy               \
        python3-pygame              \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY Makefile /app/Makefile

RUN make pip-install

COPY manage.py /app/manage.py
COPY ParadoxiBox /app/ParadoxiBox
COPY songs /app/songs
copy uuser /app/uuser

RUN make migrate

ENTRYPOINT ["make", "runserver-prod"]
