# -*- coding: utf-8 -*-
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://google.com/')

body = browser.find_element_by_tag_name('body')
assert 'Google' in body.text
  
print('Hello Google')

browser.quit()