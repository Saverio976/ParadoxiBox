module main

import x.json2
import net.http

struct GetPosResponse {
	pos int
}

fn api_set_pos(api_url string, bearer string, pos int) ! {
	resp := http.fetch(http.FetchConfig{
		url: api_url + '/songs/queue/current/pos/set'
		params: {
			'pos': '${pos}'
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

fn api_get_pos(api_url string, bearer string) !int {
	resp := http.fetch(http.FetchConfig{
		url: api_url + '/songs/queue/current/pos'
		method: http.Method.get
		header: http.new_header_from_map({
			http.CommonHeader.authorization: 'Bearer ' + bearer
		})
	})!
	if resp.status_code != 200 {
		return error('Unexpected status code: ${resp.status_code}')
	}
	resp_json := json2.decode[GetPosResponse](resp.body)!
	return resp_json.pos
}

fn api_get_pos_max(api_url string, bearer string) !int {
	resp := http.fetch(http.FetchConfig{
		url: api_url + '/songs/queue/current/pos'
		method: http.Method.get
		header: http.new_header_from_map({
			http.CommonHeader.authorization: 'Bearer ' + bearer
		})
	})!
	if resp.status_code != 200 {
		return error('Unexpected status code: ${resp.status_code}')
	}
	resp_json := json2.decode[GetPosResponse](resp.body)!
	return resp_json.pos
}
