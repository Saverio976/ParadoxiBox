module main

import cli

fn cmd_is_paused(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := cmd.flags.get_string('url-api')!
	is_paused := api_is_paused(api_url, bearer)!

	println('is paused: ${is_paused}')
}

const command_is_paused_conf = cli.Command{
	name: 'is-paused'
	description: 'Check current song is paused'
	execute: cmd_is_paused
}
