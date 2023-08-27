module main

import os
import cli

fn cmd_create_account(cmd cli.Command) ! {
	email := cmd.flags.get_string('email')!
	password := cmd.flags.get_all_found().get_string('password') or {
		os.input_password('Password: ') or { return error('No password provided') }
	}
	username := cmd.flags.get_string('username')!
	url_api := cmd.flags.get_string('url-api')!
	api_create_account(url_api, email, username, password)!
}

const command_create_account_conf = cli.Command{
	name: 'create-account'
	description: 'Create an Account to the api'
	execute: cmd_create_account
	flags: [
		cli.Flag{
			flag: cli.FlagType.string
			name: 'email'
			abbrev: 'e'
			description: 'Email'
			required: true
		},
		cli.Flag{
			flag: cli.FlagType.string
			name: 'password'
			abbrev: 'p'
			description: 'Password (if not provided, you will be prompted)'
		},
		cli.Flag{
			flag: cli.FlagType.string
			name: 'username'
			abbrev: 'user'
			description: 'Username'
			required: true
		},
	]
}
