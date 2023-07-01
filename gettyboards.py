import time
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import NoSuchElementException
import logging
from download import media_download
import re

#Functionality for handling the special URL of a Getty Board
def board_link_cleaner(board_image_link, **kwargs):
 
#Size String no longer built due to Getty website changes

    size_string = "?s=612x612"
        
  #Detect media_type and find image/video id.
    if re.search("photo", board_image_link):
        media_type = "image"
        # split_link = re.split("\?", board_image_link)
        # main_link_part = split_link[0]

        # link_id = re.split("-id",main_link_part)[1]



    elif re.search("video", board_image_link):
        media_type = "video"

        # split_link = re.split("\?", board_image_link)[0]

        # link_id = split_link.partition("-id")[2]

    pattern = r"/id/(\d+)/"

# Search for the pattern in the link using regular expression
    match = re.search(pattern,board_image_link)

    if match:
        # Extract the "id" value and "video" string from the match object
        link_id = match.group(1)

    print(link_id)
    return link_id, media_type




        
def board_scraper(path, driver, directory,pages,media_number,kwargs):
    #ONLY FOR IMAGE SIZE 612x612, refer to image_scraper() for more nuanced comments.

    k = 1
    for i in range(pages): 
        
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') # Scroll to the end of page.
        time.sleep(2) # Wait for all the images to load correctly.

        media= driver.find_elements(By.CLASS_NAME, "board-asset")




        

        print(f"\nDownloading {i+1} out of {pages} pages\n")

        for item in media: 
            if k <= media_number:
                try:

                    media_url = item.get_attribute('src') # Get the link
                    id, media_type = board_link_cleaner(media_url)

                    
                    if media_type == "image":
                        file_extension = ".png"
                        
                    elif media_type == "video":
                        file_extension = ".mp4"
                        
                    else:
                        raise Exception(f"Could not identify the media type of asset {id} ")

                    media_download(path,media_url,directory,file_extension, id) # And download it to directory
                    print(f"[{k}/{media_number}] Downloaded asset {id}")

                    k+=1
                    time.sleep(1)

                except Exception as e:
                        logging.error(f"An error occurred in downloading the {k}th image: {str(e)}")


        try:
            #Note nextpage for a board is different from a search.
            nextpage = driver.find_element(By.CLASS_NAME, 'next-page')
            driver.execute_script(""" 
                                const elem = arguments[0];
                                const y_offset = -500;
                                const target = elem.getBoundingClientRect().top + window.pageYOffset + y_offset;
                                console.log(target);
                                window.scrollTo(target,0);

                                """
                                , nextpage)
            time.sleep(2)
            nextpage.click() 

        except Exception as e:
            logging.error(f"An error occurred in scrolling: {str(e)}")

        time.sleep(2)
