from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.dates import MONTHS

from utils.uploads import get_unique_upload_path
from .utils import generate_thumbnail

MONTH_CHOICES = [(key, value) for key, value in MONTHS.items()]

YEAR_CHOICES = [(year, year) for year in
                range(1950, (datetime.now().year + 1))]


class Location(models.Model):
    """A location is a physical location that can be applied to an album."""

    name = models.CharField(_('name'), max_length=200)

    class Meta:
        ordering = ['name', ]
        verbose_name = _('location')
        verbose_name_plural = _('locations')

    @models.permalink
    def get_absolute_url(self):
        return ('location', [str(self.id)])

    def __str__(self):
        return self.name

    @property
    def cover_photo(self):
        """
        Returns the cover photo for this person, which for now is just the
        first photo from the first album based on whatever ordering is the
        default.
        """
        if self.album_set.count():
            return self.album_set.first().photo_set.first()


class Person(models.Model):
    """A person is an actual person that can be tagged in photos."""

    name = models.CharField(_('name'), max_length=200)

    class Meta:
        ordering = ['name', ]
        verbose_name = _('person')
        verbose_name_plural = _('people')

    @models.permalink
    def get_absolute_url(self):
        return ('person', [str(self.id)])

    def __str__(self):
        return self.name

    @property
    def cover_photo(self):
        """
        Returns the cover photo for this person, which for now is just the
        first photo based on whatever ordering is the default.
        """
        return self.photo_set.first()


class Album(models.Model):
    """
    An album is a collection of photos. It belongs to a location and can also
    have a month and a year associated with it.
    """

    name = models.CharField(_('name'), max_length=200)
    month = models.PositiveSmallIntegerField(
        _('month'), null=True, blank=True, choices=MONTH_CHOICES)
    year = models.PositiveSmallIntegerField(
        _('year'), null=True, blank=True, choices=YEAR_CHOICES)

    location = models.ForeignKey(
        Location, null=True, blank=True,
        verbose_name=_('location'), on_delete=models.SET_NULL)

    class Meta:
        ordering = ['name', ]
        verbose_name = _('album')
        verbose_name_plural = _('albums')

    @models.permalink
    def get_absolute_url(self):
        return ('album', [str(self.id)])

    def __str__(self):
        return self.name

    @property
    def cover_photo(self):
        """
        Returns the cover photo for this album, which for now is just the
        first photo based on whatever ordering is the default.
        """
        return self.photo_set.first()

    def get_date_display(self):
        """
        Returns a pretty display of the month and year in one of the formats:
        - 'January 2014'
        - 'January'
        - '2014'
        """
        month = self.get_month_display() or ''
        year = self.get_year_display() or ''
        return '{} {}'.format(month, year).strip()


class Photo(models.Model):
    """
    A photo is just that - a single photo. It can belong to only one album.
    """

    name = models.CharField(_('name'), max_length=200, null=True, blank=True)
    file = models.ImageField(_('file'), upload_to=get_unique_upload_path)

    album = models.ForeignKey(Album, verbose_name=_('album'))
    people = models.ManyToManyField(
        Person, blank=True, verbose_name=_('people'))

    # exif_make = models.CharField(max_length=100, null=True, blank=True)
    # exif_model = models.CharField(max_length=100, null=True, blank=True)
    # exif_iso = models.PositiveSmallIntegerField(null=True, blank=True)
    # exif_focal = models.PositiveSmallIntegerField(null=True, blank=True)
    # exif_exposure = models.CharField(max_length=100, null=True, blank=True)
    # exif_fnumber = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['name', ]
        verbose_name = _('photo')
        verbose_name_plural = _('photos')

    @models.permalink
    def get_absolute_url(self):
        return ('photo', [str(self.id)])

    def __str__(self):
        return self.name

    def thumbnail(self, size):
        """
        Generate and return a thumbnail with the given size. Only do this once
        in this instance to save on hits to the Thumnail model.
        """
        prop_name = '_thumb_%s' % size.replace('-', '_')
        instance, created = self.thumbnail_set.get_or_create(size=size)
        if not hasattr(self, prop_name):
            setattr(self, prop_name, instance.file)
        return getattr(self, prop_name)

    @property
    def file_thumb(self):
        """
        Shortcut to generate a '200x200-fit' thumbnail. Useful in templates.
        """
        return self.thumbnail('200x200-fit')

    @property
    def file_medium(self):
        """
        Shortcut to generate a '1024x768-thumb' thumbnail. Useful in templates.
        """
        return self.thumbnail('1024x768-thumb')


class Thumbnail(models.Model):
    """
    A thumbnail is a smaller resolution size of a photo. It knows how to
    generate itself once it has a size and a photo associated to it.
    """

    size = models.CharField(_('size'), max_length=20, db_index=True)
    file = models.ImageField(_('file'), upload_to=get_unique_upload_path)
    photo = models.ForeignKey(Photo, verbose_name=_('photo'))

    class Meta:
        ordering = ['photo', 'size', ]
        unique_together = ('photo', 'size', )
        verbose_name = _('thumbnail')
        verbose_name_plural = _('thumbnails')

    def __str__(self):
        return '%s (%s)' % (self.photo, self.size)

    def save(self, **kwargs):
        """
        If we have a photo and a size, generate a thumbnail before saving.
        """
        if self.photo and self.size:
            self.generate()
        super().save(**kwargs)

    def generate(self):
        """
        Generate the thumbnail. This happens regardless of whether we already
        have one generated. The new one will overwrite the existing one (while
        keeping the same filename).
        """
        self.file = generate_thumbnail(self.photo.file, self.size)
