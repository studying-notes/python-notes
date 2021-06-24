import unittest
from time import sleep

import win32con

import win32api
from selenium import webdriver


VK_CODE = {
    'ctrl': 0x11,
    't': 0x54,
    'tab': 0x09,
}


def key_down(key):
    win32api.keybd_event(VK_CODE[key], 0, 0, 0)


def key_up(key):
    win32api.keybd_event(VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)


def simulate_key(first_key, second_key):
    key_down(first_key)
    key_down(second_key)
    key_up(second_key)
    key_up(first_key)


class Demo(unittest.TestCase):

    def setUp(self):
        # self.driver = webdriver.Firefox()
        self.driver = webdriver.Edge()

    def test_new_tab(self):
        sleep(3)
        for i in range(2):
            simulate_key('ctrl', 't')
        sleep(3)
        simulate_key('ctrl', 'tab')
        sleep(1)
        self.driver.get('http://www.sogou.com')
        self.driver.find_element_by_id('query').send_keys('数学家')
        self.driver.find_element_by_id('stb').click()
        sleep(3)
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        self.driver.get('http://www.baidu.com')
        self.driver.find_element_by_id('kw').send_keys('w3cschool')
        self.driver.find_element_by_id('su').click()
        sleep(3)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
