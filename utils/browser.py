import os
from selenium import webdriver
from utils.utils import parse_str_to_list


def make_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    options = os.environ.get('CHROMEDRIVER_OPTIONS', '')
    for option in parse_str_to_list(options, ','):
        chrome_options.add_argument(option)
    return webdriver.Chrome(options=chrome_options)
