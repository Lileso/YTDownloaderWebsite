import sqlite3, os,logging
from subprocess import check_call

def updateyt():
    check_call(['pip','install','--upgrade', 'youtube-dl','pafy','flask'])
    check_call(['systemctl','restart','ytdownloader'])

def removefiles():
    conn = sqlite3.connect('/etc/youtubedl/YTDownloaderWebsite/vid.db')
    c = conn.cursor()
    query = 'SELECT * from videos WHERE del = ?;'
    c.execute(query,("true",))
    data = c.fetchall()
    for x in data:
        filename =  x[1]
        os.remove(f'/etc/youtubedl/YTDownloaderWebsite/static/{filename}')   
        query = 'DELETE FROM videos WHERE id =?;'
        c.execute(query,(x[0],))
    conn.commit()
    conn.close()
LOG_FILE = "/etc/youtubedl/YTDownloaderWebsite/cleanup.log"
logging.basicConfig(level=logging.INFO, filemode='a', format='%(asctime)s, %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename=LOG_FILE)
logging.info("Updating python packages")
updateyt()
logging.info("Python packages updated")
logging.info("Removing video files")
removefiles()
logging.info("Video files removed")