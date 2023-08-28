module main

import os
import cli
import x.json2

struct ConfigCLI {
mut:
	bearer ?string
	url_api ?string
}

fn get_conf_dir() string {
	return os.getenv_opt('XDG_CONFIG_HOME') or { return os.home_dir() + '/.config' }
}

fn get_conf_cli_path() string {
	return get_conf_dir() + '/paradoxibox-cli'
}

fn get_conf_cli_file() string {
	return get_conf_cli_path() + '/config.json'
}

fn cmd_login(cmd cli.Command) ! {
	os.mkdir_all(get_conf_cli_path())!
	if !os.is_file(get_conf_cli_file()) {
		os.write_file(get_conf_cli_file(), json2.encode[ConfigCLI](ConfigCLI{}))!
	}
	mut conf := json2.decode[ConfigCLI](os.read_file(get_conf_cli_file())!)!
	email := cmd.flags.get_string('email')!
	password := cmd.flags.get_all_found().get_string('password') or {
		os.input_password('Password: ') or { return error('No password provided') }
	}
	url_api := cmd.flags.get_string('url-api')!
	conf.bearer = api_login(url_api, email, password)!
	conf.url_api = url_api
	os.write_file(get_conf_cli_file(), json2.encode[ConfigCLI](conf))!
}

fn get_bearer() !string {
	conf := json2.decode[ConfigCLI](os.read_file(get_conf_cli_file())!)!
	if conf.bearer == none {
		return error('No bearer, please login')
	}
	return conf.bearer or { '' }
}

fn get_url_api() !string {
	conf := json2.decode[ConfigCLI](os.read_file(get_conf_cli_file())!)!
	if conf.url_api == none {
		return error('No url api, please login')
	}
	return conf.url_api or { '' }
}

const command_login_conf = cli.Command{
	name: 'login'
	description: 'Login to the api'
	execute: cmd_login
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
			name: 'url-api'
			abbrev: 'u'
			description: 'ParadoxiBox api url (i.e.: http://localhost:8080/api)'
			required: true
		},
	]
}
