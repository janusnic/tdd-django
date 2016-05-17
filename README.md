# tdd-django unit_17

Кэширование на уровне представлений
===================================
        django.views.decorators.cache.cache_page()
Более детальный способ использования системы кэширования возможен за счет кэширования вывода отдельных представлений. Модуль django.views.decorators.cache определяет декоратор cache_page, который автоматически кэширует вывод представления. Использовать его несложно:

        from django.views.decorators.cache import cache_page

        @cache_page(60 * 15)
        def my_view(request):
            ...
Декоратор cache_page принимает единственный аргумента: длительность кэширования, в секундах. В предыдущем примере, результат представления my_view() будет закэширован на 15 минут. ( 60 * 15 будет вычислено в 900, т.е. 15 минут умножается на 60 секунд в минуте.)

Кэш уровня представления, аналогично кэшу уровня сайта, использует ключи на основе URL. Если несколько URL указывают на одно представление, каждый URL будет закэширован отдельно.

        urlpatterns = [
            url(r'^foo/([0-9]{1,2})/$', my_view),
        ]
запросы к /foo/1/ и /foo/23/ будут закэшированы отдельно. Но как только определённый URL (например, /foo/23/) будет запрошен, следующие запросы к этому URL будут использовать кэш.

Декоратор cache_page также может принимать необязательный именованный аргумент, cache, который указывает декоратору использовать определённый кэш (из списка параметра конфигурации CACHES) для кэширования результатов. По умолчанию используется кэш default, но вы можете указать любой:

        @cache_page(60 * 15, cache="special_cache")
        def my_view(request):
            ...
Также вы можете переопределять префикс кэша на уровне представления. Декоратор cache_page принимает необязательный именованный аргумент key_prefix, который работает аналогично параметру конфигурации CACHE_MIDDLEWARE_KEY_PREFIX для мидлвари. Он может быть использован следующим образом:

        @cache_page(60 * 15, key_prefix="site1")
        def my_view(request):
            ...
Аргументы key_prefix и cache можно указать вместе. Аргумент key_prefix и параметр KEY_PREFIX настройки CACHES будут объединены.

pages/views.py
--------------

        from django.views.decorators.cache import cache_page

        @cache_page(10)
        def main_view(request, url, preview=False):

parse_url
---------

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


pages/views.py
--------------

            url_result = parse_url(url)

site/__init__.py/get_site
-------------------------
        # -*- encoding: utf-8 -*-

        from ..common.errors import ConfigurationError
        from .models import Site, Script


        def get_site():
            """
            checks for site with pk=1

            @return Site object
            @raises ConfigurationError
            """
            try:
                site = Site.objects.get(pk=1)
                return site

            except Site.DoesNotExist:
                raise ConfigurationError('There are no Site\'s, please create one in admin')

            except Site.MultipleObjectsReturned:
                raise ConfigurationError('There is more than one site, please make sure there is exactly one, this feature may be changed in future')


        def get_scripts():
            """
            Returns all scripts from DB
            """
            return Script.objects.all()

pages/views.py
--------------

        from .site import get_site, get_scripts

                    current_site = get_site()

language/__init__.py/get_language
---------------------------------

        from django.http import Http404

        from ..common.errors import ConfigurationError
        from .models import Language


        def get_language(url_data):
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

pages/views.py
--------------

        from .language import get_language, get_languages

            language = get_language(url_result)

.layouts import get_template
----------------------------

            from django.core.cache import caches

            from .models import Template


            def get_template():
                """
                Returns current active template
                If there is none user-defined template, return 'default'

                @return (string, int)
                """
                try:
                    cache = caches['default']

                    if not cache.get('template'):
                        template = Template.objects.get(active=True)
                        current_template = (template.template, template.submenu_max_characters)
                        cache.set('template', current_template, 30)

                    else:
                        current_template = cache.get('template')

                except Template.DoesNotExist:
                    current_template = ('default', 150)

                return current_template

pages/views.py
--------------

        from .layouts import get_template
                    # sets tuple (template_name, posts_on_page)
                    current_template = get_template()
get_index_page
--------------
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

get_page
--------
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



    if not url_result['page']:
        page = get_index_page(language)

    else:
        page = get_page(url_result['page'], language, preview)

menu/__init__.py/get_main_menuitems
-----------------------------------
        from .models import Menu
        from functools import cmp_to_key

        def get_main_menuitems(current_page_url, page, preview=False):
            """
            Returns menuitem set for specified page
            if preview = True, it displays non-active menuitems
            """
            menuitems_orig = page.link.lang.menuitem_set
            menuitems = menuitems_orig.order_by('position').filter(menu__id=1)

            # filter active pages if we're not previewing
            if not preview:
                menuitems = menuitems.filter(page__status=1)

            # build a list with menuitems, querysets can't be extended
            new_menuitems = []
            for menuitem in menuitems:
                menuitem.current = menuitem.is_current(current_page_url)
                new_menuitems.append(menuitem)

            new_menuitems.extend(
                menuitems_orig.order_by('position').filter(
                    url__icontains='http://', menu__id=1
                )
            )

            return sorted(new_menuitems, key=cmp_to_key(lambda x, y: cmp(x.position, y.position)))

