from django.contrib import admin

from .models import *

class AigerimAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'photo','price', 'cat', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Aigerim, AigerimAdmin)
admin.site.register(Category, CategoryAdmin)