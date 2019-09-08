import pafy,ffmpeg,sqlite3,secrets

def download_low_quality(url):
    conn = sqlite3.connect('vid.db')
    c = conn.cursor()
    video = pafy.new(url)
    best = video.getbest()
    vid = video.title + "." + best.extension
    query = 'SELECT * from videos WHERE name = ?;'
    c.execute(query,(vid,))
    data = c.fetchone()
    if data:
        query = 'UPDATE videos SET del="false" WHERE id=?;'
        c.execute(query,(data[0],))
        conn.commit()
        conn.close()
        return data[0], data[1]
    else:
        best.download(filepath="static/")
        vidid = secrets.token_hex(15)
        query = 'INSERT INTO videos (id, name, del) VALUES (?, ?, "false");'
        c.execute(query,(vidid, vid))
        conn.commit()
        conn.close()
        return vidid, vid

def download_high_quality(url):
    conn = sqlite3.connect('vid.db')
    c = conn.cursor()
    video = pafy.new(url)
    bestvid = video.getbestvideo()
    aud = video.getbestaudio()
    audio = video.title + "." + aud.extension
    vid = video.title + "." + bestvid.extension
    query = 'SELECT * from videos WHERE name = ?;'
    c.execute(query,(vid,))
    data = c.fetchone()
    if data:
        query = 'UPDATE videos SET del="false" WHERE id=?;'
        c.execute(query,(data[0],))
        conn.commit()
        conn.close()
        return data[0], data[1]
    else:
        vidid = secrets.token_hex(15)
        vid.download('static/vid')
        aud.download('static/aud')
        try:
            out, err = (ffmpeg
            .input('static/aud'+audio)
            .input('static/vid'+vid)
            .output('static/'+vid)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            print(e.stderr)
    return vidid, vid
        


def download_audio_only(url):
    conn = sqlite3.connect('vid.db')
    c = conn.cursor()
    video = pafy.new(url)
    aud = video.getbestaudio()
    audio_input = video.title + "." + "webm"
    vid = video.title + "." + "mp3"
    query = 'SELECT * from videos WHERE name = ?;'
    c.execute(query,(vid,))
    data = c.fetchone()
    if data:
        query = 'UPDATE videos SET del="false" WHERE id=?;'
        c.execute(query,(data[0],))
        conn.commit()
        conn.close()
        return data[0], data[1]
    else:
        vidid = secrets.token_hex(15)
        aud.download('static/')
        try:
            out, err = (ffmpeg
            .input(audio_input)
            .output(vid, format='mp3', acodec='libmp3lame', ac=2)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            print(e.stderr)
        query = 'INSERT INTO videos (id, name, del) VALUES (?, ?, "false");'
        c.execute(query,(vidid, vid))
        conn.commit()
        conn.close()
        return vidid, vid
    

download_audio_only("https://www.youtube.com/watch?v=y7aDi0-FC7o&t")
