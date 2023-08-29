module main

import os
import flag
import time

fn loop(mut player &Player) {
    mut last_data := ""
    mut stop := false

    for {
        time.sleep(time.millisecond)
        if stop {
            break
        }
        data := communicate_read(player.lockfile, player.file)
        if data == last_data {
            continue
        }
        res := interpret_data(data, mut player)
        communicate_write(player.lockfile, player.file, res)
        last_data = res
        if last_data.starts_with("stop") && last_data.ends_with("OK") {
            stop = true
        }
    }
}

fn main() {
    mut fp := flag.new_flag_parser(os.args)
    fp.application('musicplayer')
    fp.version('v0.0.1')
    fp.limit_free_args(0, 0) or {
        eprintln(err)
        println(fp.usage())
        return
    }
    fp.description('Music Player for ParadoxiBox')
    fp.skip_executable()
    file_lock := fp.string_opt('file-lock', `l`, 'lock file to acquire before writing/reading') or {
        eprintln(err)
        println(fp.usage())
        return
    }
	file := fp.string_opt('file', `f`, 'file in which the communication will be') or {
        eprintln(err)
        println(fp.usage())
        return
    }
    _ := fp.finalize() or {
        eprintln(err)
        println(fp.usage())
        return
    }
    communicate_clear(file_lock, file)
    mut player := init_player(file_lock, file)!
    loop(mut player)
    uninit_player(mut player)
}
