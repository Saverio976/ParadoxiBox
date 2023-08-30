import os
import flag

fn main() {
	mut fp := flag.new_flag_parser(os.args)
	fp.application('api')
	fp.version('v0.0.1')
	fp.limit_free_args(0, 0) or {
		eprintln(err)
		println(fp.usage())
		return
	}
	fp.description('CLI the Music Player for ParadoxiBox')
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
	title := fp.string_opt('command', `c`, 'command to send') or {
		eprintln(err)
		println(fp.usage())
		return
	}
	value := fp.string_opt('value', `v`, 'value with the command (optional)') or { '' }
	_ := fp.finalize() or {
		eprintln(err)
		println(fp.usage())
		return
	}
	cm := musicplayer_bus(Command{title: title, value: value}, file_lock, file)
	println(cm.nice_str())
}
