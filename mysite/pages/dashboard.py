# -*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class PagesDashboard(Dashboard):
    """
    Custom index dashboard for Django-pages
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(
            modules.ModelList(
                _('General'),
                column=1,
                collapsible=True,
                models=(
                    
                    'pages.language.models.*',
                    'pages.menu.models.*',
                    'pages.layouts.models.*',
                    'pages.site.models.*',
                ),
            )
        )

        self.children.append(
            modules.ModelList(
                _('Pages'),
                column=1,
                collapsible=True,
                models=('pages.models.*', )
            )
        )

        self.children.append(
            modules.ModelList(
                _('Polls'),
                column=1,
                collapsible=True,
                models=('polls.models.*', )
            )
        )

        self.children.append(
            modules.ModelList(
                _('SEO'),
                column=2,
                collapsible=True,
                models=('pages.metadata.models.*', )
            )
        )


        self.children.append(
            modules.AppList(
                _('Administration'),
                column=1,
                collapsible=False,
                models=('django.contrib.*', )
            )
        )

        self.children.append(modules.LinkList(
            _('File Management'),
            column=3,
            children=[
                {
                    'title': _('File Browser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))

        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))
