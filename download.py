import urllib
import logging
import os


def media_download(path, url,directory,file_extension, id):
 
    try:
        filename = id + file_extension 
        media_path = os.path.join(path, directory, filename)
      
        urllib.request.urlretrieve(url, media_path) # download image and video

    
    except Exception as e:
       logging.error(f"Failed to fetch a file:{e}")
