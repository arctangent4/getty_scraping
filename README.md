# getty_scraper
An adaptable Getty images and videos scraper using Selenium and Chrome Webdriver. Can scrape from searches or boards.

NOTE: This is just an illustrative example. Use at your own discretion and follow all relevant laws. 

## Installation:
Download files or use git clone https://github.com/arctangent4/light_getty.git

>cd light_getty

>python -m venv virt

>source virt/bin/activate   
or with Git Bash on Windows
>source virt/Scripts/activate

>pip install -r requirements.txt

If you get an error along the lines "error: invalid command 'bdist_wheel' ", uninstall the package that triggered
the error during installation. Then, run "pip install wheel" and reinstall the package.


## Program Details
URL is required, other arguments are optional. At the moment, only 612x612 images are supported due to new changes in how Getty URLS are constructed.
>python getty.py [getty url] -d [storage directory] -in [number of images] -pn [number of pages of images] -s [image size]


Contact or submit a feature request if you notice any bugs.
