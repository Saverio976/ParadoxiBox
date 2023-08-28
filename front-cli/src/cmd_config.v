module main

import cli

fn cmd_config(cmd cli.Command) ! {
	bearer := get_bearer() or { return error('Login first with command login') }
	api_url := get_url_api()!
	path := get_conf_cli_file()
	println('Config path: ${path}')
	println('Api url: ${api_url}')
	println('Bearer: ${bearer}')
}

const command_config_conf = cli.Command{
	name: 'config'
	description: 'Show config information'
	execute: cmd_config
}
