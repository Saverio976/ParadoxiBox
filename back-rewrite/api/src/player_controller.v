import vweb

// TODO: queue
['/api/songs/queue'; get]
pub fn (mut app App) page_songs_queue() vweb.Result {
	return app.ok('true')
}

// TODO: queue current
['/api/songs/queue/current'; get]
pub fn (mut app App) page_songs_queue_current() vweb.Result {
	return app.ok('true')
}

// TODO: next
['/api/songs/queue/next'; get]
pub fn (mut app App) page_songs_queue_next() vweb.Result {
	return app.ok('true')
}

['/api/songs/queue/current/pos/set'; get]
pub fn (mut app App) page_songs_queue_current_pos_set() vweb.Result {
	if 'pos' !in app.query {
		return app.not_found()
	}
	id := app.player_conn.send_command('set_pos', app.query['pos'])
	resp := app.player_conn.get_response(id) or {
		app.error(err.msg())
		return app.server_error(500)
	}
	if resp.value == 'KO' {
		app.error('/api/songs/queue/current/pos/set + ${app.query['id']} = KO')
		return app.server_error(500)
	}
	return app.ok('true')
}

['/api/songs/queue/current/pos'; get]
pub fn (mut app App) page_songs_queue_current_pos_next() vweb.Result {
	id := app.player_conn.send_command('get_pos', '')
	resp := app.player_conn.get_response(id) or {
		app.error(err.msg())
		return app.server_error(500)
	}
	if resp.value == 'KO' {
		app.error('/api/songs/queue/current/pos = KO')
		return app.server_error(500)
	}
	return app.ok(resp.value)
}

['/api/songs/queue/add/song/url'; get]
pub fn (mut app App) page_songs_queue_add_song_url() vweb.Result {
	if 'url' !in app.query {
		return app.not_found()
	}
	go download_song_url(app.query['url'], app.player_conn)
	return app.ok('processing')
}

['/api/songs/queue/add/song/query'; get]
pub fn (mut app App) page_songs_queue_add_song_query() vweb.Result {
	if 'query' !in app.query {
		return app.not_found()
	}
	go download_song_query(app.query['query'], app.player_conn)
	return app.ok('processing')
}

['/api/songs/queue/add/playlist/url'; get]
pub fn (mut app App) page_songs_queue_add_playlist_url() vweb.Result {
	if 'url' !in app.query {
		return app.not_found()
	}
	go download_playlist_url(app.query['url'], app.player_conn)
	return app.ok('processing')
}

['/api/songs/pause'; get]
pub fn (mut app App) page_songs_pause() vweb.Result {
	id := app.player_conn.send_command('pause', '')
	resp := app.player_conn.get_response(id) or {
		app.error(err.msg())
		return app.server_error(500)
	}
	if resp.value == 'KO' {
		app.error('/api/songs/pause = KO')
		return app.server_error(500)
	}
	return app.ok('true')
}

['/api/songs/resume'; get]
pub fn (mut app App) page_songs_resume() vweb.Result {
	id := app.player_conn.send_command('resume', '')
	resp := app.player_conn.get_response(id) or {
		app.error(err.msg())
		return app.server_error(500)
	}
	if resp.value == 'KO' {
		app.error('/api/songs/pause = KO')
		return app.server_error(500)
	}
	return app.ok('true')
}

['/api/songs/is-paused'; get]
pub fn (mut app App) page_songs_is_paused() vweb.Result {
	id := app.player_conn.send_command('get_pause', '')
	resp := app.player_conn.get_response(id) or {
		app.error(err.msg())
		return app.server_error(500)
	}
	if resp.value == 'KO' {
		app.error('/api/songs/pause = KO')
		return app.server_error(500)
	}
	return app.ok(resp.value)
}

['/api/songs/stop'; get]
pub fn (mut app App) page_songs_stop() vweb.Result {
	id := app.player_conn.send_command('stop', '')
	resp := app.player_conn.get_response(id) or {
		app.error(err.msg())
		return app.server_error(500)
	}
	if resp.value == 'KO' {
		app.error('/api/songs/pause = KO')
		return app.server_error(500)
	}
	return app.ok('true')
}

// TODO: improvise now
['/api/songs/improvise/now'; get]
pub fn (mut app App) page_songs_improvise_now() vweb.Result {
	return app.ok('true')
}

// TODO: improvise auto toggle
['/api/songs/improvise/auto/toggle'; get]
pub fn (mut app App) page_songs_improvise_auto_toggle() vweb.Result {
	return app.ok('true')
}

// TODO: improvise auto get
['/api/songs/improvise/auto'; get]
pub fn (mut app App) page_songs_improvise_auto() vweb.Result {
	return app.ok('true')
}

['/api/songs/volume/set'; get]
pub fn (mut app App) page_songs_volume_set() vweb.Result {
	if 'vol' !in app.query {
		return app.not_found()
	}
	id := app.player_conn.send_command('set_volume', app.query['vol'])
	resp := app.player_conn.get_response(id) or {
		app.error(err.msg())
		return app.server_error(500)
	}
	if resp.value == 'KO' {
		app.error('/api/songs/volume/set + ${app.query['vol']} = KO')
		return app.server_error(500)
	}
	return app.ok('true')
}

['/api/songs/volume'; get]
pub fn (mut app App) page_songs_queue_current_pos_next() vweb.Result {
	id := app.player_conn.send_command('get_pos', '')
	resp := app.player_conn.get_response(id) or {
		app.error(err.msg())
		return app.server_error(500)
	}
	if resp.value == 'KO' {
		app.error('/api/songs/queue/current/pos = KO')
		return app.server_error(500)
	}
	return app.ok(resp.value)
}
