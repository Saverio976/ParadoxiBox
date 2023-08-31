module player_service

pub struct Response {
pub:
	title string
	value string
}

fn split_data(data string) (string, string) {
	rstring, lstring := data.split_once(':') or { data, '' }
	return rstring, lstring
}
