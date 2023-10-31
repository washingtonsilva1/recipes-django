import os
from selenium import webdriver


def make_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    options = os.environ.get('CHROMEDRIVER_OPTIONS', '')
    if options:
        for option in options.strip().split(','):
            chrome_options.add_argument(option.strip())
    return webdriver.Chrome(options=chrome_options)
