module player_service

import time

import os.filelock

import os

pub struct Connection {
	lockfile string
	file string
	lock_internal string
}

fn (cn Connection) bus_connection(cm Command) !Response {
	mut data := ''
	mut @lock := filelock.new(cn.lock_internal)
	if !@lock.wait_acquire(5) {
		return error('lock failed')
	}
	eprintln('this -1')
	s := cm.str()
	communicate_write(cn.lockfile, cn.file, s)
	data = s
	eprintln('this 0')
	for data == s {
		time.sleep(time.microsecond)
		data = communicate_read(cn.lockfile, cn.file)
		eprintln('this 1')
	}
	@lock.release()
	eprintln('this 2')
	rsplit, lsplit := split_data(data)
	eprintln('this 3')
	res := Response{
		title: rsplit
		value: lsplit
	}
	return res
}

pub fn start_connection(lockfile string, file string) !Connection {
	communicate_clear(lockfile, file)
	return Connection{
		lockfile: lockfile
		file: file
		lock_internal: os.join_path(os.cache_dir(), 'internal_lock.txt')
	}
}

pub fn (cn Connection) send_command(title string, value string) !Response {
	cm := new_command(title, value)
	res := cn.bus_connection(cm)!
	eprintln('Command sended: ${cm.str()}')
	return res
}

// pub fn (cn Connection) get_response(id int) !Response {
// 	mut found := false
// 	eprintln('id waiting: ${id}')
// 	for !found {
// 		time.sleep(time.microsecond)
// 		rlock cn.responses {
// 			found = id in cn.responses
// 		}
// 	}
// 	eprintln('id found: ${id}')
// 	mut rs := Response{}
// 	lock cn.responses {
// 		eprintln('id found (in lock): ${id}')
// 		rs = cn.responses[id] or { return error('id ${id} not found') }
// 		cn.responses.delete(id)
// 	}
// 	return rs
// }
