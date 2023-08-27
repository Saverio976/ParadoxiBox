module main

import net.http
import x.json2

pub struct CreateAccountResponse {
	status string
}

fn api_create_account(api_url string, email string, username string, password string) ! {
	resp := http.fetch(http.FetchConfig{
		url: api_url + '/auth/create'
		params: {
			'email':    email
			'password': password
			'username': username
		}
		method: http.Method.get
	})!
	if resp.status_code != 200 {
		return error('Unexpected status code: ${resp.status_code}')
	}
	resp_json := json2.decode[CreateAccountResponse](resp.body)!
	if resp_json.status != 'created' {
		return error('Unexpected status: ${resp_json.status}')
	}
}
