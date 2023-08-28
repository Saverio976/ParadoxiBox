module main

import cli

// get

fn cmd_get_improvise(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	improvised := api_get_improvise(api_url, bearer)!
	println('${improvised}')
}

const command_get_improvise_conf = cli.Command{
	name: 'get'
	description: 'Get improvise auto state'
	execute: cmd_get_improvise
}

// toggle

fn cmd_toggle_improvise(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	api_toggle_improvise(api_url, bearer)!
}

const command_toggle_improvise_conf = cli.Command{
	name: 'toggle'
	description: 'Toggle improvise auto state'
	execute: cmd_toggle_improvise
}

// now

fn cmd_now_improvise(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	api_now_improvise(api_url, bearer)!
}

const command_now_improvise_conf = cli.Command{
	name: 'now'
	description: 'Add new song to queue based on current'
	execute: cmd_now_improvise
	flags: [
		cli.Flag{
			flag: cli.FlagType.int
			name: 'n'
			abbrev: 'n'
			description: 'number of song to add'
			required: true
		}
	]
}

// base

const command_improvise_conf = cli.Command{
	name: 'improvise'
	description: 'Position in time of current song'
	execute: fn (cmd cli.Command) ! {
		cmd.execute_help()
	}
	commands: [
		command_now_improvise_conf,
		command_toggle_improvise_conf,
		command_get_improvise_conf,
	]
}
