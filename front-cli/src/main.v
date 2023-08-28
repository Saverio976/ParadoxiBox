module main

import os
import cli

fn main() {
	mut app := cli.Command{
		name: os.args[0]
		usage: os.args[0]
		description: 'ParadoxiBox cli ( https://github.com/Saverio976/ParadoxiBox )'
		execute: fn (cmd cli.Command) ! {
			cmd.execute_help()
		}
		posix_mode: true
	}
	app.add_command(command_queue_conf)
	app.add_command(command_login_conf)
	app.add_command(command_add_song_conf)
	app.add_command(command_next_conf)
	app.add_command(command_is_paused_conf)
	app.add_command(command_pause_conf)
	app.add_command(command_resume_conf)
	app.add_command(command_create_account_conf)
	app.add_command(command_config_conf)
	app.setup()
	app.parse(os.args)
}
