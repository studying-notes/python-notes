from time import sleep

import win32api
import win32clipboard as w
import win32con
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def set_text(content):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, content)
    w.CloseClipboard()


VK_CODE = {
    'enter': 0x0D,
    'ctrl': 0x11,
    'a': 0x41,
    'v': 0x56,
    'x': 0x58,
}


def key_down(key):
    win32api.keybd_event(VK_CODE[key], 0, 0, 0)


def key_up(key):
    win32api.keybd_event(VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)


driver = webdriver.Chrome()
driver.get(r'html\upload.html')

wait = WebDriverWait(driver, 10, 0.2)
wait.until(ec.element_to_be_clickable((By.ID, 'file')))

set_text(r'radio.html')
driver.find_element_by_id('file').click()
sleep(3)

key_down('ctrl')
key_down('v')
key_up('v')
key_up('ctrl')

sleep(1)
key_down('enter')
key_up('enter')
