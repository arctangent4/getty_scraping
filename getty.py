import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import urllib.request
import time
import os
import sys
import argparse
from datetime import datetime

from progress.bar import Bar
import math
import fileinput
import gettyboards
import gettyvideos
import gettyimages

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
#chrome_options = Options()
#chrome_options.headless = True
#driver = webdriver.Chrome()

parser = argparse.ArgumentParser(description="This is the parser for the getty downloader.")
parser.add_argument("url", help = "Choose an url to scrape ")
parser.add_argument("-d", "--dir", help = "Choose a directory to store images in ")
parser.add_argument("-in", "--image-number",dest="imgs", type = int, help = "Choose how many images you want to download; it must be a positive integer.")
parser.add_argument("-pn",  "--page-number",dest="pages", help = "Choose how many pages of images you want to download; it can be a fractional number. If you have already provided the number of images, the program will use that argument instead of the number of pages. ")

img_sizes = ['2048','1024','612']
parser.add_argument("-s", "--size", choices = img_sizes, help = "Choose an image size to download in. Choices: '2048' for max size of 2048x2048 px, '1024' for max size of 1024x1024 px, and '612' for max size of 612x612 px.")
 
args = parser.parse_args()

path = os.getcwd()+"\downloads"



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

def media_download(url,directory,file_extension, id):
    
    try:

        filename = id + file_extension 

        media_path = os.path.join(path, directory, filename)
      
        urllib.request.urlretrieve(url, media_path) # download image and video

    
    except Exception:
        pass

            
   

        

        
def image_scraper(url,directory,kwargs):
    
    
    if  kwargs["imgs"]:
        img_number = kwargs["imgs"]
        if img_number < 1:
            raise Exception("Sorry, but your number of images cannot be less than or equal to 1.")
        pages = math.ceil(float(img_number)/60)
        pages_string = round(pages,2)
        print(f"Downloading {img_number} images, or ~ {pages} pages in total...\n")
        
    elif kwargs["pages"]:
        pages = float(kwargs["pages"])
        img_number = math.ceil(pages*60)
        if pages <= 0:
            raise Exception("Sorry, but your number of pages cannot be less than or equal to 0.")
        
        print(f"Downloading {pages} pages, or {img_number} images in total...\n")
        pages = math.ceil(pages)
        #Converting to the actual amount used in the iterator
        
    else:
        pages = 1
        img_number = math.ceil(float(pages*60))
        print(f"No number of pages or images specified. Defaulting to downloading 1 page, or {img_number} images in total... \n")
        
    if kwargs["size"]:
        img_size = kwargs["size"]
    else:
        img_size = "2048"
        
    k = 1
    for i in range(pages): 
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') # Scroll to the end of page.
        time.sleep(2) # Wait for all the images to load correctly.
        images = driver.find_elements_by_xpath("//a[contains(@class, 'gallery-mosaic-asset__link')]") # Find all images.
#        print('Scrolled down')
        nextpage = driver.find_element_by_class_name('PaginationRow-module__nextButton___1A4gS')
        driver.execute_script("arguments[0].scrollIntoView()", nextpage)
        print(f"\nDownloading {i+1} out of {pages} pages\n")
#        
    #        
    ##        with Bar('Processing', max=img_number) as bar:
    ##            for i in range(img_number):
    ##                i+=1
    ##                bar.next()


        for image in images: 
            if k <= img_number:
                try:


                    bad_image_url = image.get_attribute('href') # Get the link
                    image_url, id = gettyimages.image_link_cleaner(bad_image_url, size = img_size)


                    media_download(image_url,directory,'.png', id) # And download it to directory
                    print(f"[{k}/{img_number}] Downloaded image {id}")
                    k+=1





                    time.sleep(1)
                except:

                    pass

        try:

            nextpage = driver.find_element_by_class_name('PaginationRow-module__nextButton___1A4gS')
            driver.execute_script("arguments[0].scrollIntoView()", nextpage)
            nextpage.click() # Move to next page
        except:
            pass
        time.sleep(2)
    
    
    
    
def board_scraper(url,directory,kwargs):
    if  kwargs["imgs"]:
        img_number = kwargs["imgs"]
        if img_number < 1:
            raise Exception("Sorry, but your number of images cannot be less than or equal to 1.")
        pages = math.ceil(float(img_number)/100)
        pages_string = round(pages,2)
        print(f"Downloading {img_number} images, or ~ {pages} pages in total...\n")
        
    elif kwargs["pages"]:
        pages = float(kwargs["pages"])
        img_number = math.ceil(pages*100)
        if pages <= 0:
            raise Exception("Sorry, but your number of pages cannot be less than or equal to 0.")
        
        print(f"Downloading {pages} pages, or {img_number} images in total...\n")
        pages = math.ceil(pages)
        #Converting to the actual amount used in the iterator
        
    else:
        pages = 1
        img_number = math.ceil(float(pages*100))
        print(f"No number of pages or images specified. Defaulting to downloading 1 page, or {img_number} videos in total... \n")
        
    if kwargs["size"]:
        img_size = kwargs["size"]
    else:
        img_size = "2048"
        

        
    k = 1
    for i in range(pages): 
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') # Scroll to the end of page.
        time.sleep(2) # Wait for all the images to load correctly.
        images = driver.find_elements_by_xpath("//img[contains(@class, 'board-asset')]") # Find all media assets
