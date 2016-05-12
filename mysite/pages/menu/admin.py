# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from pages.settings import ADMIN_MEDIA_PREFIX
from .models import *
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.conf.urls import url
from django.utils.html import format_html
class MenuAdmin(admin.ModelAdmin):

    fields = ('name', )
    list_display = ('name', )


class MenuItemAdmin(admin.ModelAdmin):

    fields = (('lang', 'menu', 'menuitem_name'), 'url', 'style')
    list_display = (
        'menuitem_name',
        'lang',
        'menu',
        'url',
        'move',
        'position',
        'style'
    )
    list_filter = ('lang', 'menu')
    prepopulated_fields = {"url": ("menuitem_name",)}

    def move(self, obj):
        """
        Returns html with links to move_up and move_down views.
        """
        button = u'<a href="%s"><img src="%simg/arrow-%s.png" /> %s</a>'
        prefix = ADMIN_MEDIA_PREFIX

        link = '%d/move_up/' % obj.pk
        html = button % (link, prefix, 'up', _('up')) + " | "
        link = '%d/move_down/' % obj.pk
        html += button % (link, prefix, 'down', _('down'))

        return format_html(html)

    def get_urls(self):
        admin_view = self.admin_site.admin_view
        urls = [
            url(r'^(?P<item_pk>\d+)/move_up/$', admin_view(self.move_up)),
            url(r'^(?P<item_pk>\d+)/move_down/$', admin_view(self.move_down)),
        ]

        return urls + super(MenuItemAdmin, self).get_urls()

    def move_up(self, request, item_pk):
        if self.has_change_permission(request):
            item = get_object_or_404(MenuItem, pk=item_pk)
            item.increase_position()

        else:
            raise PermissionDenied

        
        return redirect('/admin/pages/menuitem')

    def move_down(self, request, item_pk):
        if self.has_change_permission(request):
            item = get_object_or_404(MenuItem, pk=item_pk)
            item.decrease_position()

        else:
            raise PermissionDenied

        
        return redirect('/admin/pages/menuitem')


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)