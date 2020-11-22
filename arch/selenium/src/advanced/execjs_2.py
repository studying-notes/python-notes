import traceback
import unittest
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class Demo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_scroll(self):
        url = 'http://www.jd.com'
        self.driver.get(url)
        # 将页面的滚动条滑动到页面的最下方
        scroll = "window.scrollTo(100, document.body.scrollHeight);"
        # 将元素滚动到屏幕中间
        scroll_to_center = "document.getElementById('J_cate').scrollIntoView(true);"
        # 将元素滚动到屏幕底部
        scroll_to_bottom = "document.getElementById('J_cate').scrollIntoView(true);"
        # 将页面纵向向下滚动400像素
        scroll_px = "window.scrollBy(0, 400);"
        try:
            self.driver.execute_script(scroll)
            sleep(3)
            self.driver.execute_script(scroll_to_bottom)
            sleep(3)
            self.driver.execute_script(scroll_px)
            sleep(3)
        except WebDriverException:
            print(traceback.print_exc())

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
