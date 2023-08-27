FROM debian:12-slim

RUN apt-get update                  \
    && apt-get install              \
        --no-install-recommends     \
        -y                          \
        gcc                         \
        make                        \
        git                         \
        curl                        \
        libssl-dev                  \
        ca-certificates             \
        build-essential             \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/vlang/v /opt/v \
    && cd /opt/v \
    && make \
    && ./v symlink

WORKDIR /app
COPY . /app

RUN make paradoxibox-cli-prod-linux

ENTRYPOINT ["/app/paradoxibox-cli"]
