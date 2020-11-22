import unittest
from time import sleep

from selenium import webdriver


def high_light_element(driver, element):
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                          element, "background:green; border:2px solid red;")


class Demo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_high_light_element(self):
        self.driver.get('http://www.sogou.com')
        ele = self.driver.find_element_by_id('query')
        high_light_element(self.driver, ele)
        sleep(3)
        ele.send_keys('数学家')
        stb = self.driver.find_element_by_id('stb')
        high_light_element(self.driver, stb)
        sleep(3)
        stb.click()
        sleep(3)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
