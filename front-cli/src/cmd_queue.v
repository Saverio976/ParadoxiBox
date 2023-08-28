module main

import cli
import time

fn cmd_queue(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := cmd.flags.get_string('url-api')!
	songs := api_queue(api_url, bearer)!

	println('${songs.len} Songs queued...')
	for song in songs {
		println('-----> ${song.title}')
		println('artist: ${song.artist}')
		println('url: ${song.source_link}')
		duration := time.Duration(isize(song.duration_second) * time.second).debug()
		println(duration)
	}
}

const command_queue_conf = cli.Command{
	name: 'queue'
	description: 'Show music in the queue'
	execute: cmd_queue
}
