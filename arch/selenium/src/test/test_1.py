import logging
import time
import traceback
import unittest

import ddt

from report_template import generate_html
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

    @classmethod
    def setUpClass(cls):
        Demo.tr_string = ""

    def setUp(self):
        self.driver = webdriver.Firefox()
        status = None
        flag = 0

    @ddt.file_data('data_list.json')
    def test_data_driven_by_file(self, value):
        flag_dict = {
            0: 'red',
            1: '#00AC4E'
        }
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
            status = 'fail'
            flag = 0
        else:
            logging.info("搜索{}，期望{}，通过".format(test_data, expect_data))
            status = 'pass'
            flag = 1

        waste_time = time.time() - start - 3
        Demo.tr_string += '''
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%.2f</td>
            <td style="color: %s">%s</td>
        </tr>
        <br/>''' % (test_data, expect_data, start_time, waste_time, flag_dict[flag], status)

    def tearDown(self):
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        generate_html(Demo.tr_string)


if __name__ == '__main__':
    unittest.main()
