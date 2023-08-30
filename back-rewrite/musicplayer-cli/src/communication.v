import os.filelock
import os
import time

fn communicate_read(lockfile string, file string) string {
	mut lockk := filelock.new(lockfile)
	lockk.acquire() or {
		lockk.release()
		return ''
	}
	s := os.read_file(file) or { '' }
	lockk.release()
	return s
}

fn communicate_write(lockfile string, file string, data string) {
	mut lockk := filelock.new(lockfile)
	lockk.acquire() or { return }
	os.write_file(file, data) or {
		lockk.release()
		return
	}
	lockk.release()
}

fn communicate_clear(lockfile string, file string) {
	communicate_write(lockfile, file, '')
}

struct Command {
	title string [required]
	value string [required]
}

fn (cm Command) nice_str() string {
	if cm.value == '' {
		return cm.title
	}
	return cm.title + ':' + cm.value
}

fn split_data(data string) (string, string) {
	rstring, lstring := data.split_once(':') or { data, '' }
	return rstring, lstring
}

fn musicplayer_bus(command Command, lockfile string, file string) Command {
	s := command.nice_str()
	communicate_write(lockfile, file, s)
	mut data := s
	for s == data {
		time.sleep(time.microsecond)
		data = communicate_read(lockfile, file)
	}
	rsplit, lsplit := split_data(data)
	return Command{
		title: rsplit
		value: lsplit
	}
}
