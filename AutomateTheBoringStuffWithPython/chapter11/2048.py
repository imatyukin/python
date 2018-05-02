#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

brower = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
brower.get("https://gabrielecirulli.github.io/2048/")
html_elem = brower.find_element_by_tag_name('html')

time.sleep(2)
while True:
    html_elem.send_keys(Keys.ARROW_UP)
    html_elem.send_keys(Keys.ARROW_RIGHT)
    html_elem.send_keys(Keys.ARROW_DOWN)
    html_elem.send_keys(Keys.ARROW_LEFT)
