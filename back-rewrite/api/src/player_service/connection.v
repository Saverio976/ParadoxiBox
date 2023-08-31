module player_service

import time

pub struct Connection {
	commands chan Command
	responses shared map[int]Response
	t thread int
}

fn bus_connection(commands chan Command, shared responses map[int]Response, lockfile string, file string) int {
	mut stop := false
	for !stop && commands.closed == false {
		eprintln('loop')
		select {
			cm := <- commands {
				eprintln('this -1')
				s := cm.str()
				communicate_write(lockfile, file, s)
				mut data := s
				eprintln('this 0')
				for data == s {
					time.sleep(time.microsecond)
					data = communicate_read(lockfile, file)
					eprintln('this 1')
				}
				eprintln('this 2')
				rsplit, lsplit := split_data(data)
				eprintln('this 3')
				res := Response{
					title: rsplit
					value: lsplit
				}
				if res.title == 'stop' && res.value == 'OK' {
					stop = true
				}
				lock responses {
					responses[cm.id] = res
				}
			}
		}
	}
	return 0
}

pub fn start_connection(lockfile string, file string) !Connection {
	communicate_clear(lockfile, file)
	shared responses := map[int]Response{}
	commands := chan Command{}
	t := go bus_connection(commands, shared responses, lockfile, file)
	return Connection{
		commands: commands
		responses: responses
		t: t
	}
}

pub fn (cn Connection) send_command(title string, value string) int {
	eprintln('err 1')
	cm := new_command(title, value)
	eprintln('err 2')
	cn.commands <- cm
	eprintln('err 3')
	return cm.id
}

pub fn (cn Connection) get_response(id int) !Response {
	mut found := false
	for !found {
		time.sleep(time.microsecond)
		rlock cn.responses {
			found = id in cn.responses
		}
	}
	mut rs := Response{}
	lock cn.responses {
		rs = cn.responses[id] or { return error('id ${id} not found') }
		cn.responses.delete(id)
	}
	return rs
}
