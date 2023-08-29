module main

import os
import flag
import miniaudio

fn main() {
    mut fp := flag.new_flag_parser(os.args)
    fp.application('musicplayer')
    fp.version('v0.0.1')
    fp.limit_free_args(0, 0)! // comment this, if you expect arbitrary texts after the options
    fp.description('Music Player for ParadoxiBox')
    fp.skip_executable()
    file_lock := fp.string_opt('file-lock', `l`, 'lock file to acquire before writing/reading')!
	file := fp.string_opt('file', `f`, 'file in which the communication will be')!
    additional_args := fp.finalize() or {
        eprintln(err)
        println(fp.usage())
        return
    }
    println(additional_args.join_lines())
}
