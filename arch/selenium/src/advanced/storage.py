import unittest
from time import sleep

from selenium import webdriver


class Demo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_html5_local_storage(self):
        self.driver.get(
            'http://www.w3school.com.cn/tiy/loadtext.asp?f=html5_webstorage_local')
        sleep(3)
        last_name = self.driver.execute_script("return localStorage.lastname")
        print(last_name)
        self.driver.execute_script("localStorage.clear();")
        last_name = self.driver.execute_script("return localStorage.lastname")
        print(last_name)
        sleep(3)

    def test_html5_session_storage(self):
        self.driver.get(
            'http://www.w3school.com.cn/tiy/loadtext.asp?f=html5_webstorage_session')
        sleep(3)
        self.driver.find_element_by_tag_name('button').click()
        click_count = self.driver.execute_script(
            "return sessionStorage.clickcount")
        print(click_count)
        self.driver.execute_script("sessionStorage.clear();")
        click_count = self.driver.execute_script(
            "return sessionStorage.clickcount")
        sleep(3)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
