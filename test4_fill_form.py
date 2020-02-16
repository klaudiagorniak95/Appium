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
        desired_caps['app'] = PATH('ContactManager.apk')
        desired_caps['appPackage'] = 'com.example.android.contactmanager'
        desired_caps['appActivity'] = 'com.example.android.contactmanager.ContactManager'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_fill_form(self):
        # 1. Kliknij ADD contact
        self.add_contact_button = self.driver.find_element_by_id('com.example.android.contactmanager:id/addContactButton')
        self.add_contact_button.click()

        # 2. Uzupełnij pole
        self.name = 'Klaudia'
        self.number = '456456456'
        self.mail = 'ania@mail.pl'

        self.name_input = self.driver.find_element_by_id('com.example.android.contactmanager:id/contactNameEditText')
        self.name_input.send_keys(self.name)
        self.contact_phone_input = self.driver.find_element_by_id('com.example.android.contactmanager:id/contactPhoneEditText')
        self.contact_phone_input.send_keys(self.number)
        self.contact_phone_dropdown = self.driver.find_element_by_id('com.example.android.contactmanager:id/contactPhoneTypeSpinner')
        self.contact_phone_dropdown.click()
        self.driver.find_element_by_xpath('//android.widget.CheckedTextView[@text="Mobile"]').click()
        self.contact_email_input = self.driver.find_element_by_id('com.example.android.contactmanager:id/contactEmailEditText')
        self.contact_email_input.send_keys(self.mail)
        self.contact_email_dropdown = self.driver.find_element_by_id('com.example.android.contactmanager:id/contactEmailTypeSpinner')
        self.contact_email_dropdown.click()
        self.driver.find_element_by_xpath('//android.widget.CheckedTextView[@text="Work"]').click()
        sleep(3)

        # 3. Sprawdź asercje
        self.inputs = [self.name_input.text, self.contact_phone_input.text, self.contact_email_input.text]
        self.assertEqual(self.inputs, [self.name, self.number, self.mail])
        self.driver.find_element_by_id('com.example.android.contactmanager:id/contactSaveButton')

        # 4. Wyjdź z apki
        self.driver.close_app()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestingMobileApp)
    unittest.TextTestRunner(verbosity=2).run(suite)