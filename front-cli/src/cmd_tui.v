module main

import cli
import term
import term.ui as tui
import time

struct Queue {
mut:
	songs []SongQueued
	last_updated time.Time
	cursor_start int
}

struct Controller {
mut:
	pos_button_vol_plus tui.KeyCode
	pos_button_vol_less tui.KeyCode
	pos_button_pause tui.KeyCode
	pos_button_resume tui.KeyCode
	pos_button_next tui.KeyCode
	vol int
	last_updated time.Time
}

struct App {
	api_url string
	bearer string
mut:
	tui &tui.Context = unsafe { nil }
	width int
	height int
	queue Queue
	controller Controller
}

fn event(e &tui.Event, x voidptr) {
	mut app := unsafe { &App(x) }

	if e.typ == .key_down && e.code == .down {
		if app.queue.cursor_start + 1 < app.queue.songs.len {
			app.queue.cursor_start++
		}
	} else if e.typ == .key_down && e.code == .up {
		if app.queue.cursor_start - 1 >= 0 {
			app.queue.cursor_start--
		}
	} else if e.typ == .key_down {
		if e.code == app.controller.pos_button_next {
			api_next(app.api_url, app.bearer) or { return }
		} else if e.code == app.controller.pos_button_pause {
			api_pause(app.api_url, app.bearer) or { return }
		} else if e.code == app.controller.pos_button_resume {
			api_resume(app.api_url, app.bearer) or { return }
		} else if e.code == app.controller.pos_button_vol_plus {
			api_set_vol(app.api_url, app.bearer, app.controller.vol + 5) or { return }
		} else if e.code == app.controller.pos_button_vol_less {
			api_set_vol(app.api_url, app.bearer, app.controller.vol - 5) or { return }
		}
	}
}

fn draw_queue(mut app &App, x int, y int, x1 int, y1 int) {
	app.tui.draw_rect(x, y, x1, y1)

	if time.since(app.queue.last_updated).seconds() > 2 {
		app.queue.songs = api_queue(app.api_url, app.bearer) or { [] }
		app.queue.last_updated = time.now()
	}
	mut i := 1
	if app.queue.songs.len == 0 {
		app.tui.draw_text(x + 1, y + i, 'No Songs in Queue')
		i++
	}
	app.tui.draw_text(x + 1, i + y, 'showing from index ${app.queue.cursor_start}/${app.queue.songs.len - 1}...')
	i++
	for index_song in app.queue.cursor_start .. app.queue.songs.len {
		if i + y >= y1 {
			break
		}
		song := app.queue.songs[index_song]
		song_text_init := term.bold(song.title) + ' <=> ' + song.artist + ' <=> '
		mut song_text_duration := time.Duration(isize(song.duration_second) * time.second).str()
		if i == 1 {
			pos_cur := api_get_pos(app.api_url, app.bearer) or { 0 }
			song_text_duration = time.Duration(pos_cur * time.second).str() + '/' + song_text_duration
		}
		app.tui.draw_text(x + 1, i + y, song_text_init + song_text_duration)
		i++
	}
}

fn draw_controller(mut app &App, x int, y int, x1 int, y1 int) {
	app.tui.draw_rect(x, y, x1, y1)

	if time.since(app.controller.last_updated).seconds() > 2 {
		app.controller.vol = api_get_vol(app.api_url, app.bearer) or { 0 }
		app.controller.last_updated = time.now()
	}
	mut i := 1
	mut start_x := 1
	pause := 'PAUSE (P)'
	app.tui.draw_text(x + start_x, i + y, term.underline(pause))
	app.controller.pos_button_pause = .p
	start_x += pause.len + 5
	resume := 'RESUME (R)'
	app.tui.draw_text(x + start_x, i + y, term.underline(resume))
	app.controller.pos_button_resume = .r
	start_x += resume.len + 5
	next := 'NEXT (N)'
	app.tui.draw_text(x + start_x, i + y, term.underline(next))
	app.controller.pos_button_next = .n
	i++

	start_x = 1
	vol_less := '-- (-)'
	app.tui.draw_text(x + start_x, i + y, term.underline(vol_less))
	app.controller.pos_button_vol_less = .minus
	start_x += vol_less.len + 5
	vol := ' volume=${app.controller.vol}'
	app.tui.draw_text(x + start_x, i + y, vol)
	start_x += vol.len + 5
	vol_plus := '++ (+)'
	app.tui.draw_text(x + start_x, i + y, term.underline(vol_plus))
	app.controller.pos_button_vol_plus = .plus
}


fn frame(x voidptr) {
	mut app := unsafe { &App(x) }

	app.tui.clear()
	draw_queue(mut app, 1, 1, app.width - 1, (app.height / 2) - 1)
	draw_controller(mut app, 1, (app.height / 2) + 1, app.width - 1, app.height)
	app.tui.horizontal_separator(app.height / 2)
	app.tui.set_cursor_position(app.width, app.height)

	app.tui.reset()
	app.tui.flush()
}

fn cleanup(x voidptr) {
	mut app := unsafe { &App(x) }

	app.tui.reset()
}

fn cmd_tui(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	mut app := &App{api_url: api_url, bearer: bearer}
	app.width, app.height = term.get_terminal_size()
	app.tui = tui.init(
		user_data: app
		event_fn: event
		frame_fn: frame
		cleanup_fn: cleanup
	)
	app.tui.run()!
}

const command_tui_conf = cli.Command{
	name: 'tui'
	description: 'Nice Terminal User Interface'
	execute: cmd_tui
}
