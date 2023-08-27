module main

import net.http

fn api_is_paused(api_url string, bearer string) ! {
	resp := http.fetch(http.FetchConfig{
		url: api_url + '/songs/is-paused'
		method: http.Method.get
		header: http.new_header_from_map({
			http.CommonHeader.authorization: 'Bearer ' + bearer
		})
	})!
	if resp.status_code != 200 {
		return error('Unexpected status code: ${resp.status_code}')
	}
}
