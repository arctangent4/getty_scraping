import re


def board_link_cleaner(board_image_link, **kwargs):
 

    if 'size' in kwargs:
        dimension = kwargs['size']
        size_string = "?s="+dimension+"x"+dimension
    else:
        size_string = "?s=2048x2048"
        
        

        

  
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

#url ="https://media.gettyimages.com/photos/female-doctor-teaching-how-to-wearing-surgical-mask-for-protect-and-picture-id1215085919?k=6&m=1215085919&s=612x612&w=0&h=oTtjRPTfb3l_YqR2kLEJ63SQr85bWwzoMMogEYgce2Y="
#board_link_cleaner(url, size='1024')

#
#url = "https://media.gettyimages.com/videos/female-nurse-wearing-a-gown-surgical-face-mask-gloves-and-a-face-a-video-id1252939357?s=640x640"
#board_link_cleaner(url)





    