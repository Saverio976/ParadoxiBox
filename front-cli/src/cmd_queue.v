module main

import cli
import x.json2

fn cmd_queue(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := cmd.flags.get_string('url-api')!
	songs := api_queue(api_url, bearer)!

	println('${songs.len} Songs queued...')
	for song in songs {
		println(json2.encode_pretty[SongQueued](song))
	}
}

const command_queue_conf = cli.Command{
	name: 'queue'
	description: 'Show music in the queue'
	execute: cmd_queue
}
