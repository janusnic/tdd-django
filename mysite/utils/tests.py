import json

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory

from utils.uploads import split_extension, file_allowed, get_unique_upload_path


class FakeModel:
    class Meta:
        app_label = 'testing'
        model_name = 'fake_model'

    def __init__(self):
        self._meta = FakeModel.Meta()


class Uploads(TestCase):
    def test_split_extension(self):
        """
        Test that split_extension method works properly.
        """
        scenarios = {
            'awesome_filename.jpg': ['awesome_filename', 'jpg'],
            'path/awesome_filename.GIF': ['path/awesome_filename', 'gif'],
            'path/path/awesome_filename': ['path/path/awesome_filename', ''],
        }
        for input, output in scenarios.items():
            name, ext = split_extension(input)
            self.assertEqual(name, output[0])
            self.assertEqual(ext, output[1])

    def test_file_allowed(self):
        """
        Test that file_allowed method works properly on all ALLOWED_EXTENSIONS
        and does not allow other file types.
        """
        scenarios = {
            'path/awesome_filename.exe': False,
            'path/awesome_filename.dll': False,
            'path/awesome_filename.sh': False,
            'path/awesome_filename': False,
        }
        for ext in settings.ALLOWED_EXTENSIONS:
            scenarios['path/awesome_filename.{}'.format(ext)] = True
        for input, output in scenarios.items():
            result = file_allowed(input)
            self.assertEqual(result, output)

    def test_get_unique_upload_path(self):
        """
        Test that get_unique_upload_path works properly.
        """
        instance = FakeModel()
        filename = get_unique_upload_path(instance, 'image.jpg')
        self.assertEqual(len(filename), 55)
        self.assertEqual(filename[:19], 'testing/fake_model/')
        self.assertEqual(filename[-4:], '.jpg')
