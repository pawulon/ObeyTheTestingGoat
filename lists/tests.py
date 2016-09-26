from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
import re

def remove_csrf_token_from_response(response):
    return re.sub('<input type=\'hidden\' name=\'csrfmiddlewaretoken\'.*/>', '', response)

class HomePageTest(TestCase):
    
    def test_root_url_resolved_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        
        response = home_page(request)
        response = remove_csrf_token_from_response(response.content.decode())        
        
        expected_html = render_to_string('home.html')        
        self.assertEqual(response, expected_html)        
        
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        
        response = home_page(request)
        response = remove_csrf_token_from_response(response.content.decode())
        
        self.assertIn('A new list item', response)
        expected_html = render_to_string('home.html',
                                         {'new_item_text' : 'A new list item'})
        self.assertEqual(response, expected_html)
        