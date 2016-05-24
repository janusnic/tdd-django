import os
import uuid

from django.conf import settings


def file_allowed(filename):
    """
    Determines whether the given filename is allowed to be uploaded. This is
    based on the extension and the ALLOWED_EXTENSIONS setting.
    """
    filename, ext = split_extension(filename)
    return (ext in settings.ALLOWED_EXTENSIONS)


def split_extension(filename):
    """
    Given a filename, splits out the extension and returns just the filename
    and then just the extension.
    """
    basename, ext = os.path.splitext(filename)
    if ext.startswith('.'):
        ext = ext[1:]
    return basename, ext.lower()


def get_unique_upload_path(instance, filename):
    """
    Gets the upload path for a file. Folder is based on the app_label and
    model_name. File name with path is guaranteed to be unique by using a UUID.
    An example path for a thumbnail in the photos application looks like this:
        photos/thumbnail/bc31d8ba49c149598f83cf6c64eed500.jpg
    """
    filename, ext = split_extension(filename)
    unique = str(uuid.uuid4()).replace('-', '')
    new_filename = '{}.{}'.format(unique, ext)
    app_label = str(instance._meta.app_label.lower())
    model_name = str(instance._meta.model_name.lower())
    return '/'.join([app_label, model_name, new_filename])
