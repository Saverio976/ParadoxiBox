import os.filelock
import os

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
