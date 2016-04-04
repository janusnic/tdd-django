from django.contrib import admin
from .models import Category, Product
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category,CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):

    # list_display = ('name', 'updated')
    list_filter = ['updated']
    search_fields = ['name']
    ordering = ['updated']
    readonly_fields = ('created','updated')
    fieldsets = [
                ('Item',             {'fields': [('name','slug'),'category']}),
                ('Date information', {'fields': [('created','updated')], 'classes': ['collapse']}),
                ('Description',      {'fields': ['description']}),
                ('Medias',           {'fields': ['image']}),
                ('Metas',            {'fields': ['status','price','stock']}),
            ]
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = 'updated'

admin.site.register(Product, ProductAdmin)
