from django.contrib import admin
from django import forms
from .models import Page, Content
from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext_lazy as _
from .common.admin_actions import activate, deactivate

from pages.language.admin import *
from pages.metadata.admin import *
from pages.menu.admin import *
from pages.layouts.admin import *
from pages.site.admin import *
    
class PageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'author',
                'parent',
                'publication_date',
                'publication_end_date',
                'last_modification_date',
                'status',
                'template',
                'delegate_to',
                'freeze_date',
                'redirect_to_url',
                'redirect_to',
            )
        }),
    )

    actions = [activate, deactivate]
    

admin.site.register(Page, PageAdmin)

class ContentAdminForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Content
        fields = '__all__'

class ContentAdmin(admin.ModelAdmin):
    
    form = ContentAdminForm

admin.site.register(Content,ContentAdmin)

