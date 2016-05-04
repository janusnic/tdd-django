# -*- encoding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from pages.language.models import Language

@python_2_unicode_compatible
class MetaSet(models.Model):
    """
    Stores MetaData configurations
    """

    language = models.ForeignKey(Language, verbose_name=_('Language'))
    name = models.CharField(
        _('Name'),
        help_text=_('Name of meta set (for identification).'),
        max_length=200
    )

    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name = _('Meta set')
        verbose_name_plural = _('Meta sets')

@python_2_unicode_compatible
class MetaData(models.Model):
    """
    Stores MetaData item
    """

    meta_set = models.ForeignKey(MetaSet, verbose_name=_('Meta set'))
    name = models.CharField(
        _('Name'),
        help_text=_('Name of meta tag &lt;meta name="THIS NAME" ... &gt;'),
        max_length=200
    )
    content = models.TextField(
        _('Content'),
        help_text=_('Content of meta tag &lt;meta ... content="THIS CONTENT" &gt;'),
        max_length=2000
    )

    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name = _('Meta data')
        verbose_name_plural = _('Meta data')
