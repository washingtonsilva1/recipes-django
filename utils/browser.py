from selenium import webdriver
from time import sleep


def make_chrome_driver(*options):
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)
    return webdriver.Chrome(options=chrome_options)


if __name__ == '__main__':
    browser = make_chrome_driver('--headless')
    browser.get('https://www.google.com.br')
    sleep(5)
    browser.quit()
