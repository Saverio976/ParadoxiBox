import vweb

import os
import flag

struct App {
	vweb.Context
	lockfile string
	filecom string
}

fn main() {
	mut fp := flag.new_flag_parser(os.args)
	fp.application('api')
	fp.version('v0.0.1')
	fp.limit_free_args(0, 0) or {
		eprintln(err)
		println(fp.usage())
		return
	}
	fp.description('Web API for the Music Player for ParadoxiBox')
	fp.skip_executable()
	file_lock := fp.string_opt('file-lock', `l`, 'lock file to acquire before writing/reading') or {
		eprintln(err)
		println(fp.usage())
		return
	}
	file := fp.string_opt('file', `f`, 'file in which the communication will be') or {
		eprintln(err)
		println(fp.usage())
		return
	}
	_ := fp.finalize() or {
		eprintln(err)
		println(fp.usage())
		return
	}
	communicate_clear(file_lock, file)
	mut app := new_app(file_lock, file)
	{
		mut db := database_connect() or { panic(err) }
		database_init(db)
		db.close()
	}
	vweb.run_at(app, vweb.RunParams{
		port: 8080
	}) or { panic(err) }
}

fn new_app(file_lock string, file string) &App {
	mut app := &App{lockfile: file_lock, filecom: file}
	return app
}
