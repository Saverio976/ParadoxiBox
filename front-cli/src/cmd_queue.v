module main

import cli
import time

fn cmd_queue(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	songs := api_queue(api_url, bearer)!

	mut i := 1
	for song in songs {
		println('---[${i}/${songs.len}]--> ${song.title}')
		println('artist: ${song.artist}')
		println('url: ${song.source_link}')
		duration := time.Duration(isize(song.duration_second) * time.second)
		if i == 1 {
			pos_cur := api_get_pos(api_url, bearer)!
			println('${time.Duration(pos_cur * time.second)}/${duration}')
		} else {
			println(duration.debug())
		}
		i++
	}
}

const command_queue_conf = cli.Command{
	name: 'queue'
	description: 'Show music in the queue'
	execute: cmd_queue
}
