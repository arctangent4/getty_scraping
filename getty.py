
from selenium import webdriver
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
import urllib.request
import time
import os
import sys
import argparse
import re
from datetime import datetime


import logging
import math
import fileinput
from gettyboards import *
from gettyvideos import *
from gettyimages import *


#Installs new version of Chrome Webdriver each time.
chrome_options = webdriver.ChromeOptions()

#Useful options for either debugging or making the driver invisible
chrome_options.add_argument("--headless")
# chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)



#ARGUMENTS
parser = argparse.ArgumentParser(description="This is the parser for the Getty downloader.")
parser.add_argument("url", help = "Choose an url to scrape ")
parser.add_argument("-d", "--dir", help = "Choose a directory to store images in ")
parser.add_argument("-num", "--image-number",dest="imgs", type = int, help = "Choose how many images you want to download; it must be a positive integer.")
parser.add_argument("-pn",  "--page-number",dest="pages", help = "Choose how many pages of images you want to download; it can be a fractional number. If you have already provided the number of images, the program will use that argument instead of the number of pages. ")

img_sizes = ['2048','1024','612']
parser.add_argument("-s", "--size", choices = img_sizes, help = "Choose an image size to download in. Choices: '2048' for max size of 2048x2048 px, '1024' for max size of 1024x1024 px, and '612' for max size of 612x612 px.")
 
args = parser.parse_args()


path = os.getcwd()+"/downloads/"
if os.path.exists(path) == False:
    os.mkdir(path)


#PROGRAM HEAD--COLLATES ARGUMENTS AND CALLS NECESSARY SCRAPER
def selenium_head(url,directory,**kwargs):

 
    # if kwargs["size"] != 612:
    #     print(f"Requested image size is not 612x612. Please be patient as the program must manually click links for {kwargs['size']}x{kwargs['size']} images")
    #     img_manual_scrape()

    #Collect kwargs and determines number of media items to be scraped
    if  kwargs["imgs"]:
        media_number = kwargs["imgs"]

        if media_number < 1:
            raise Exception("Sorry, but your number of media items cannot be less than or equal to 1.")
        
        pages = math.ceil(float(media_number)/80)
        pages_string = round(pages,2)
        print(f"Downloading {media_number} items, or ~ {pages} pages in total...\n")
    
    elif kwargs["pages"]:
        pages = float(kwargs["pages"])
        media_number = math.ceil(pages*80)

        if pages <= 0:
            raise Exception("Sorry, but your number of pages cannot be less than or equal to 0.")
        
        print(f"Downloading {pages} pages, or {media_number} items in total...\n")
        pages = math.ceil(pages)
        #Converting to the actual amount used in the iterator
        
    else:
        pages = 1
        media_number = math.ceil(float(pages*80))
        print(f"No number of pages or videos specified. Defaulting to downloading 1 page, or {media_number} items in total... \n")
    

#If Statement to determine nature of the input URL.
    if re.search("gettyimages.com/collaboration/boards", url):
        print("\nURL given has been identified as a board. \n")
        board_scraper(path,driver,directory,pages,media_number, kwargs)
        
    elif re.search("gettyimages.com/photos/", url):
        print("\nURL given has been identified as an image search. \n")
        image_scraper(path,driver,directory,pages,media_number,kwargs)

        
    elif re.search("gettyimages.com/videos", url):
        print("\nURL given has been identified as a video search. \n")
        video_scraper(path,driver,directory,pages,media_number, kwargs)

        
    elif re.search("gettyimages.com/search/more-like-this", url):
        print("\nURL given has been identified as a similar images search. \n")
        image_scraper(path,driver,directory,pages,media_number, kwargs)
        
    elif re.search("gettyimages.com/search",url):
        print("\nURL given has been identified as a special image search. \n")
        image_scraper(path,driver,directory,pages,media_number, kwargs)
        
    else:
        print("\nThe program could not process the URL given. Please check to see if the URL you provided is correct and from a gettyimages.com image search, video search, or board.")
        exit()

