module main

import cli

fn cmd_next(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := cmd.flags.get_string('url-api')!
	api_next(api_url, bearer)!
}

const command_next_conf = cli.Command{
	name: 'next'
	description: 'Skip to the next song'
	execute: cmd_next
}
