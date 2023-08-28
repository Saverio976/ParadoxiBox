module main

import x.json2
import net.http

struct GetVolResponse {
	volume int
}

fn api_set_vol(api_url string, bearer string, vol int) ! {
	resp := http.fetch(http.FetchConfig{
		url: api_url + '/songs/volume/set'
		params: {
			'volume': '${vol}'
		},
		method: http.Method.get
		header: http.new_header_from_map({
			http.CommonHeader.authorization: 'Bearer ' + bearer
		})
	})!
	if resp.status_code != 200 {
		return error('Unexpected status code: ${resp.status_code}')
	}
}

fn api_get_vol(api_url string, bearer string) !int {
	resp := http.fetch(http.FetchConfig{
		url: api_url + '/songs/volume'
		method: http.Method.get
		header: http.new_header_from_map({
			http.CommonHeader.authorization: 'Bearer ' + bearer
		})
	})!
	if resp.status_code != 200 {
		return error('Unexpected status code: ${resp.status_code}')
	}
	resp_json := json2.decode[GetVolResponse](resp.body)!
	return resp_json.volume
}