#        print(videos)
#        print('Scrolled down')
        nextpage = driver.find_element_by_class_name('next-page')
        driver.execute_script("arguments[0].scrollIntoView()", nextpage)
        print(f"\nDownloading {i+1} out of {pages} pages\n")
#        
    #        
    ##        with Bar('Processing', max=img_number) as bar:
    ##            for i in range(img_number):
    ##                i+=1
    ##                bar.next()


        for image in images: 
            if k <= img_number:
                try:

                    img_url = image.get_attribute('src') # Get the link

                    img_url, id, media_type = gettyboards.board_link_cleaner(img_url, size = img_size)

                    
                    if media_type == "image":
                        file_extension = ".png"
                        
                    elif media_type == "video":
                        file_extension = ".mp4"
                        
                    else:
                        raise Exception(f"Could not identify the media type of asset {id} ")

                    media_download(img_url,directory,file_extension, id) # And download it to directory
                    print(f"[{k}/{img_number}] Downloaded asset {id}")
                    k+=1


                    time.sleep(1)
                except:

                    pass

        try:

            nextpage = driver.find_element_by_class_name('next-page')
            driver.execute_script("arguments[0].scrollIntoView()", nextpage)
            nextpage.click() # Move to next page
        except:
            pass
        time.sleep(2)
    



def video_scraper(url,directory,kwargs):
    if  kwargs["imgs"]:
        vid_number = kwargs["imgs"]
        if vid_number < 1:
            raise Exception("Sorry, but your number of videos cannot be less than or equal to 1.")
        pages = math.ceil(float(vid_number)/80)
        pages_string = round(pages,2)
        print(f"Downloading {vid_number} videos, or ~ {pages} pages in total...\n")
        
    elif kwargs["pages"]:
        pages = float(kwargs["pages"])
        vid_number = math.ceil(pages*80)
        if pages <= 0:
            raise Exception("Sorry, but your number of pages cannot be less than or equal to 0.")
        
        print(f"Downloading {pages} pages, or {vid_number} videos in total...\n")
        pages = math.ceil(pages)
        #Converting to the actual amount used in the iterator
        
    else:
        pages = 1
        vid_number = math.ceil(float(pages*80))
        print(f"No number of pages or videos specified. Defaulting to downloading 1 page, or {vid_number} videos in total... \n")
        

        
    k = 1
    for i in range(pages): 
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') # Scroll to the end of page.
        time.sleep(2) # Wait for all the images to load correctly.
        videos = driver.find_elements_by_xpath("//img[contains(@class, 'gallery-asset__thumb gallery-mosaic-asset__thumb')]") # Find all videos
#        print(videos)
#        print('Scrolled down')
        nextpage = driver.find_element_by_class_name('PaginationRow-module__nextButton___1A4gS')
        driver.execute_script("arguments[0].scrollIntoView()", nextpage)
        print(f"\nDownloading {i+1} out of {pages} pages\n")
#        
    #        
    ##        with Bar('Processing', max=img_number) as bar:
    ##            for i in range(img_number):
    ##                i+=1
    ##                bar.next()


        for video in videos: 
            if k <= vid_number:
                try:

                    vid_url = video.get_attribute('src') # Get the link
                    vid_url, id = gettyvideos.video_link_cleaner(vid_url)



                    media_download(vid_url,directory,".mp4", id) # And download it to directory
                    print(f"[{k}/{vid_number}] Downloaded video {id}")
                    k+=1





                    time.sleep(1)
                except:

                    pass

        try:

            nextpage = driver.find_element_by_class_name('PaginationRow-module__nextButton___1A4gS')
            driver.execute_script("arguments[0].scrollIntoView()", nextpage)
            nextpage.click() # Move to next page
        except:
            pass
        time.sleep(2)
    
    
    
def selenium_head(url,directory,**kwargs):
    #kwarg collector and determines the type of board

    
    if re.search("gettyimages.com/collaboration/boards", url):
        print("\nURL given has been identified as a board. \n")
        board_scraper(url, directory, kwargs)
        
    elif re.search("gettyimages.com/photos/", url):
        print("\nURL given has been identified as an image search. \n")
        image_scraper(url, directory, kwargs)

        
    elif re.search("gettyimages.com/videos", url):
        print("\nURL given has been identified as a video search. \n")
        video_scraper(url, directory, kwargs)

        
    elif re.search("gettyimages.com/search/more-like-this", url):
        print("\nURL given has been identified as a similar images search. \n")
        image_scraper(url, directory, kwargs)
        
    elif re.search("gettyimages.com/search",url):
        print("\nURL given has been identified as a special image search. \n")
        image_scraper(url, directory, kwargs)
        
    else:
        print("\nThe program could not process the URL given. Please check to see if the URL you provided is correct and from a gettyimages.com image search, video search, or board.")


if __name__ == "__main__":

    search_link = args.url

    if args.dir:
            directory = args.dir
    else:
            directory = create_default_directory(search_link)
            

            
    if os.path.exists(os.path.join(path, directory)) == False:
        os.mkdir(os.path.join(path, directory))
    else:
        dirnumber = 0
        while os.path.exists(os.path.join(path, directory, str(dirnumber))) == True:
            dirnumber+=1
            
        newdir = directory+"/"+str(dirnumber)
        os.mkdir(newdir)
        print(f"You already have a directory called '{directory}'. A temporary directory was made at {newdir}")
        directory = newdir
            



driver.get(search_link)
selenium_head(search_link,directory,pages = args.pages, imgs = args.imgs, size = args.size)
print("\nJob is finished")
#driver.close()

        

