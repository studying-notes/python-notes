import logging
import traceback
import unittest
from time import sleep

import ddt

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s [line: %(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='report.log',
    filemode='w'
)


@ddt.ddt
class Demo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    @ddt.data(
        ["神奇动物在哪里", "叶茨"],
        ["疯狂动物城", "古德温"],
        ["大话西游之月光宝盒", "周星驰"],
    )
    @ddt.unpack
    def test_data_driven_by_obj(self, test_data, expect_data):
        self.driver.get('http://www.baidu.com')
        self.driver.implicitly_wait(10)
        try:
            self.driver.find_element_by_id('kw').send_keys(test_data)
            self.driver.find_element_by_id('su').click()
            sleep(3)
            self.assertTrue(expect_data in self.driver.page_source)
        except NoSuchElementException as e:
            logging.error("查找的页面元素不存在，异常堆栈信息：" + str(traceback.format_exc()))
        else:
            logging.info("搜索{}，期望{}，通过".format(test_data, expect_data))

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
