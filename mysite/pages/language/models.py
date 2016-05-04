# -*- encoding: utf-8 -*-

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.http import Http404
from pages.common.errors import ConfigurationError
from pages.settings import FLAG_UPLOAD_DIR

IMAGES_DIR = FileSystemStorage(FLAG_UPLOAD_DIR)

@python_2_unicode_compatible
class Language(models.Model):
    """
    Stores single language with optional flag image.
    Country Code will be part of URL in lowercase.
    """
    language = models.CharField(_('Language'), max_length=150, unique=True)
    country_code = models.CharField(
        _('Country code'),
        help_text=_('(US, UK, CZ, SK, ...)'),
        max_length=3,
        unique=True
    )
    flag = models.ImageField(
        _('Flag'),
        help_text=_('Flag image to display on page.'),
        storage=IMAGES_DIR,
        upload_to='languages',
        blank=True
    )
    default = models.BooleanField(
        _('Default'),
        help_text=_('Display as default language?'),
        blank=True
    )
    active = models.BooleanField(_('Active'), blank=True, default=True)

    def __str__(self):
        return self.language

    def save(self, *args, **kwargs):
        """
        override save method to check wheter it is first language.
        and if so, check default to True.
        if not, check if some other language has default set to True.
        if not, do not allow to set it to False.
        """
        if not self.default:
            if not Language.objects.exists():
                self.default = True

        else:
            others = Language.objects.filter(default=True).exclude(id=self.id)

            for other_default in others:
                other_default.default = False
                # call super.save on this, so we don't check all this again
                super(Language, other_default).save(*args, **kwargs)

            self.default = True

        self.country_code = self.country_code.lower()
        super(Language, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        override delete method to check if any other language has default set.
        if not, set language with lowest ID as default.
        """
        super(Language, self).delete(*args, **kwargs)

        if not Language.objects.filter(default=True):
            new_default = Language.objects.all().order_by('id')

            if new_default:
                new_default = new_default[0]
                new_default.default = True
                new_default.save()

    def get_language(self,url_data):
        """
        checks for language in data from url parsing
        @param url_data: dict
        @return Language object
        """
        if not url_data['country_code']:
            language = Language.objects.get(default=True)

            if not language.active:
                raise ConfigurationError('There is no default language active, please activate it in admin')
        else:
            try:
                language = Language.objects.get(country_code=url_data['country_code'])
            except Language.DoesNotExist:
                raise Http404
        return language

    def get_languages(self):
        """
        returns Language QuerySet or ()
        """
        languages = list(Language.objects.filter(active=True))
        
        if len(languages) > 1:
            return languages

        return tuple()

    class Meta:
        
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
