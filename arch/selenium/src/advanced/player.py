import unittest
from time import sleep

from selenium import webdriver


class Demo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_new_tab(self):
        self.driver.get(
            'http://www.w3school.com.cn/tiy/loadtext.asp?f=html5_video_simple')
        video_player = self.driver.find_element_by_tag_name('video')
        video_src = self.driver.execute_script(
            "return arguments[0].currentSrc;", video_player)
        video_duration = self.driver.execute_script(
            "return arguments[0].duration;", video_player)
        print(video_duration)
        self.driver.execute_script("return arguments[0].play();", video_player)
        sleep(3)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
