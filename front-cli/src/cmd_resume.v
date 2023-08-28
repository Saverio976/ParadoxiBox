module main

import cli

fn cmd_resume(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	api_resume(api_url, bearer)!
}

const command_resume_conf = cli.Command{
	name: 'resume'
	description: 'Resume current song'
	execute: cmd_pause
}
