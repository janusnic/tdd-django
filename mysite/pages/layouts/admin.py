# -*- encoding: utf-8 -*-

from django.contrib import admin

from ..common.admin_actions import activate, deactivate
from .models import *

class LayoutsAdmin(admin.ModelAdmin):

    fields = ('template', 'submenu_max_characters', 'active')
    list_display = fields
    actions = [activate, deactivate]

admin.site.register(Template, LayoutsAdmin)