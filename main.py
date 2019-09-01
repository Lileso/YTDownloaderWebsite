from flask import Flask, redirect, render_template, request
import waitress, os, pafy

def DownloadVideo(url):
    #This whole def was written by Matt Limb github.com/MattLimb and slightly adapted to fit in my code
    #analyses URL
    video = pafy.new(url)
    #finds best quality video
    best = video.getbest()
    #finds the direct url of the video
    dl_location = best.url
    #downloads the video so that its called the daymonth.mp4 eg 1stJanuary.mp4
    import urllib.request, shutil
    with urllib.request.urlopen(dl_location) as response, open(f"static/{video.title},mp4") as out_file:
        shutil.copyfileobj(response, out_file)

 
app = Flask(__name__)
@app.route("/", method=['GET','POST'])
def main():
    if request.method == "GET":
        render_template("main.html")
    elif request.method == 'POST':
        




if __name__ == '__main__':
    app.secret_key = os.urandom(1000)
    app.run(host='0.0.0.0', port=5050, debug = True,)
    #waitress.serve(app,port=5050)