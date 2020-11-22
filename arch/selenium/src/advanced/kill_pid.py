import os
import unittest

from selenium import webdriver


class Demo(unittest.TestCase):

    def test_kill_windows_process(self):
        firefox = webdriver.Firefox()
        chrome = webdriver.Chrome()

        return_code = os.system("TASKKILL /F /IM firefox.exe")
        if return_code == 0:
            print('OK')

        return_code = os.system("TASKKILL /F /IM chrome.exe")
        if return_code == 0:
            print('OK')


if __name__ == '__main__':
    unittest.main()
