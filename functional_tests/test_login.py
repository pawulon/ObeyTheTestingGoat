import os
import poplib
import time
import re
from django.core import mail
from .base import FunctionalTest

SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):
    
    def wait_for_email(self, test_email, subject):
        if not self.is_live_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body
        
        subject_line = 'Subject: {}'.format(subject)
        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.gmail.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['EMAIL_PASSWORD'])
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    print(lines)
                    if subject_line in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()
    
    def test_can_get_email_link_to_log_in(self):
        if self.is_live_server:
            test_email = 'prmailsender@gmail.com'
        else:
            test_email = 'pawel@pawel.com'
            
        self.browser.get(self.server_url)
        self.browser.find_element_by_name('email').send_keys(test_email + '\n')
        
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Check your email', body.text)
        
        body = self.wait_for_email(test_email, SUBJECT)
        
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail('Could not find url in email body:\n{}'.format(body))
        url = url_search.group(0)
        self.assertIn(self.server_url, url)
        
        self.browser.get(url)
        
        self.assert_logged_in(email=test_email)
                       
        self.browser.find_element_by_link_text('Log out').click()
        
        self.assert_logged_out(email=test_email)        