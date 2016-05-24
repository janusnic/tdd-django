import tempfile
import re

from PIL import Image, ImageOps

from django.core.files.uploadedfile import SimpleUploadedFile

from utils.uploads import split_extension


class ImageHandler:
    def __init__(self, file_field):
        self.file_field = file_field
        self.name = file_field.name
        self.storage = file_field.storage
        self.pil = self._get_pil_image()
        self.temp = self._get_temp_file()

    def _get_pil_image(self):
        """
        Generate and return a PIL Image instance from the given file_field.
        """
        return Image.open(self.storage.open(self.file_field))

    def _get_temp_file(self):
        """
        Generate and return a temporary file instance with the same extension
        as self.file_field.
        """
        filename, ext = split_extension(self.file_field.name)
        return tempfile.NamedTemporaryFile(suffix='.%s' % ext)

    def parse_size(self, size):
        """
        Converts a size specified as '800x600-fit' to a tuple like (800, 600)
        and a string 'fit'.
        """
        error_msg = 'Size must be specified as 000x000-method such as 800x600-fit.'

        assert len(size.split('-')) == 2, error_msg
        assert len(size.split('-')[0].split('x')) == 2, error_msg

        try:
            width, height, method = size.replace('-', 'x').split('x')
            width, height = int(width), int(height)
        except ValueError:
            raise AssertionError(error_msg)

        assert width > 0 and height > 0, 'Height and width must both be greater than 0.'
        assert method in ('fit', 'thumb'), "Method must be 'fit' or 'thumb'."

        return (width, height), method

    def resize(self, size):
        """
        Create a thumbnail with the given size/method, save it to the temp
        file, and return the data for it.
        """
        size, method = self.parse_size(size)

        if method == 'thumb':
            # Image.thumbnail resizes the image in place
            self.pil.thumbnail(size, Image.ANTIALIAS)
        if method == 'fit':
            # PILImageOps.fit returns an Image instance
            self.pil = ImageOps.fit(self.pil, size, method=Image.ANTIALIAS)
        self.pil.save(self.temp, self.pil.format)
        self.temp.seek(0)
        return self.temp.read()

    def rotate(self, degrees):
        """
        Rotate the image the given degrees, save it to the temp file, and
        return the data for it.
        """
        self.pil = self.pil.rotate(degrees)
        self.pil.save(self.temp, self.pil.format)
        self.temp.seek(0)
        return self.temp.read()

    def save_to_storage(self):
        """
        Save the current file to the field's storage. This will overwrite the
        existing file (if it exists). Actually does a delete then save, since
        Django storage will not overwrite the file.
        """
        self.storage.delete(self.file_field.name)
        self.storage.save(self.file_field.name, self.temp)


def friendly_name(filename):
    """
    Creates a 'friendly' name based on the given filename:
    - Get everything after the last slash
    - Remove the extension
    - Convert slashes, underscores, bracket, pound to space
    - Convert consecutive spaces to just one space
    """
    filename = filename.split('\\')[-1].split('/')[-1]
    filename, ext = split_extension(filename)
    filename = re.sub('[/\\_\[\]#]', ' ', filename)
    filename = re.sub('\s{2,}', ' ', filename)
    return filename.strip()[:200]


def rotate_image(file_field):
    """
    Rotate (clockwise) the file associated with the given file_field.
    Return True if successful.
    """
    handler = ImageHandler(file_field)
    handler.rotate(270)
    handler.save_to_storage()
    return True


def generate_thumbnail(file_field, size):
    """
    Generate a thumbnail from the given file_field and size.
    Returns a SimpleUploadedFile with the same name as the file_field.
    """
    handler = ImageHandler(file_field)
    return SimpleUploadedFile(handler.name, handler.resize(size))
