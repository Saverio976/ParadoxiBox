module main

import cli

fn cmd_get_vol(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	vol := api_get_vol(api_url, bearer)!
	println('${vol}')
}

const command_get_vol_conf = cli.Command{
	name: 'get'
	description: 'Get current volume'
	execute: cmd_get_vol
}

fn cmd_set_vol(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	vol := cmd.flags.get_int('vol')!
	api_set_vol(api_url, bearer, vol)!
}

const command_set_vol_conf = cli.Command{
	name: 'set'
	description: 'Set current volume'
	execute: cmd_set_vol
	flags: [
		cli.Flag{
			flag: cli.FlagType.int
			name: 'vol',
			abbrev: 'v',
			description: 'volume'
			required: true
		}
	]
}

const command_vol_conf = cli.Command{
	name: 'vol'
	description: 'Position in time of current song'
	execute: fn (cmd cli.Command) ! {
		cmd.execute_help()
	}
	commands: [
		command_get_vol_conf,
		command_set_vol_conf,
	]
}
