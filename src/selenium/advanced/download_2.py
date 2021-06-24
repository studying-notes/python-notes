import unittest
from time import sleep

from selenium import webdriver


class Demo(unittest.TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": "F:\\360Downloads"}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=chrome_options)

    def test_download(self):
        self.driver.get(
            "http://sw.bos.baidu.com/sw-search-sp/software/96ef512539181/QQ_9.0.1.23161_setup.exe")
        sleep(100)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
