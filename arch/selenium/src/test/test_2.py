import logging
import time
import traceback
import unittest

import ddt

import HTMLTestRunner
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s %(filename)s [line: %(lineno)d] %(levelname)s %(message)s',
    datefmt = '%a, %d %b %Y %H:%M:%S',
    filename = 'report.log',
    filemode = 'w'
)


@ddt.ddt
class Demo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    @ddt.file_data('data_list.json')
    def test_data_driven_by_file(self, value):
        self.driver.get('http://www.baidu.com')
        self.driver.maximize_window()
        test_data, expect_data = tuple(value.strip().split("||"))
        self.driver.implicitly_wait(10)
        start = time.time()
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            self.driver.find_element_by_id('kw').send_keys(test_data)
            self.driver.find_element_by_id('su').click()
            time.sleep(3)
            self.assertTrue(expect_data in self.driver.page_source)
        except NoSuchElementException as e:
            logging.error("查找的页面元素不存在，异常堆栈信息：" + str(traceback.format_exc()))
        else:
            logging.info("搜索{}，期望{}，通过".format(test_data, expect_data))

    def tearDown(self):
        self.driver.quit()



if __name__ == '__main__':
    # unittest.main()
    suite_raw = unittest.TestLoader().loadTestsFromTestCase(Demo)
    suite = unittest.TestSuite(suite_raw)
    runner = HTMLTestRunner.HTMLTestRunner(stream=open('report.html', 'wb'), title='Report Title', description='Report Description')
    runner.run(suite)
