import re
from django.core import mail
from .base import FunctionalTest

TEST_EMAIL = 'pawel@pawel.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):
    
    def test_can_get_email_link_to_log_in(self):
        self.browser.get(self.server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL + '\n')
        
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Check your email', body.text)
        
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail('Could not find url in email body:\n{}'.format(email.body))
        url = url_search.group(0)
        self.assertIn(self.server_url, url)
        
        self.browser.get(url)
        
        self.assert_logged_in(email=TEST_EMAIL)
                       
        self.browser.find_element_by_link_text('Log out').click()
        
        self.assert_logged_out(email=TEST_EMAIL)