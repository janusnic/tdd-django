# -*- coding: utf-8 -*-
from django.test import TestCase

class HomePageTest(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)

    def test_homepage_request_path(self):
        response = self.client.get('/req')
        request = response.wsgi_request
        self.assertEqual(request.path, '/req')

    def test_homepage_request_scheme(self):
        response = self.client.get('/')
        request = response.wsgi_request
        self.assertEqual(request.scheme, 'http')

    
    def test_homepage_request_path_info(self):
        response = self.client.get('/req/test')
        request = response.wsgi_request
        self.assertEqual(request.path_info, '/req/test')
    
    def test_homepage_request_method(self):
        response = self.client.get('/req')
        request = response.wsgi_request
        self.assertEqual(request.method, 'GET')

    def test_homepage_request_encoding(self):
        response = self.client.get('/req')
        request = response.wsgi_request
        request.encoding = 'utf-8'
        self.assertEqual(request.encoding, 'utf-8')

    
    def test_homepage_response_charset(self):
        response = self.client.get('/req')
        request = response.wsgi_request
        
        self.assertEqual(response.charset, 'utf-8')


    
