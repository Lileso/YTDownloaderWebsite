import sqlite3, os
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

updateyt()
removefiles()