from flask import Flask, redirect, render_template, request,send_file,jsonify,abort
import waitress, os, pafy, sqlite3,secrets

def createdatabase():
    conn = sqlite3.connect('vid.db')
    c = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS videos (id TEXT, name TEXT, del TEXT);"
    c.execute(query)
    conn.commit()
    conn.close()

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

app = Flask(__name__)
@app.route("/", methods=['GET'])
def main():
    return render_template("main.html")

@app.route("/downloads", methods=['POST'])
def js():    
    data = request.json
    if "quality" in data:
        if data['quality']=="low":
            vidurl, video = download_low_quality(data['url'])
            if video != None:
                return jsonify({"error":0,"video_url":vidurl,"filename":video})
            else:
                return jsonify({"error":1, "error_details":"A problem occured downloading this video"})
        else:
            return abort(404)
    else:
        return abort(404)

@app.route("/files/<fileid>", methods=['GET'])
def vidfile(fileid):
    conn = sqlite3.connect('vid.db')
    c = conn.cursor()
    query = 'SELECT * FROM videos WHERE id=?;'
    c.execute(query,(fileid,))
    data = c.fetchone()
    if data:
        query = 'UPDATE videos SET del="true" WHERE id=?;'
        c.execute(query,(fileid,))
        conn.commit()
        conn.close()
        return send_file("static/"+data[1], as_attachment=True)
    else:
        conn.close() 
        return abort(404)
if __name__ == '__main__':
    createdatabase()
    app.secret_key = os.urandom(1000)
    #app.run(host='0.0.0.0', port=5050, debug = True,)
    waitress.serve(app,port=5050)