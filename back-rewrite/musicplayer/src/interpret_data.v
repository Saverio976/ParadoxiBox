module main

import strconv

fn split_data(data string) (string, string) {
	rstring, lstring := data.split_once(':') or { data, '' }
	return rstring, lstring
}

fn interpret_data(data string, mut player Player) string {
	title, value := split_data(data)
	match title {
		'has_song' {
			return title + ':' + player.has_song().str()
		}
		'play' {
			player.play_sound(value) or { return title + ':KO' }
		}
		'get_pause' {
			return title + ':' + player.is_paused().str()
		}
		'pause' {
			player.pause()
		}
		'resume' {
			player.resume()
		}
		'stop' {
			player.stop()
			return title + 'ed:OK'
		}
		'get_volume' {
			return title + ':' + player.get_volume().str()
		}
		'set_volume' {
			volume := strconv.atoi(value) or { return title + ':KO' }
			player.set_volume(volume)
		}
		'get_pos' {
			return title + ':' + player.get_pos().str()
		}
		'set_pos' {
			pos := strconv.atoi(value) or { return title + ':KO' }
			player.set_pos(pos)
		}
		else {
			return title + ':KO'
		}
	}
	return title + ':OK'
}
