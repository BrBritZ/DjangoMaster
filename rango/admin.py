from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile

# Customise the Admin Interface for Page
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

# Customise the Admin Interface for Category
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)