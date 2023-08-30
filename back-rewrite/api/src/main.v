import vweb

struct App {
	vweb.Context
}

fn main() {
	mut app := new_app()
	{
		mut db := database_connect() or { panic(err) }
		database_init(db)
		db.close()
	}
	vweb.run_at(app, vweb.RunParams{
		port: 8080
	}) or { panic(err) }
}

fn new_app() &App {
	mut app := &App{}
	return app
}
