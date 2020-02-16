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

    def test_wifi_settings(self):
        # 1. Kliknij "Preference"
        self.driver.find_element_by_accessibility_id("Preference").click()

        # 2. Kliknij "Preference dependencies"
        self.driver.find_element_by_accessibility_id("3. Preference dependencies").click()

        # 3. Jeśli checkbox 'wifi' odznaczony to zaznacz

        # rozwiązanie nr 1
        # is_checked = self.driver.find_element_by_class_name("android.widget.CheckBox").get_attribute("checked")
        # if is_checked == "false":
        #     self.driver.find_element_by_class_name("android.widget.CheckBox").click()
        # self.assertTrue("Checkbox is checked", is_checked == 'true')
        # sleep(3)
        # self.driver.back()

        # rozwiazanie nr 2.1 dla jednego checkboxa:
        # self.driver.find_element_by_android_uiautomator('new UiSelector().checkable(true)').click()
        # self.driver.back()
        # self.driver.find_element_by_accessibility_id("3. Preference dependencies").click()
        # self.driver.find_element_by_android_uiautomator('new UiSelector().checkable(true)').click()

        # rozwiazanie nr 2.2 dla wielu:
        self.checkboxes = self.driver.find_elements_by_android_uiautomator('new UiSelector().checkable(true)')
        print('Liczba checkboxow: ', str(len(self.checkboxes)))

        for el in self.checkboxes:
            el.click()

        sleep(4)

        # 4. Wifi settings jest aktywne, wpisz hasło "1234"
        self.wifi_settings = self.driver.find_element_by_xpath("//*[@text='WiFi settings'][@class='android.widget.TextView']")
        if self.wifi_settings.get_attribute('enabled') == 'true':
            self.wifi_settings_bool = True
        self.assertTrue("Ustawienia wifi sa aktywne", self.wifi_settings_bool)
        self.wifi_settings.click()
        self.password_input = self.driver.find_element_by_id('android:id/edit')
        self.pswd = '1234'
        self.password_input.send_keys(self.pswd)
        self.assertEqual(self.password_input.text, self.pswd)
        self.driver.find_element_by_xpath('//*[@resource-id="android:id/button1"][@text="OK"]').click()

        # 5. Kliknij "back"
        self.driver.back()



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestingMobileApp)
    unittest.TextTestRunner(verbosity=2).run(suite)