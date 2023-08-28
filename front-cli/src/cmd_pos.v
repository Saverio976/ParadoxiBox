module main

import cli
import time

fn cmd_get_pos(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	pos := api_get_pos(api_url, bearer)!
	duration := time.Duration(pos * time.second)
	println('${duration} (${pos} second)')
}

const command_get_pos_conf = cli.Command{
	name: 'get'
	description: 'Get current song pos'
	execute: cmd_get_pos
}

fn cmd_set_pos(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	pos := cmd.flags.get_int('pos')!
	api_set_pos(api_url, bearer, pos)!
}

const command_set_pos_conf = cli.Command{
	name: 'set'
	description: 'Set current song pos'
	execute: cmd_set_pos
	flags: [
		cli.Flag{
			flag: cli.FlagType.int
			name: 'pos',
			abbrev: 'p',
			description: 'position'
			required: true
		}
	]
}

const command_pos_conf = cli.Command{
	name: 'pos'
	description: 'Position in time of current song'
	execute: fn (cmd cli.Command) ! {
		cmd.execute_help()
	}
	commands: [
		command_get_pos_conf,
		command_set_pos_conf,
	]
}
