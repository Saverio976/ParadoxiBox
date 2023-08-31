import vweb

['/api/auth/create'; get]
pub fn (mut app App) page_auth_create() vweb.Result {
	if !['username', 'password'].all(it in app.query) {
		return app.not_found()
	}
	mut db := database_connect() or {
		app.error(err.msg())
		return app.server_error(500)
	}

	defer {
		db.close()
	}

	db.user_create(app.query['username'], app.query['password']) or {
		app.error(err.msg())
		return app.server_error(500)
	}
	return app.ok('true')
}

['/api/auth/login'; get]
pub fn (mut app App) page_auth_login() vweb.Result {
	if !['username', 'password'].all(it in app.query) {
		return app.not_found()
	}
	mut db := database_connect() or {
		app.error(err.msg())
		return app.server_error(500)
	}

	defer {
		db.close()
	}

	bearer := db.user_login(app.query['username'], app.query['password']) or {
		app.error(err.msg())
		return app.server_error(500)
	}
	return app.ok(bearer)
}

['/api/auth/logout'; get]
pub fn (mut app App) page_auth_logout() vweb.Result {
	if 'bearer' !in app.query {
		return app.not_found()
	}
	mut db := database_connect() or {
		app.error(err.msg())
		return app.server_error(500)
	}

	defer {
		db.close()
	}

	db.user_logout(app.query['bearer']) or {
		app.error(err.msg())
		return app.server_error(504)
	}
	return app.ok('true')
}

['/api/auth/delete'; get]
pub fn (mut app App) page_auth_delete() vweb.Result {
	if 'bearer' !in app.query {
		return app.not_found()
	}
	mut db := database_connect() or {
		app.error(err.msg())
		return app.server_error(504)
	}

	defer {
		db.close()
	}

	db.user_delete(app.query['bearer']) or {
		app.error(err.msg())
		return app.server_error(504)
	}
	return app.ok('true')
}
