# ParadoxiBox CLI

## Usage

```txt
❯ paradoxibox-cli --help
Usage: paradoxibox-cli [flags] [commands] ./paradoxibox-cli

ParadoxiBox cli ( https://github.com/Saverio976/ParadoxiBox )

Flags:
  -u  --url-api       ParadoxiBox api url (i.e.: http://localhost:8080/api) (required)
  -h  --help          Prints help information.
      --man           Prints the auto-generated manpage.

Commands:
  queue               Show music in the queue
  login               Login to the api
  add                 Add a song to the queue
  help                Prints help information.
  man                 Prints the auto-generated manpage.
```

## Install

### From Docker/Podman

```bash
# CRI="podman" # uncomment this line if you want to use podman
# CRI="docker" # uncomment this line if you want to use docker

CRI run ghcr.io/saverio976/paradoxibox-front-cli:main --help
```

### From Source

```bash
# install vlang (https://github.com/vlang/v#installing-v-from-source)
make
./paradoxibox-cli --help
```
