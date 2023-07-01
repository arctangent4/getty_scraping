import time
from selenium import webdriver
from selenium.webdriver.common.by import By 
import logging
from download import media_download
import re



def video_link_cleaner(video_link):
    import re
#Video URL does not need a formatting function but link_id is helpful for naming videos. Also useful if Getty's URL conventions change in the future.
    video_link = re.split("\?",video_link)[0]
    link_id = video_link.partition("-id")[2]

    return link_id
 



def video_scraper(path,driver,directory,pages,media_number,kwargs):
        
    k = 1
    for i in range(pages): 
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') # Scroll to the end of page.
        time.sleep(5) # Wait for all the images to load correctly.
        videos = driver.find_elements(By.XPATH, "//video[contains(@data-testid, 'gallery-asset-video')]") # Find all videos
        print(videos)
#        print('Scrolled down')
        nextpage = driver.find_element(By.XPATH, "//button[contains(@data-testid, 'pagination-button-next')]")
        driver.execute_script(""" 
                                const elem = arguments[0];
                                const y_offset = -500;
                                const target = elem.getBoundingClientRect().top + window.pageYOffset + y_offset;
                                console.log(target);
                                window.scrollTo(target,0);

                                """
                                , nextpage)
        
        # driver.execute_script("arguments[0].scrollIntoView()", nextpage)
        print(f"\nDownloading {i+1} out of {pages} pages\n")
        

        for video in videos: 
            print(video)
            if k <= media_number:
                try:

                    vid_url = video.get_attribute('src') # Get the link
                    print(vid_url)
                    vid_url, id = video_link_cleaner(vid_url)
                    print(id)
                    media_download(path,vid_url,directory,".mp4", id) # And download it to directory
                    print(f"[{k}/{media_number}] Downloaded video {id}")
                    k+=1

                    time.sleep(1)

                except Exception as e:
                        logging.error(f"An error occurred in downloading the {k}th video: {str(e)}")

        try:

            # nextpage = driver.find_element(By.XPATH, "//button[contains(@data-testid, 'pagination-button-next')]")
            # driver.execute_script("arguments[0].scrollIntoView()", nextpage)
            pop_up = driver.find_element(By.CLASS_NAME, "global-notification-banner__close-icon")
            if pop_up:
                pop_up.click()
            time.sleep(1)
            nextpage.click() # Move to next page
        except Exception as e:
            logging.error(f"An error occurred in scrolling: {str(e)}")

        time.sleep(2)








    
