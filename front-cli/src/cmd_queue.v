module main

import cli
import time
import term

fn cmd_queue(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	songs := api_queue(api_url, bearer)!

	mut i := 1
	for song in songs {
		println(term.bold(term.green('---[${i}/${songs.len}]-->')))
		title := term.underline('title') + ': ' + term.bold(song.title)
		println(title)
		artist := term.underline('artist') + ': ' + song.artist
		println(artist)
		url := term.underline('url') + ': ' + song.source_link
		println(url)
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
