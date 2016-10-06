from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import os
import sys

dir = os.path.dirname(__file__)
chromedriver_path = os.path.join(dir, 'chromedriver.exe')

class NewVisitorTest(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()
        
    def setUp(self):
        self.browser = webdriver.Chrome(chromedriver_path)
        self.browser.implicitly_wait(3)
    
    def tearDown(self):        
        self.browser.quit()

    def check_for_row_in_list_table(self, searched_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(searched_text, [row.text for row in rows])
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_url)
        self.assertIn('To-Do', self.browser.title)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')       
        
        self.browser.quit()
        self.browser = webdriver.Chrome(chromedriver_path)
        
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
        
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        
        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, '/lists/.+')
        self.assertNotEqual(second_user_list_url, user_list_url)
        
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)                       
        
    def test_layout_and_styling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)
        