# -*- coding: utf-8 -*-
import sys, getopt, os
from datetime import datetime as dt
try:
    import pafy
except ImportError:
    error_on_import('to use this script you should install pafy\nrun [sudo] pip --install pafy', 2)

try:
    from pydub import AudioSegment
except ImportError:
    error_on_import('to use this script you should install pydub\nrun [sudo] pip --install pydub')



def error_on_import(text, status = 1):
    print(text)
    sys.exit(status)

def download_callback(total, recvd, ratio, rate, eta):
    print('Time left : %d Seconds' % int(eta) , end='\r')
    if total == recvd:
        print()

def sorted_playlist(item):
    return dt.strptime(k['playlist_meta']['added'], "%m/%d/%y")
def download(link , type='file' ,dirc = os.getcwd(), mFormat = 'mp3' ):
    """
        Download the video link as audio file.
        default format is mp3.
        @params:
            link    - Required : the youtube link of the video or playlist.
            type    - Optional : the type of download (file or playlist).
            dir     - Optional : the directory the files download to.
            format  - Optional : the format of the download files.
    """
    if(type == 'file'):
        item = pafy.new(link)
        handleonefile(item, dirc, mFormat)
    elif(type == 'playlist'):
        playlist = pafy.get_playlist(link)
        items = sorted(playlist['items'] , key= lambda k : dt.strptime(k['playlist_meta']['added'], "%m/%d/%y"))
        for item in items:
            handleonefile(item['pafy'], dirc, mFormat)
    else:
        raise ValueError("argument type should be only 'type' or 'playlist'")

def handleonefile(item, dirc, mFormat):
    ba = item.getbestaudio()
    downloadname = dirc + '/' + item.title + '.'+ ba.extension
    filename = ba.download(filepath=downloadname, quiet=True, callback=download_callback)
    print('Finish download file ' + filename)
#    convert_file(filename, mFormat)
#    print('Done Convert file to mp3')
#    delete_file(filename)

def convert_file(filename, mFormat):
    """
        Convert file from m4a or wbem to mp3 file
        @params
            filename    - Required : the original file.
            mFormat - Required : the format to be convert to.
    """
    exten = filename[filename.rfind('.')+1::]
    convertname = filename[:filename.rfind('.') + 1:] + mFormat
    raw = AudioSegment.from_file(filename, format=exten)
    raw.export(convertname, format=mFormat)

def delete_file(filename):
    os.remove(filename)
