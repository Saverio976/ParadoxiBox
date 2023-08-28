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
		duration := time.Duration(isize(song.duration_second) * time.second).debug()
		println(duration)
		i++
	}
}

const command_queue_conf = cli.Command{
	name: 'queue'
	description: 'Show music in the queue'
	execute: cmd_queue
}
