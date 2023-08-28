module main

import cli

fn cmd_add_song(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	mut songs := AddSong{}

	if cmd.flags.get_all_found().get_string('song-url') or { '' } != '' {
		songs.url_song = cmd.flags.get_all_found().get_string('song-url')!
	}
	if cmd.flags.get_all_found().get_string('song-pattern') or { '' } != '' {
		songs.search_song = cmd.flags.get_all_found().get_string('song-pattern')!
	}
	if cmd.flags.get_all_found().get_string('playlist-url') or { '' } != '' {
		songs.url_playlist = cmd.flags.get_all_found().get_string('playlist-url')!
	}

	api_add_song(api_url, bearer, songs)!
}

const command_add_song_conf = cli.Command{
	name: 'add'
	description: 'Add a song to the queue'
	execute: cmd_add_song
	flags: [
		cli.Flag{
			flag: cli.FlagType.string
			name: 'song-url'
			abbrev: 'su'
			description: 'Song url to add (anything https://github.com/yt-dlp/yt-dlp can support)'
		},
		cli.Flag{
			flag: cli.FlagType.string
			name: 'song-pattern'
			abbrev: 'sp'
			description: 'Song pattern to search and add'
		},
		cli.Flag{
			flag: cli.FlagType.string
			name: 'playlist-url'
			abbrev: 'pu'
			description: 'Playlist url to add (anything https://github.com/yt-dlp/yt-dlp can support)'
		},
	]
}
