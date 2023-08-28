module main

import cli

fn cmd_pause(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	api_pause(api_url, bearer)!
}

const command_pause_conf = cli.Command{
	name: 'pause'
	description: 'Pause current song'
	execute: cmd_pause
}
