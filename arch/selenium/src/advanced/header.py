import unittest
from time import sleep

from selenium import webdriver

iPad = "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
iPhone = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"
Android = "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Mobile Safari/537.36"


class Demo(unittest.TestCase):

    def test_iPad(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('http://www.baidu.com')
        driver.find_element_by_id("kw").send_keys("iPad")
        sleep(3)
        driver.get("about:version")
        sleep(100)
        driver.quit()


if __name__ == '__main__':
    unittest.main()
