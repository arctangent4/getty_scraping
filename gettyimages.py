#import datetime


def image_link_cleaner(image_link,**kwargs):
    import re
    #currently in 2048x2048, 612x612 and 1024x1024 also works
    if 'size' in kwargs:
        dimension = kwargs['size']
        size_string = "?s="+dimension+"x"+dimension
    else:
        size_string = "?s=2048x2048"
        
    split_link = re.split("/", image_link)
    link_id = split_link[-1]
    link_id = re.sub("\?adppopup=true","",link_id)

    link_phrase = re.sub("-news-photo","",split_link[-2])
    link_phrase = re.sub("news-photo-","",link_phrase) 
    new_link = "https://media.gettyimages.com/photos/"+link_phrase+ "-picture-id" +link_id +size_string
#    print(new_link)
#    print("pls")
    
    return new_link, link_id



#image_link_cleaner("https://www.gettyimages.com/detail/photo/portrait-asian-female-doctor-wearing-face-shield-royalty-free-image/1215687764?adppopup=true")

#time = str(datetime.now()).replace(":","_").replace(".","_")
#title = "Images downloaded on " + str(time)
#print(title)








