from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import os
import sys

class FunctionalTest(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):   
        dir = os.path.dirname(__file__)
        self.chromedriver_path = os.path.join(dir, 'chromedriver.exe')    
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.is_live_server = True
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()        
        cls.is_live_server = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if not cls.is_live_server:
            super().tearDownClass()
        
    def setUp(self):
        self.browser = webdriver.Chrome(self.chromedriver_path)
        self.browser.implicitly_wait(3)
    
    def tearDown(self):        
        self.browser.quit()

    def check_for_row_in_list_table(self, searched_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(searched_text, [row.text for row in rows])        