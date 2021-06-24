import unittest
from selenium import webdriver
from time import sleep


class GloryRoad(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def testSoGou(self):
        self.driver.get('http://www.sogou.com')
        ele = self.driver.find_element_by_id('query')
        ele.clear()
        ele.send_keys('数学家')
        self.driver.find_element_by_id('stb').click()
        sleep(3)
        assert '顾浩杰' in self.driver.page_source, '页面中不存在该关键词！'

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
