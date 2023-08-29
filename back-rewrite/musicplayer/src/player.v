import miniaudio as ma

struct Player {
mut:
	engine &ma.Engine
	sound ?&ma.Sound
	volume int = 50
	is_paused bool
pub:
	lockfile string
	file string
}

fn init_player(lockfile string, file string) !&Player {
	mut player := &Player{
		engine: &ma.Engine{}
		lockfile: lockfile
		file: file
	}
	result := ma.engine_init(ma.null, player.engine)
	if result != .success {
		return error('Failed to init miniaudio engine')
	}
	player.set_volume(player.volume)
	return player
}

fn uninit_player(mut player Player) {
	ma.engine_uninit(player.engine)
}

fn (mut player Player) stop() {
	if mut sound := player.sound {
		ma.sound_stop(sound)
		ma.sound_uninit(sound)
		player.sound = none
	}
}

fn (mut player Player) play_sound(file string) ! {
	player.stop()
	mut sound := &ma.Sound{}
	result := ma.sound_init_from_file(player.engine, file.str, 0, ma.null, ma.null, sound)
	if result != .success {
		return error('Failed to init miniaudio sound')
	}
	if !player.is_paused() {
		ma.sound_start(sound)
	}
	player.sound = sound
}

fn (mut player Player) pause() {
	if mut sound := player.sound {
		ma.sound_stop(sound)
		player.is_paused = true
	}
}

fn (mut player Player) resume() {
	if mut sound := player.sound {
		ma.sound_start(sound)
		player.is_paused = false
	}
}

fn (mut player Player) set_pos(position int) {
	pos := if position > 0 { position } else { 0 }
	if !player.has_song() {
		return
	}
	if mut sound := player.sound {
		ma.sound_stop(sound)
		mut sample_rate := u32(0)
		ma.sound_seek_to_pcm_frame(sound, 0)
		result := ma.sound_get_data_format(sound, ma.null, ma.null, sample_rate, ma.null, ma.null)
		if result != .success {
			return
		}
		println('sample rate: ${sample_rate}')
		ma.sound_seek_to_pcm_frame(sound, sample_rate * u32(pos))
		ma.sound_start(sound)
	}
}

fn (mut player Player) get_pos() int {
	if !player.has_song() {
		return 0
	}
	if mut sound := player.sound {
		mut cursor := f32(0)
		result := ma.sound_get_cursor_in_seconds(sound, cursor)
		if result != .success {
			return 0
		}
		return int(cursor)
	}
	return 0
}

// between 0 and ... (0 = mute, 100 = normal sound, more than 100 = amplification)
fn (mut player Player) set_volume(volume int) {
	vol := if volume > 0 { volume } else { 0 }
	if mut sound := player.sound {
		ma.sound_set_volume(sound, f32(vol) / 100.0)
		player.volume = volume
	}
}

// between 0 and 100
fn (player Player) get_volume() int {
	return player.volume
}

fn (mut player Player) has_song() bool {
	if sound := player.sound {
		if ma.sound_at_end(sound) != 0 {
			player.stop()
			return false
		}
		return true
	}
	return false
}

fn (mut player Player) is_paused() bool {
	if !player.has_song() {
		return false
	}
	return player.is_paused
}
