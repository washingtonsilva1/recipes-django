import os
from selenium import webdriver
from time import sleep


def make_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    if os.environ.get('CHROMEDRIVER_OPTIONS', '').strip():
        for option in os.environ.get('CHROMEDRIVER_OPTIONS').split(','):
            chrome_options.add_argument(option.strip())
    return webdriver.Chrome(options=chrome_options)


if __name__ == '__main__':
    browser = make_chrome_driver()
    browser.get('https://www.google.com.br')
    sleep(5)
    browser.quit()
