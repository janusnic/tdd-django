from django.contrib import admin

from .models import MetaSet, MetaData
from django.utils.translation import ugettext_lazy as _


class MetaDataInline(admin.TabularInline):

    model = MetaData


class MetaSetAdmin(admin.ModelAdmin):

    fields = (('language', 'name'),)
    list_display = ('name', 'language')
    inlines = (MetaDataInline, )
    list_filter = ('language', )
    search_fields = ['metadata__name', 'metadata__content']


class MetaDataAdmin(admin.ModelAdmin):

    list_display = ('name', 'content', 'meta_set')
    list_filter = ('meta_set__name', 'name')
    search_fields = ['content']

admin.site.register(MetaSet, MetaSetAdmin)
admin.site.register(MetaData, MetaDataAdmin)
