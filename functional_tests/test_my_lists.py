from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


class MyListsTest(FunctionalTest):
    
    def create_pre_authenticated_session(self, email):
        if self.is_live_server:
            session_key = create_session_on_server(self.server_host, email)
        else:
            session_key = create_pre_authenticated_session(email)
        
        self.browser.get(self.server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(name=settings.SESSION_COOKIE_NAME,
                                     value=session_key,
                                     path='/',))
                                     
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'pawel@pawel.com'
        self.create_pre_authenticated_session(email)
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Reticulate splines\n')
        self.get_item_input_box().send_keys('Immanetize eschaton\n')
        first_list_url = self.browser.current_url
        
        self.browser.find_element_by_link_text('My lists').click()        
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )
        
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Click cows\n')
        second_list_url = self.browser.current_url
        
        self.browser.find_element_by_link_text('My lists').click()
        self.browser.find_element_by_link_text('Click cows').click()
        self.assertEqual(self.browser.current_url, second_list_url)
        
        self.browser.find_element_by_link_text('Log out').click()
        self.assertEqual(self.browser.find_elements_by_link_text('My lists'), [])