# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import *

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'display_name', 'tagline')

class ScriptAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

admin.site.register(Site,SiteAdmin)
admin.site.register(Script,ScriptAdmin)