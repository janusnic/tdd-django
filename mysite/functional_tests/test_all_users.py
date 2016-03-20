# -*- coding: utf-8 -*-
from selenium import webdriver
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import LiveServerTestCase  
 
class HomeNewVisitorTest(LiveServerTestCase): 
 
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
 
    def tearDown(self):
        self.browser.quit()
 
    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)
 
    def test_home_title(self):
        self.browser.get(self.get_full_url("main"))
        self.assertIn("My Cool Django Site", self.browser.title)
 
    def test_h1_css(self):
        self.browser.get(self.get_full_url("main"))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.value_of_css_property("color"), 
                         "rgba(0, 0, 1, 1)")