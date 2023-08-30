# protocol

- All messages are passed via a file

## Commands and Response

### Has Song

- Command: `has_song`
- Response: `has_song:true` | `has_song:false`

### Play

- Command: `play:<absolute file path>` (ex: `play:/home/gerard/Music/Despacito.mp3`)
- Response: `play:OK` | `play:KO`

### Get Pause

- Command: `get_pause`
- Response: `get_pause:true` | `get_pause:false`

### Pause

- Command: `pause`
- Response: `pause:OK`

### Resume

- Command: `resume`
- Response: `resume:OK`

### Stop

- Command: `stop`
- Response: `stop:OK`

### Get Volume

- Command: `get_volume`
- Response: `get_volume:<volume int between 0 and ...>` (ex: `get_volume:20`)

- Volume 0 mean no sound
- Volume 100 mean normal sound volume
- More than 100 is amplification

### Set Volume

- Command `set_volume:<volume int between 0 and ...`
- Response `set_volume:OK` | `set_volume:KO`

### Get Possition

- Command: `get_pos`
- Response: `get_pos:<position int seconds between 0 and ...`

- Position 0 mean no song being played or song just started
- Position is in second

### Get Position Max

- Command: `get_pos_max`
- Response: `get_pos_max:<position int seconds`

- Position 0 mean no song or song has length 0 second
- Position is in second

### Set Position

- Command `set_pos:<position int seconds between 0 and ...`
- Response: `set_pos:OK` | `set_pos:KO`

- Position 0 mean no song being played or song just started
- Position is in second
