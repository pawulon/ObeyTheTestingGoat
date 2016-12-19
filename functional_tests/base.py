from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import os
import sys
from .server_tools import reset_database

class FunctionalTest(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):   
        dir = os.path.dirname(__file__)
        
        if os.name == 'posix':                  # on linux
            chromedriver_name = 'chromedriver'
        else:                                   # on windows
            chromedriver_name = 'chromedriver.exe'
            
        cls.chromedriver_path = os.path.join(dir, chromedriver_name)    
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.is_live_server = True
                cls.server_host = arg.split('=')[1]
                cls.server_url = 'http://' + cls.server_host
                return
        super().setUpClass()        
        cls.is_live_server = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if not cls.is_live_server:
            super().tearDownClass()
        
    def setUp(self):
        if self.is_live_server:
            reset_database(self.server_host)
        self.browser = webdriver.Chrome(self.chromedriver_path)
        self.browser.implicitly_wait(3)
    
    def tearDown(self):        
        self.browser.quit()
    
    def restart_browser(self):
        self.tearDown()
        self.setUp()
    
    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')
        
    def check_for_row_in_list_table(self, searched_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(searched_text, [row.text for row in rows])        
        
    def assert_logged_in(self, email):
        self.browser.find_elements_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)
        
    def assert_logged_out(self, email):
        self.browser.find_elements_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)        