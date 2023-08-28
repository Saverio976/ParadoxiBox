module main

import x.json2
import net.http

struct GetImproviseResponse {
	improvise bool
}

fn api_toggle_improvise(api_url string, bearer string) ! {
	resp := http.fetch(http.FetchConfig{
		url: api_url + '/songs/improvise/auto/toggle'
		method: http.Method.get
		header: http.new_header_from_map({
			http.CommonHeader.authorization: 'Bearer ' + bearer
		})
	})!
	if resp.status_code != 200 {
		return error('Unexpected status code: ${resp.status_code}')
	}
}

fn api_get_improvise(api_url string, bearer string) !bool {
	resp := http.fetch(http.FetchConfig{
		url: api_url + '/songs/improvise/auto'
		method: http.Method.get
		header: http.new_header_from_map({
			http.CommonHeader.authorization: 'Bearer ' + bearer
		})
	})!
	if resp.status_code != 200 {
		return error('Unexpected status code: ${resp.status_code}')
	}
	resp_json := json2.decode[GetImproviseResponse](resp.body)!
	return resp_json.improvise
}

fn api_now_improvise(api_url string, bearer string) ! {
	resp := http.fetch(http.FetchConfig{
		url: api_url + '/songs/improvise/auto/now'
		method: http.Method.get
		header: http.new_header_from_map({
			http.CommonHeader.authorization: 'Bearer ' + bearer
		})
	})!
	if resp.status_code != 200 {
		return error('Unexpected status code: ${resp.status_code}')
	}
}
