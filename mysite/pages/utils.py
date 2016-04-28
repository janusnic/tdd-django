# -*- coding: utf-8 -*-
"""A collection of functions for Page CMS"""

from django.conf import settings as django_settings
from django.utils import timezone

from datetime import datetime


def get_now():
    if django_settings.USE_TZ:
        return datetime.utcnow().replace(tzinfo=timezone.utc)
    else:
        return datetime.now()


