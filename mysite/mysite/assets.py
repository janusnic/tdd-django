from io import StringIO
from os import path
from cssmin import cssmin
from jsmin import jsmin
from scss import Scss

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed

FILE_CACHE = {}


def get_file_content(filename):
    """
    Get the file contents from the cache for the given filename. If it does
    not exist in the cache, then get the contents from disk and cache it.
    """
    # If the filename is in the cache and the file has not changed then
    # grab the content from the cache and return it.
    date_modified = path.getmtime(filename)
    cached_content = FILE_CACHE.get(filename, None)
    if cached_content:
        content = cached_content['content']
        if date_modified <= cached_content['date']:
            return content, False
    # Read the current file and add it to the cache.
    with open(filename, 'r') as f:
        content = f.read()
        FILE_CACHE[filename] = {'date': date_modified, 'content': content, }
        return content, True


class CompileAssetsMiddleware:
    """
    A middleware class to compile and minify CSS files and to minify JS files.
    Depends on CSS_FILES and JS_FILES being set in project settings.
    Processors can be customized by changing them in process_request method.
    This is designed to run only in development, so that when you push your
    project to production, the compiled assets can be served like normal.
    """

    def __init__(self):
        if not settings.DEBUG:
            raise MiddlewareNotUsed('CompileAssetsMiddleware only runs in DEBUG mode.')

    def process_request(self, request):
        self.compile(getattr(settings, 'CSS_FILES', {}), (Scss().compile, cssmin,))
        self.compile(getattr(settings, 'JS_FILES', {}), (jsmin,))

    def compile(self, filedict, processors):
        # The key for filedict is the output file, and the value is a list
        # of files that should contribute to that output file.
        for mainfile, filelist in filedict.items():
            rebuild = False
            output = StringIO()
            # Loop through each file in the set and keep track of whether any
            # of them have changed.
            for filename in filelist:
                content, changed = get_file_content(filename)
                output.write("\n" + content)
                if changed:
                    rebuild = True

            # Only rebuild the main file if some files in the set have changed.
            if rebuild:
                output = output.getvalue()
                # Run each processor against the whole output.
                for func in processors:
                    output = func(output)
                # Then save to the desired output file.
                with open(mainfile, 'w') as f:
                    f.write(output)