#CREATE A 'DEFAULT' DIRECTORY
def create_default_directory(search_link):
    if re.search("phrase", search_link) and re.search("photos", search_link):
        split_search_link= re.split("&", search_link)

        for fragment in split_search_link:
            if re.search("phrase", fragment):
                keyword = re.sub("phrase=","",fragment)
                hashtag_clean = keyword.partition("#")[0]
                title = re.sub("%20"," ",hashtag_clean)
                
                
    elif re.search("phrase", search_link) and re.search("videos", search_link):
        split_search_link= re.split("&", search_link)

        for fragment in split_search_link:
            
            if re.search("phrase", fragment):
                keyword = re.split("phrase=", fragment)[1]
                hashtag_clean = keyword.partition("#")[0]
                title = re.sub("%20"," ",hashtag_clean)+" videos"

                
    elif re.search("phrase", search_link) and re.search("more-like-this", search_link):
        split_search_link= re.split("&", search_link)
      
        for fragment in split_search_link:
            if re.search("phrase", fragment):
                keyword = re.sub("phrase=","",fragment)
                hashtag_clean = keyword.partition("#")[0] 
                title = re.sub("%20"," ",hashtag_clean)
                
    elif re.search("collaboration/boards/", search_link):
        driver.get(search_link)
        board_name = driver.title
        board_name = re.sub(" Board","", board_name)
        title = board_name

        
    else:
        time = str(datetime.now()).replace(":","_").replace(".","_")
        title = "Images downloaded on " + time
            
    return title


        

#CREATE DIR / RUN PROGRAM
if __name__ == "__main__":

    search_link = args.url

#Determines Directory Argument
    if args.dir:
        directory = args.dir

    else:
        directory = create_default_directory(search_link)
            
    #Make dir if it doesn't exist
    if os.path.exists(os.path.join(path, directory)) == False:
        os.makedirs(os.path.join(path, directory))

    #If directory already exists, we will make a subfolder to partition newly downloaded files from existing ones.
    else:
        dirnumber = 0
        parent_path = os.path.join(path, directory)
        print(parent_path)
        while os.path.exists(os.path.join(parent_path, str(dirnumber))) == True:
            dirnumber+=1
            
        newdir = directory+"/"+str(dirnumber)

     
        os.makedirs(os.path.join(path,newdir))
        print(f"You already have a directory called '{directory}'. A temporary directory was made at {newdir}")
        directory = newdir
            


    #Actual execution of the program
    driver.get(search_link)
    selenium_head(search_link,directory,pages = args.pages, imgs = args.imgs, size = args.size)
    print("\nJob is finished")
    driver.close()

        

#Work in progress code to manually scrape larger image sizes    
# def img_manual_scrape(directory,pages, media_number, **kwargs):

#     img_size = kwargs["size"]
#     if img_size=="1024":
#         link_index = 1
#     elif img_size=="2048":
#         link_index =2
#     else:
#         print("Unrecognized image size. Defaulting to 2048x2048")
#         link_index =2
        


#     for i in range(pages): 
#         driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') # Scroll to the end of page.
#         time.sleep(2) # Wait for all the images to load correctly.

#         image_links = []

#         target_divs = driver.find_elements(By.XPATH, "//div[contains(@data-testid, 'galleryMosaicAsset')]") 
#         nav_links = [div.find_elements(By.XPATH, "//a") for div in target_divs]
#         for link in nav_links:
#             #Add bit that navigates link into view
#             link.click()
#             parent_container = driver.find_element(By.XPATH, "//picture[contains(@data-testid, 'hero-picture')]")
#             source_links = parent_container.find_elements(By.XPATH, "//source")
#             img_link = [item.get_attribute("srcset") for item in source_links][link_index]
#             image_links.append(img_link)

#             time.sleep(2)
#             driver.back()
            


#         # images = driver.find_elements(By.XPATH, "//img[parent::picture]") # Find all images.
     
#         nextpage = driver.find_element(By.XPATH, "//button[@title='Next page']")
#         # driver.execute_script("arguments[0].scrollIntoView()", nextpage)
#         print(f"\nDownloading {i+1} out of {pages} pages\n")
# #        
#     #        
#     ##        with Bar('Processing', max=media_number) as bar:
#     ##            for i in range(media_number):
#     ##                i+=1
#     ##                bar.next()


#         for img_link in image_links: 
#             if k <= media_number:
#                 try:
#                     id = image_link_cleaner(img_link)
#  # Get the link


#                     media_download(path,img_link,directory,".png", id) # And download it to directory
#                     print(f"[{k}/{media_number}] Downloaded video {id}")
#                     k+=1

#                     time.sleep(1)

#                 except Exception as e:
#                         logging.error(f"An error occurred in downloading the {k}th video: {str(e)}")

#         try:

#             nextpage = driver.find_element_by_class_name('PaginationRow-module__nextButton___1A4gS')
#                                                 # const elem = document.getElementById('site-top-header-wrapper')
#             # driver.execute_script(""" 
#             #                         const elem = arguments[0];
#             #                         const y_offset = -200;
#             #                         const target = elem.getBoundingClientRect().top + window.pageYOffset + y_offset;
#             #                         window.scrollTo({top:target, behavior: 'smooth'});

#             #                       """
#             #                       , nextpage)
            
#             nextpage.click() # Move to next page
#         except Exception as e:
#             logging.error(f"An error occurred in scrolling: {str(e)}")
