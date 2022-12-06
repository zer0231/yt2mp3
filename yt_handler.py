from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import youtube_dl
import shutil
import datetime

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'downloading':
        print("downloading "+ str(round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1))+"%")
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def generate_name():
    x = datetime.datetime.now()
    x=str(x).replace('-','')
    x=x.replace(' ','')
    x=x.replace(':','')
    x=x.replace('.','')
    return x

output_name = generate_name()

def fetch_title(url):
    req = requests.get(url)
    bs = BeautifulSoup(req.text, "html.parser")
    title = bs.title
    return title.string

def download_to_mp3(url):
    print("Downloading: "+fetch_title(url))
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': './tmp/'+output_name+'/%(title)s.%(ext)s',
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Download started...")
        ydl.download([url])
    return True

def convert_to_zip():
    shutil.make_archive('./tmp/archives/'+output_name, 'zip', './tmp/'+output_name)
    print('Converted to zip')
    return output_name