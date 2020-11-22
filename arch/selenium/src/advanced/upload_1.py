from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get(r'upload.html')
file_box = driver.find_element_by_id('file')
file_box.send_keys(r'radio.html')
driver.find_element_by_id('filesubmit').click()
