import re

#Functionality for handling the special URL of a Getty Board
def board_link_cleaner(board_image_link, **kwargs):
 
#Build the size_string
    if 'size' in kwargs:
        dimension = kwargs['size']
        size_string = "?s="+dimension+"x"+dimension
    else:
        size_string = "?s=2048x2048"
        
        

        

  #Detect media_type and find image/video id.
    if re.search("photos", board_image_link):
        media_type = "image"
        split_link = re.split("\?", board_image_link)
        main_link_part = split_link[0]

        link_id = re.split("-id",main_link_part)[1]
        new_link = main_link_part + size_string


    elif re.search("videos", board_image_link):
        media_type = "video"

        split_link = re.split("\?", board_image_link)[0]

        link_id = split_link.partition("-id")[2]
        new_link = split_link

                





    return new_link,link_id, media_type





    
