FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg make && rm -rf /var/lib/apt/lists/*

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
