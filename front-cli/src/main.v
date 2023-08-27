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
		flags: [
			cli.Flag{
				flag: cli.FlagType.string
				name: 'url-api'
				abbrev: 'u'
				global: true
				description: 'ParadoxiBox api url (i.e.: http://localhost:8080/api)'
				required: true
			},
		]
		posix_mode: true
	}
	app.add_command(command_queue_conf)
	app.add_command(command_login_conf)
	app.add_command(command_add_song_conf)
	app.setup()
	app.parse(os.args)
}