pages/views.py
--------------

        from .menu import get_main_menuitems, has_other_menu, get_other_menuitems

            menuitems = get_main_menuitems(url_result['page'], page, preview)
    
.metadata import get_metadata
-----------------------------
        def get_metadata(page):
            """
            returns metadata for page

            @param page: Page object
            @return MetaData QuerySet
            """
            if page.metadata_set:
                return page.metadata_set.metadata_set.all()

            return None


pages/views.py
--------------
        from .metadata import get_metadata
            meta_data = get_metadata(page)


Paginator
---------

        from django.core.paginator import Paginator, EmptyPage
                    page_num = url_result['page_num'] or 1

                    if url_result['post']:
                        posts = get_post(page, url_result['post'], preview)
                        template_page = 'post.html'

                    else:
                        posts = get_paginated_posts(page, page_num, page.items_per_menu)
                        template_page = 'page.html'

site_content
------------
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

template
--------
    template = '{}/{}'.format(current_template[0], template_page)

    return render_to_response(
        template,
        {'site_content': site_content},
        RequestContext(request)
    )

post.html
---------
            {% extends 'default/base.html'%}
            {% block title %}
            {{ block.super }}, {{ site_content.posts.title }}
            {% endblock %}
            {% block content %}
                <div id="content" class="clearfix"><!-- #content start -->
                    <div id="main" role="main" class="clearfix"><!-- #main start -->
                        <article class="post" role="article" itemscope="" itemtype="http://schema.org/BlogPosting"><!-- .post start -->
                <header><!-- header start -->
                <h2 class="page-title" itemprop="headline">
                    {{ site_content.posts.title }}
                </h2>
                </header><!-- header end -->
                <section class="post-content clearfix" itemprop="articleBody"><!-- .post-content start -->
                            {{ site_content.posts.body|safe }}
                </section><!-- .post-content end -->
                </article><!-- .post end -->
                <br />
                <!-- g+ button -->
                <link rel="cannonical" href="{{ site_content.posts.get_url }}">
                <div class="g-plusone" data-size="medium" data-annotation="inline" data-width="32"></div>
                <!-- g+ end -->
                {% include 'default/comments.html' %}
                </div><!-- #main end -->
                </div><!-- .content end -->
                <!-- google plus button -->
                <script type="text/javascript">
                    (function() {
                        var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
                        po.src = 'https://apis.google.com/js/plusone.js';
                        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
                     })();
                 </script>
            {% endblock %}


page.html
---------
            {% extends 'default/base.html'%}
            {% block content %}
                <div id="content" class="clearfix"><!-- #content start -->
                    <div id="main" role="main" class="clearfix"><!-- #main start -->
                        <article class="post" role="article" itemscope="" itemtype="http://schema.org/BlogPosting"><!-- .post start -->
                        <header><!-- header start -->
                        <h2 class="page-title" itemprop="headline">
                            {{ site_content.page.title }}
                        </h2>
                        </header><!-- header end -->

                {% include 'default/post_list.html' %}    
                </article><!-- .post end -->
                </div><!-- #main end -->
                </div><!-- .content end -->
            {% endblock %}


default/post_list.html
----------------------

        <section class="post-content clearfix" itemprop="articleBody"><!-- .post-content start -->
            {{ site_content.page.content|safe }}
            {% for post in site_content.posts.object_list %}
            <div class="page_post">
                <div id="{{ post.title|slugify }}" class="page_post_title">
                    <a href="{{ post.get_url }}">
                        {{ post.title }}
                    </a>
                </div>
                <div class="page_post_content">
                    {{ post.content|safe }}
                </div>
                {% if post.comments %}
                <div class="page_post_comments">
                    <a href='{{ post.get_url }}#comments'>
                        {{ post.comment_set.count }} comments
                    </a>
                </div>
                {% endif %}
            </div>
            {% endfor %}
            {% if site_content.posts.has_other_pages %}
                <div id="pagination">
                    {% for page in site_content.posts.paginator.page_range %}
                    <a class="pagination_page
                        {% if site_content.posts.number == page %}
                            page_active
                        {% endif %}
                        " href="/pages/{{ site_content.current_language.country_code }}/{{ site_content.page.link.url }}~{{ page }}">
                         <span>{{ page }}</span></a>
                     {% endfor %}
                <span id="pagination_all">{{ site_content.posts }}</span>
                </div>
            {% endif %}
            </section><!-- .post-content end -->

