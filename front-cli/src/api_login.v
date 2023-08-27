module main

import net.http
import x.json2

pub struct LoginResponse {
	bearer ?string
}

fn api_login(api_url string, email string, password string) !string {
	resp := http.fetch(http.FetchConfig{
		url: api_url + '/auth/login'
		params: {
			'email':    email
			'password': password
		}
		method: http.Method.get
	})!
	if resp.status_code != 200 {
		return error('Unexpected status code: ${resp.status_code}')
	}
	resp_json := json2.decode[LoginResponse](resp.body)!
	if resp_json.bearer == none || resp_json.bearer? == 'null' {
		return error('Please create an account or provide true email and password: ${resp_json.bearer}')
	}
	return resp_json.bearer or { '' }
}
