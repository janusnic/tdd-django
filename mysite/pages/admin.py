from django.contrib import admin
from django import forms
from .models import Page, Content
from tinymce.widgets import TinyMCE
from pages.language.models import Language
from pages.metadata.models import MetaSet, MetaData
from django.utils.translation import ugettext_lazy as _
from .common.admin_actions import activate, deactivate

    
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



class LanguageAdminForm(forms.ModelForm):
    country_code = forms.RegexField(
        r'^[A-z]{2,3}$',
        label=_('Country code'),
        help_text=_('(US, UK, CZ, SK, ...)'),
        error_messages={
            'invalid': _('2-3 letter combination required (US, UK, CZ, ...)')
        }
    )

    class Meta:
        fields = '__all__'
        model = Language


class LanguageAdmin(admin.ModelAdmin):

    form = LanguageAdminForm
    fields = (('language', 'country_code'), 'flag', 'default', 'active')
    list_display = ('language', 'country_code', 'default', 'active')
    list_filter = ('active',)
    actions = [activate, deactivate]

admin.site.register(Language, LanguageAdmin)



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