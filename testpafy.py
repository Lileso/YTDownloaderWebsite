import pafy, ffmpeg
def DownloadVideo(url):
    #This whole def was written by Matt Limb github.com/MattLimb and slightly adapted to fit in my code
    video = pafy.new(url)
    print(video.videostreams)
    print(video.audiostreams)
    #best = video.getbest()
    #print(best)

    #dl_location = best.url
    #print(best.url)
    #best.download()
    '''
    import urllib.request, shutil
    with urllib.request.urlopen(dl_location) as response, open(f"{video.title}.mp4", 'wb') as out_file:
        shutil.copyfileobj(response, out_file)'''

def download_low_quality(url):
    video = pafy.new(url)
    best = video.getbest()
    best.download()
    vid = video.title + "." + best.extension
    return vid

def download_high_quality(url):
    video = pafy.new(url)
    vid = video.getbestvideo()
    aud = video.getbestaudio()
    vid.download()
    aud.download()
    

print(download_low_quality("https://www.youtube.com/watch?v=y7aDi0-FC7o&t"))
