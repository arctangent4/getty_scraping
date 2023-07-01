import time
from selenium import webdriver
from selenium.webdriver.common.by import By 
import logging
from download import media_download
import re

#GET IMAGE ID TO NAME FILES
def image_link_cleaner(image_link,**kwargs):


    split_link = re.split("/", image_link)
    link_id = split_link[-1]
    link_id = re.sub("\?adppopup=true","",link_id)

    return link_id


    
#IMAGE SCRAPER
def image_scraper(path,driver,directory,pages,media_number,kwargs):
 #ONLY FOR IMAGE SIZE 612x612


   #k tracks the number of total images downloaded
    k = 1
    for i in range(pages): 
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') # Scroll to the end of page.
        time.sleep(2) # Wait for all the images to load correctly.
         
        images = driver.find_elements(By.XPATH, "//img[parent::picture]") # Find all images.

        print(f"\nDownloading {i+1} out of {pages} pages\n")

        #Loop over all elements and download
        for image in images: 
            if k <= media_number:
                try:

                    image_url = image.get_attribute('src') # Get the link
                    img_id = image_link_cleaner(image_url)


                    media_download(path,image_url,directory,'.png', img_id) # And download it to directory
                    print(f"[{k}/{media_number}] Downloaded image {img_id}")
                    k+=1



                    time.sleep(1)
                except Exception as e:
                        logging.error(f"An error occurred in downloading the {k}th image: {str(e)}")

        try:
            # Move to next page
            nextpage = driver.find_element(By.XPATH, "//button[contains(@data-testid, 'pagination-button-next')]")

            #element.scrollTo() is a bit buggy, so we use a more complex solution.
            driver.execute_script(""" 
                                    const elem = arguments[0];
                                    const y_offset = -500;
                                    const target = elem.getBoundingClientRect().top + window.pageYOffset + y_offset;
                                    console.log(target);
                                    window.scrollTo(target,0);

                                    """
                                    , nextpage)
            
            #sometimes a popup that blocks the button appears
            pop_up = driver.find_element(By.CLASS_NAME, "global-notification-banner__close-icon")
            if pop_up:
                pop_up.click()

            time.sleep(1)

            nextpage.click()

        except Exception as e:
            logging.error(f"An error occurred in scrolling: {str(e)}")

        #Take a break after moving to the next page.
        time.sleep(2)




