import vweb

['/api/songs/queue'; get]
pub fn (mut app App) page_songs_queue() vweb.Result {
	app.error('test 1')
	resp := app.player_conn.send_command('queue', '') or {
		app.error(err.msg())
		return app.server_error(500)
	}
	if resp.value == 'KO' {
		app.error('/api/songs/queue = KO')
		return app.server_error(500)
	}
	return app.ok('true')
}

['/api/songs/queue/next'; get]
pub fn (mut app App) page_songs_queue_next() vweb.Result {
	resp := app.player_conn.send_command('next', '') or {
		app.error(err.msg())
		return app.server_error(500)
	}
	if resp.value == 'KO' {
		app.error('/api/songs/queue/next = KO')
		return app.server_error(500)
	}
	return app.ok('true')
}

['/api/songs/queue/current/pos/set'; get]
pub fn (mut app App) page_songs_queue_current_pos_set() vweb.Result {
	if 'pos' !in app.query {
		return app.not_found()
	}
	resp := app.player_conn.send_command('set_pos', app.query['pos']) or {
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
	resp := app.player_conn.send_command('get_pos', '') or {
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
	download_song_query(app.query['query'], app.player_conn)
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
	resp := app.player_conn.send_command('pause', '') or {
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
	resp := app.player_conn.send_command('resume', '') or {
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
	resp := app.player_conn.send_command('get_pause', '') or {
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
	resp := app.player_conn.send_command('stop', '') or {
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
	resp := app.player_conn.send_command('set_volume', app.query['vol']) or {
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
pub fn (mut app App) page_songs_volume() vweb.Result {
	resp := app.player_conn.send_command('get_pos', '') or {
		app.error(err.msg())
		return app.server_error(500)
	}
	if resp.value == 'KO' {
		app.error('/api/songs/queue/current/pos = KO')
		return app.server_error(500)
	}
	return app.ok(resp.value)
}
