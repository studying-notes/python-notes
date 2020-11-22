import traceback
import unittest
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class Demo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_execute_script(self):
        url = 'http://www.baidu.com'
        self.driver.get(url)
        search_box = "document.getElementById('kw').value='python';"
        search_button = "document.getElementById('su').click()"
        try:
            self.driver.execute_script(search_box)
            sleep(3)
            self.driver.execute_script(search_button)
            sleep(3)
            self.assertTrue('python' in self.driver.page_source)
        except WebDriverException:
            print(traceback.print_exc())

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
