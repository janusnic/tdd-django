# -*- encoding: utf-8 -*-

from django.shortcuts import render

import re

from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.text import slugify
from django.views.decorators.cache import cache_page

from .language import get_language, get_languages
from .language.models import Language
from .layouts import get_template
from .menu import get_main_menuitems, has_other_menu, get_other_menuitems
from .metadata import get_metadata

from .models import Page
from .site import get_site, get_scripts

import datetime

from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.utils.text import slugify


from pages.common.errors import ConfigurationError

def get_index_page(language):
    """
    checks for page with index=True and returns it

    @param language: Language object
    @return Page object
    """
    try:
        page = Page.objects.select_related('link', 'metadata_set', 'link__lang').get(index=True, link__lang=language)
        return page

    except Page.DoesNotExist:
        raise ConfigurationError('There is no index Page for this Language, please make sure exactly one Page has index field checked True')

    except Page.MultipleObjectsReturned:
        raise ConfigurationError('There are multiple index Pages for this Language, please make sure only 1 Page has index field checked True')


def get_page(page_url, language, preview=False):
    """
    returns page for specific url

    @param page_url: string
    @param language: Language object
    @return Page object
    """
    try:
        page = Page.objects.select_related('link', 'metadata_set', 'link__lang').get(link__url=page_url, link__lang=language)
        if page.status==1 or preview:
            return page

        else:
            raise Http404

    except Page.DoesNotExist:
        raise Http404


def get_paginated_posts(page, page_num=1, posts_on_page=10):
    """
    returns posts paginated by settings.POSTS_ON_PAGE for page object or ()

    @param page: Page object
    @return Paginator object
    """
    if page.have_posts():
        posts = page.content_set.filter(active=True).order_by('-creation_date')
        #posts_visible = [item for item in posts if item.is_visible(datetime.datetime.now())]
        paginated_posts = Paginator(posts, posts_on_page)

        try:
            return paginated_posts.page(page_num)

        except EmptyPage:
            return paginated_posts.page(paginated_posts.num_pages)

    return tuple()


def get_post(page, post_title, preview=False):
    """
    returns post object or 404

    @param page: Page object
    @param post_title: string
    @return Post object
    """
    for post in page.content_set.all():
        if slugify(post.title) == post_title and (post.active or preview):
            return post

    raise Http404



def parse_url(url):
    """
    parses url format is:
        language/page~pagenum/~post

        example:
            en/my-page-with-something-interresting~5/~post-on-page-5

    @param url: string
    @return dict
    """
    urlpattern = re.compile(
        r"""
        ^                                         # beginning of string
        ((?P<country_code>[A-z]{2,3})/){0,1}      # country_code match - any 2 or 3 chars
        (?P<page>[A-z0-9-._]{4,}){0,1}            # page url
        (~(?P<page_num>\d*)){0,1}                 # ~page number
        (/~(?P<post>[A-z0-9-._]*)){0,1}           # /~post title
        $                                         # end of string
        """,
        re.VERBOSE
    )

    urlmatch = re.match(urlpattern, url)
    if not urlmatch:
        raise Http404

    return urlmatch.groupdict()

@cache_page(10)
def main_view(request, url, preview=False):
    """
    @param request: HTTP request
    @param url: string
    @param preview: boolean
    """
    url_result = parse_url(url)
    current_site = get_site()

    # sets tuple (template_name, posts_on_page)
    current_template = get_template()
    language = get_language(url_result)

    if not url_result['page']:
        page = get_index_page(language)

    else:
        page = get_page(url_result['page'], language, preview)

    menuitems = get_main_menuitems(url_result['page'], page, preview)
    meta_data = get_metadata(page)
    page_num = url_result['page_num'] or 1

    if url_result['post']:
        posts = get_post(page, url_result['post'], preview)
        template_page = 'post.html'
        

    else:
        posts = get_paginated_posts(page, page_num, page.items_per_menu)
        template_page = 'page.html'

    site_content = {'site': current_site,
                    'languages': get_languages(),
                    'current_language': language,
                    'menuitems': menuitems,
                    'page': page,
                    'scripts': get_scripts(),
                    'metadata': meta_data,
                    'posts': posts, }

    if has_other_menu():
        site_content['other_menuitems'] = get_other_menuitems()



    template = '{}/{}'.format(current_template[0], template_page)

    return render_to_response(
        template,
        {'site_content': site_content},
        RequestContext(request)
    )