from django.test import TestCase

import unittest
from django.test import RequestFactory
from .views import IndexPageView

class IndexPageViewTestCase(unittest.TestCase):
    def test_get(self):
        """IndexPageView.get() sets 'name' in response context."""
        # Setup name.
        name = 'peter'
        # Setup request and view.
        request = RequestFactory().get('/fake-path')
        view = IndexPageView.as_view(template_name='gallery/index.html')
        # Run.
        response = view(request, name=name)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'gallery/index.html')
        self.assertEqual(response.context_data['name'], name)

