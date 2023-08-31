import db.sqlite
import crypto.sha512
import crypto.rand

struct DataBase {
mut:
	db sqlite.DB
}

struct User {
	username string [primary; unique]
	password string [nonull]
	bearer string
}

struct Song {
	path string [primary; unique]
	title string [nonull]
	artists string
	duration int [nonull]
	thumbnail_url string
	source_url string
}

fn database_connect() !DataBase {
	db := sqlite.connect('db.sqlite')!
	return DataBase{db: db}
}

fn database_init(db DataBase) {
	sql db.db {
		create table User
	} or { panic(err) }
	sql db.db {
		create table Song
	} or { panic(err) }
}

fn (mut db DataBase) user_create(username string, password string) ! {
	pass := hash_data(password)
	user := User{
		username: username
		password: pass
		bearer: ''
	}
	sql db.db {
		insert user into User
	}!
}

fn (mut db DataBase) user_login(username string, password string) !string {
	pass := hash_data(password)
	users := sql db.db {
		select from User where username == username && password == pass
	}!
	if users.len != 1 {
		return error('found ${users.len} entry for username')
	}
	if users[0].bearer != '' {
		return users[0].bearer
	}
	bearer := rand.bytes(25)!.hex()
	sql db.db {
		update User set bearer = bearer where username == username && password == pass
	}!
	return bearer
}

fn (mut db DataBase) user_check_login(bearer string) ! {
	if bearer == "" {
		return error('bearer empty')
	}
	users := sql db.db {
		select from User where bearer == bearer
	}!
	if users.len != 1 {
		return error('found ${users.len} entry for bearer')
	}
}

fn (mut db DataBase) user_logout(bearer string) ! {
	if bearer == "" {
		return error('bearer empty')
	}
	sql db.db {
		update User set bearer = '' where bearer == bearer
	}!
}

fn (mut db DataBase) user_delete(bearer string) ! {
	if bearer == "" {
		return error('bearer empty')
	}
	db.user_check_login(bearer)!
	sql db.db {
		delete from User where bearer == bearer
	}!
}

fn (mut db DataBase) close() {
	db.db.close() or { return }
}

fn hash_data(data string) string {
	hash := sha512.hexhash(data)
	return hash
}

fn (mut db DataBase) get_song(path string) !Song {
	songs := sql db.db {
		select from Song where path == path limit 1
	}!
	if songs.len != 1 {
		return error('song ${path} found ${songs.len} entries')
	}
	return songs[0]
}

fn new_unknow_song() Song {
	return Song{
		path: 'UNKNOW'
		title: 'UNKNOW'
		artists: 'UNKNOW'
		duration: 42
		thumbnail_url: 'UNKNOW'
		source_url: 'UNKNOW'
	}
}

fn (mut db DataBase) bulk_create_song(songs []Song) ! {
	for song in songs {
		sql db.db {
			insert song into Song
		}!
	}
}
