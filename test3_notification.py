# -*- coding: utf-8" - *

import os
import unittest
from appium import webdriver
from time import sleep

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class TestingMobileApp(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '7.0'
        desired_caps['deviceName'] = 'Gigaset GS170'
        desired_caps['app'] = PATH('ApiDemos-debug.apk')
        desired_caps['appPackage'] = 'io.appium.android.apis'
        desired_caps['appActivity'] = 'io.appium.android.apis.ApiDemos'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_notifications(self):
        self.driver.open_notifications()
        sleep(5)

        elements = self.driver.find_elements_by_class_name('android.widget.TextView')


        print("Liczba notyfikacji: "+elements.__len__().__str__())
        title=False
        body=False

        for el in elements:
            #print("element o tresci: "+el.text)
            print("element o tresci")
            print(el)
            if el.text == "USB debugging connected":
                title = True
            elif el.text == "Tap to disable USB debugging.":
                body = True

        self.assertTrue(title)
        self.assertTrue(body)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestingMobileApp)
    unittest.TextTestRunner(verbosity=2).run(suite)