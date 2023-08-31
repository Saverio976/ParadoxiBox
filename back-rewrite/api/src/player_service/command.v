module player_service

import rand

pub struct Command {
	title string [required]
	value string [required]
pub:
	id int [required]
}

fn new_command(title string, value string) Command {
	id := rand.int()
	return Command{
		title: title
		value: value
		id: id
	}
}

pub fn (cm Command) str() string {
	if cm.value == '' {
		return cm.title
	}
	return cm.title + ':' + cm.value
}
