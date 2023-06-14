

def video_link_cleaner(video_link):
    import re
#Video URL does not need a formatting function but link_id is helpful for naming videos. Also useful if Getty's URL conventions change in the future.
    video_link = re.split("\?",video_link)[0]
    link_id = video_link.partition("-id")[2]
    return video_link, link_id
 






    
