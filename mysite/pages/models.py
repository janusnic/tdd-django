# -*- coding:utf-8 -*-
"""Django page ``models``."""

from django.db import models
from pages.cache import cache
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings as django_settings
from mptt.models import MPTTModel
from django.utils.text import slugify
from .utils import get_now
from . import settings
import uuid
from .language.models import *
from .metadata.models import *
from .menu.models import *
from .site.models import *
from .layouts.models import *
from .layouts import get_template




@python_2_unicode_compatible
class Page(MPTTModel):
    # some class constants to refer to, e.g. Page.DRAFT
    DRAFT = 0
    PUBLISHED = 1
    EXPIRED = 2
    HIDDEN = 3
    STATUSES = (
        (PUBLISHED, _('Published')),
        (HIDDEN, _('Hidden')),
        (DRAFT, _('Draft')),
    )

    # used to identify pages across different databases
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    link = models.OneToOneField(MenuItem, verbose_name=_('Link'))

    title = models.CharField(_('Page title'), max_length=500)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    page_content = models.TextField(_('Page content'), blank=True)
    index = models.BooleanField(
        _('Index page'),
        help_text=_('This page will be landing page for language specified for link (menu item)'),
        blank=True, default=False
    )

    metadata_set = models.ForeignKey(MetaSet, verbose_name=('Meta set'), null=True, blank=True)

    author = models.ForeignKey(django_settings.AUTH_USER_MODEL,
            verbose_name=_('author'))

    parent = models.ForeignKey('self', null=True, blank=True,
            related_name='children', verbose_name=_('parent'))
    creation_date = models.DateTimeField(_('creation date'), editable=False,
            default=get_now)
    publication_date = models.DateTimeField(_('publication date'),
            null=True, blank=True, help_text=_('''When the page should go
            live. Status must be "Published" for page to go live.'''))
    publication_end_date = models.DateTimeField(_('publication end date'),
            null=True, blank=True, help_text=_('''When to expire the page.
            Leave empty to never expire.'''))

    last_modification_date = models.DateTimeField(_('last modification date'))

    status = models.IntegerField(_('status'), choices=STATUSES, default=DRAFT)
    template = models.CharField(_('template'), max_length=100, null=True,
            blank=True)

    delegate_to = models.CharField(_('delegate to'), max_length=100, null=True,
            blank=True)

    freeze_date = models.DateTimeField(_('freeze date'),
            null=True, blank=True, help_text=_('''Don't publish any content
            after this date.'''))


    redirect_to_url = models.CharField(max_length=200, null=True, blank=True)

    redirect_to = models.ForeignKey('self', null=True, blank=True,
        related_name='redirected_pages')


    class Meta:
        """Make sure the default page ordering is correct."""
        ordering = ['tree_id', 'lft']
        get_latest_by = "publication_date"
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        

    def __init__(self, *args, **kwargs):
        """Instanciate the page object."""
        # per instance cache
        self._languages = None
        self._content_dict = None
        self._is_first_root = None
        self._complete_slug = None
        super(Page, self).__init__(*args, **kwargs)

    def _get_calculated_status(self):
        """Get the calculated status of the page based on
        :attr:`Page.publication_date`,
        :attr:`Page.publication_end_date`,
        and :attr:`Page.status`."""
        if settings.PAGE_SHOW_START_DATE and self.publication_date:
            if self.publication_date > get_now():
                return self.DRAFT

        if settings.PAGE_SHOW_END_DATE and self.publication_end_date:
            if self.publication_end_date < get_now():
                return self.EXPIRED

        return self.status
    _get_calculated_status.short_description = _('Get the calculated status of the page based on :attr: Page.publication_date, :attr: Page.publication_end_date and :attr: Page.status')
    calculated_status = property(_get_calculated_status)

    def save(self, *args, **kwargs):
        """Override the default ``save`` method."""
        if not self.status:
            self.status = self.DRAFT
        # Published pages should always have a publication date
        if self.publication_date is None and self.status == self.PUBLISHED:
            self.publication_date = get_now()
        # Drafts should not, unless they have been set to the future
        if self.status == self.DRAFT:
            if settings.PAGE_SHOW_START_DATE:
                if (self.publication_date and
                        self.publication_date <= get_now()):
                    self.publication_date = None
            else:
                self.publication_date = None
        self.last_modification_date = get_now()
        super(Page, self).save(*args, **kwargs)

    def _visible(self):
        """Return True if the page is visible on the frontend."""
        return self.calculated_status in (self.PUBLISHED, self.HIDDEN)
    visible = property(_visible)

    def __str__(self):
        """Representation of the page, saved or not."""
        if self.id:
            # without ID a slug cannot be retrieved
            return self.title
        return "Page without id"

    def have_posts(self):
        """
        checks if Page has any Posts

        @return bool
        """
        if self.content_set.count():
            return True

        return False

    def get_url(self):
        """
        returns url for this page

        @return string
        """
        url_scheme = '/{country_code}/pages/{link_url}'
        result = url_scheme.format(country_code=self.link.lang.country_code, link_url=self.link.url)

        return result
    
    @property
    def items_per_menu(self):
        """
        Counts the number of items
        in this (sub)menu - makes sure the items
        displayed are lower than template's
        maximum characters in menu.
        It will try to match maximum posiible items
        per all paginated posts but lowest possible value
        is 1.
        """
        template = get_template()
        max_characters = template[1]

        submenu_items = self.content_set.order_by('-creation_date')
        lengths = [len(item.title) for item in submenu_items]

        items = 0
        items_sum = 0
        pages_items = []

        for i in lengths:
            if items_sum < max_characters:
                items_sum += i
                items += 1
            else:
                items_sum = 0
                pages_items.append(items)
                items = 0

        if not pages_items:
            return 1

        return min(pages_items)    


@python_2_unicode_compatible
class Content(models.Model):
    """
    A block of content, tied to a :class:`Page <pages.models.Page>`,
    for a particular language`.
    """
    page = models.ForeignKey(Page, verbose_name=_('Page'))
    title = models.CharField(_('Post title'), max_length=200, unique=True)
    type = models.CharField(_('type'), max_length=100, blank=False,
        db_index=True)
    body = models.TextField(_('Post content'))
    active = models.BooleanField(_('Active'), blank=True, default=True)
    creation_date = models.DateTimeField(_('creation date'), editable=False,
        default=get_now)
    comments = models.BooleanField(_('Enable comments'), blank=True)

    def __str__(self):
        return self.title


    class Meta:
        get_latest_by = 'creation_date'
        verbose_name = _('Content')
        verbose_name_plural = _('Contents')

    def get_url(self):
        """
        creates url for Post

        @return string
        """
        url_scheme = '/pages/{country_code}/{link_url}/~{post_title}'

        title = slugify(self.title)
        result = url_scheme.format(country_code=self.page.link.lang.country_code, link_url=self.page.link.url, post_title=title)

        return result
