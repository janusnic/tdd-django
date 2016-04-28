# -*- coding: utf-8 -*-
"""Convenience module that provides default settings for the ``pages``
application when the project ``settings`` module does not contain
the appropriate settings."""
from django.conf import settings

# Show the publication start date field in the admin.  Allows for future dating
# Changing the ``PAGE_SHOW_START_DATE``  from ``True`` to ``False``
# after adding data could cause some weirdness.  If you must do this, you
# should update your database to correct any future dated pages.
PAGE_SHOW_START_DATE = getattr(settings, 'PAGE_SHOW_START_DATE', False)

# Show the publication end date field in the admin, allows for page expiration
# Changing ``PAGE_SHOW_END_DATE`` from ``True`` to ``False`` after adding
# data could cause some weirdness.  If you must do this, you should update
# your database and null any pages with ``publication_end_date`` set.
PAGE_SHOW_END_DATE = getattr(settings, 'PAGE_SHOW_END_DATE', False)