base.html
---------
        <!DOCTYPE html>
        <!--[if IEMobile 7]><html class="no-js iem7 oldie"><![endif]-->
        <!--[if lt IE 7]><html class="no-js ie6 oldie" lang="en"><![endif]-->
        <!--[if (IE 7)&!(IEMobile)]><html class="no-js ie7 oldie" lang="en"><![endif]-->
        <!--[if (IE 8)&!(IEMobile)]><html class="no-js ie8 oldie" lang="en"><![endif]-->
        <!--[if gt IE 8]><!-->
        <html><!--<![endif]--><!--[if (gte IE 9)|(gt IEMobile 7)]><!--><!--<![endif]--><head>
        <meta http-equiv="Content-type" content="text/html; charset=UTF-8">
        {% include 'default/base_metadata.html' %}
        {% include 'default/base_title.html'%}
            <meta name="HandheldFriendly" content="True">
            <meta name="MobileOptimized" content="320">
            <meta name="viewport" content="width=device-width, target-densitydpi=160dpi, initial-scale=1.0">
        {% include 'default/base_static.html' %}    
        </head>
        <body class="clearfix">
                {% include 'default/base_header.html' %}
            {% block content %}    
            {% endblock %}
            <footer role="contentinfo" class="clearfix" id="footer"><!-- #footer start -->
                <div id="inner-footer" class="clearfix"><!-- #inner-footer start -->
                    {{ site_content.site.footer|safe }}
                </div><!-- #inner-footer end -->
            </footer><!-- #footer end -->
            <!-- Scripts -->
            {% for script in site_content.scripts %}
                <!-- {{ script.name }} --> 
                {{ script.code|safe }}
            {% endfor %}
            <!-- end scripts -->
        </body></html>

default/base_metadata.html
--------------------------
        {% for meta in site_content.metadata %}

            <meta name="{{ meta.name }}" content="{{ meta.content }}">

        {% endfor %}

default/base_title.html
-----------------------
        <title>{% block title %}{{ site_content.site.display_name }} - {{ site_content.page.title }}{% endblock %}</title>

default/base_static.html
------------------------
        {% load static %}
        <!-- Load CSS -->
            <link rel="stylesheet" type="text/css" href="{% static 'css/default/style_default.css' %}">
            <!-- Load JS -->

default/base_header.html
------------------------
            <header role="banner" id="header"><!-- #header start -->
            <div id="inner-header" class="clearfix"><!-- #inner-header start -->
            <div id="search-wrapper">
                {% for lang in site_content.languages %}            
                <a href="/pages/{{ lang.country_code }}/" class="lang_link{% if site_content.current_language == lang %} lang_active{% endif %}">
                    {% if lang.flag %}
                    <img class="lang_flag" src="{{ MEDIA_URL }}{{ lang.flag }}" alt="language_flag_icon">
                    {% endif %}
                    {{ lang.language }}
                </a>
                {% endfor %}
            </div>
            <!-- Site title -->
            <h1>
                <a href="http://{{ site_content.site.domain }}/" title="{{ site_content.site.display_name }}">
                    {{ site_content.site.display_name }}
                </a>
            </h1>
            <!-- Site tagline -->
            <p>{{ site_content.site.tagline }}</p>
                    </div><!-- #inner-header end -->
                    {% include 'default/base_menu.html' %}  
            </header><!-- #header end -->

default/base_menu.html
----------------------
        <!-- navigation -->
                <nav role="navigation" id="navigation" class="clearfix"><!-- #navigation start -->
                <ul class="level-one">
                    {% for menuitem in site_content.menuitems %}
                    <li>
                    <a href="/pages/{{ site_content.current_language.country_code }}/{{ menuitem.url }}" title="{{ menuitem.menuitem_name }}"
                        {% if menuitem.current %}
                        class="current"
                        {% endif %}
                        >
                        {{ menuitem.menuitem_name }}
                    </a>
                    </li>
                    {% endfor %}
                </ul>
        </nav><!-- #navigation end -->


urls.py
-------

        urlpatterns = [
            
            url(r'^$', views.home, name='main'),
            # url(r'^home/', include('home.urls', namespace='home')),
            url(r'', include('social.apps.django_app.urls', namespace='social')),
            url(r'^shop/', include('shop.urls', namespace='shop')),
            url(r'^reviews/', include('reviews.urls', namespace='reviews')),
            url(r'^pages/(?P<url>.*)$', pages_views.main_view),
            url(r'^tinymce/', include('tinymce.urls')),
            url(r'^ckeditor/', include('ckeditor_uploader.urls')),
            url(r'^users/', include('userprofiles.urls', namespace="users")),
            
        ]
