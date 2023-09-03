import player_service
import arrays

import json
import os

pub struct SongP {
	path string
	title string
	artists string
	source_url string
	duration int
	thumbnail_url string
}

pub struct ScriptDownloadRes {
	songs []SongP
}

fn exec_python(python_script string, params []string) !string {
	cmd := 'python3 \'' + python_script + '\' ' + arrays.join_to_string[string](params, ' ', fn (s string) string { return "'" + s + "'" })
	eprintln(cmd)
	res := os.execute(cmd)
	if res.exit_code != 0 {
		return error('invalid return code ${res.exit_code}')
	}
	return res.output
}

fn download_url(url string, no_playlist bool) []SongP {
	home := os.abs_path(os.join_path_single(os.dir(os.executable()), 'songs'))
	mut args := ['--format', 'm4a', '--home', home, url]
	if no_playlist {
		args << '--noplaylist'
	}
	output := exec_python('scripts/download_url.py', args ) or {
		eprintln(err.msg() + '::Error downloading')
		return []SongP{}
	}
	eprintln('!!! output: ${output} !!!')
	songs := json.decode(ScriptDownloadRes, output) or {
		eprintln('${err.msg()} ::Error decoding json:: ${output}')
		eprintln("Im here")
		return []SongP{}
	}
	eprintln('!!! download_url:: songs len: ${songs.songs.len} !!!')
	return songs.songs
}

fn search_song(query string) ?string {
	args := [query]
	output := exec_python('scripts/search_song.py', args) or { '' }
	if output == '' {
		return none
	}
	return output
}

fn download_song_url(url string, player_conn player_service.Connection) int {
	songs := download_url(url, true)
	if songs.len != 1 {
		eprintln('download_url:: songs len: ${songs.len}')
		return 1
	}
	resp := player_conn.send_command('play', songs[0].path) or {
		eprintln(err.msg() + 'error playing')
		return 1
	}
	if resp.value == 'KO' {
		eprintln('download_song_url + ${url} = KO')
		return 1
	}
	return 0
}

fn download_song_query(query string, player_conn player_service.Connection) int {
	if url := search_song(query) {
		return download_song_url(url, player_conn)
	}
	return 1
}

fn download_playlist_url(url string, player_conn player_service.Connection) int {
	songs := download_url(url, true)
	mut is_error := false
	for song in songs {
		resp := player_conn.send_command('play', song.path) or {
			eprintln(err.msg() + 'Error playing')
			is_error = true
			return 1
		}
		if resp.value == 'KO' {
			eprintln('download_song_url + ${url} + ${song.path} = KO')
			is_error = true
			return 1
		}
	}
	return if is_error { 1 } else { 0 }
}

fn get_queue(data string) []Song {
	mut db := database_connect() or {
		return []Song{}
	}
	defer {
		db.close()
	}
	mut songs := []Song{}
	for line in data.split('\n') {
		song := db.get_song(line) or { new_unknow_song() }
		songs << song
	}
	return songs
}
