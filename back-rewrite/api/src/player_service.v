import player_service
import download

fn download_song_url(url string, player_conn player_service.Connection) int {
	path := download.download_song_url(url) or {
		eprintln(err.msg())
		return 1
	}
	id := player_conn.send_command('play', path)
	resp := player_conn.get_response(id) or {
		eprintln(err.msg())
		return 1
	}
	if resp.value == 'KO' {
		eprintln('download_song_url + ${url} = KO')
		return 1
	}
	return 0
}

fn download_song_query(query string, player_conn player_service.Connection) int {
	path := download.download_song_query(query) or {
		eprintln(err.msg())
		return 1
	}
	id := player_conn.send_command('play', path)
	resp := player_conn.get_response(id) or {
		eprintln(err.msg())
		return 1
	}
	if resp.value == 'KO' {
		eprintln('download_song_query + ${query} = KO')
		return 1
	}
	return 0
}

fn download_playlist_url(url string, player_conn player_service.Connection) int {
	paths := download.download_playlist_url(url) or {
		eprintln(err.msg())
		return 1
	}
	mut is_error := false
	for path in paths {
		id := player_conn.send_command('play', path)
		resp := player_conn.get_response(id) or {
			eprintln(err.msg())
			is_error = true
			continue
		}
		if resp.value == 'KO' {
			eprintln('download_song_url + ${url} = KO')
			is_error = true
			continue
		}
	}
	return if is_error { 1 } else { 0 }
}
