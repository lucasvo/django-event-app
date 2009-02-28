from django.contrib import admin
from django.conf import settings

# Wether or not to use django-multilingual for event texts
USE_MULTILINGUAL = getattr(settings, 'EVENTAPP_USE_MULTILINGUAL', False) 
if USE_MULTILINGUAL:
    import multilingual

from eventapp.models import Category, Event

if USE_MULTILINGUAL:
    class EventMultilingualAdmin(multilingual.ModelAdmin):
        list_display = ('name','start','end')
        list_filter = ['categories']
    class CategoryMultilingualAdmin(multilingual.ModelAdmin):
        pass
    admin.site.register(Event, EventMultilingualAdmin)
    admin.site.register(Category, CategoryMultilingualAdmin)
else:
    class EventAdmin(admin.ModelAdmin):
        list_display = ('name','start','end')
        list_filter = ['categories']

    admin.site.register(Event, EventAdmin)
    admin.site.register(Category)
