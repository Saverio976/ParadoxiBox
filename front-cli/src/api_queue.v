module main

import net.http
// change this import to x.json2 when good parsing of array
import json

pub struct SongQueued {
	id              string
	title           string
	artist          string
	source_link     string
	duration_second f32
	thumbnail_url   string
	file_url        string
}

pub struct SongsQueued {
	songs []SongQueued
}

fn api_queue(api_url string, bearer string) ![]SongQueued {
	resp := http.fetch(http.FetchConfig{
		url: api_url + '/songs/queue'
		method: http.Method.get
		header: http.new_header_from_map({
			http.CommonHeader.authorization: 'Bearer ' + bearer
		})
	})!
	if resp.status_code != 200 {
		return error('Unexpected status code: ${resp.status_code}')
	}
	return json.decode(SongsQueued, resp.body)!.songs
}
