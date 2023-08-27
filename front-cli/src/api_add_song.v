module main

import net.http

struct AddSong {
mut:
	url_song     ?string
	search_song  ?string
	url_playlist ?string
}

fn api_add_song(api_url string, bearer string, song AddSong) ! {
	if song.url_song != none {
		resp := http.fetch(http.FetchConfig{
			url: api_url + '/songs/queue/add/song/url'
			params: {
				'url': song.url_song or { '' }
			}
			method: http.Method.get
			header: http.new_header_from_map({
				http.CommonHeader.authorization: 'Bearer ' + bearer
			})
		})!
		if resp.status_code != 200 {
			return error('Unexpected status code: ${resp.status_code}')
		}
	}
	if song.search_song != none {
		resp := http.fetch(http.FetchConfig{
			url: api_url + '/songs/queue/add/song/search'
			params: {
				'search': song.search_song or { '' }
			}
			method: http.Method.get
			header: http.new_header_from_map({
				http.CommonHeader.authorization: 'Bearer ' + bearer
			})
		})!
		if resp.status_code != 200 {
			return error('Unexpected status code: ${resp.status_code}')
		}
	}
	for song.url_playlist != none {
		resp := http.fetch(http.FetchConfig{
			url: api_url + '/songs/queue/add/playlist/url'
			params: {
				'url': song.url_playlist or { '' }
			}
			method: http.Method.get
			header: http.new_header_from_map({
				http.CommonHeader.authorization: 'Bearer ' + bearer
			})
		})!
		if resp.status_code != 200 {
			return error('Unexpected status code: ${resp.status_code}')
		}
	}
}
