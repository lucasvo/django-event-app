from datetime import datetime

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

try:
    from tagging.fields import TagField
    tagfield_help_text = _('Separate tags with spaces, put quotes around multiple-word tags.')
except ImportError:
    class TagField(models.CharField):
        def __init__(self, **kwargs):
            default_kwargs = {'max_length': 255, 'blank': True}
            default_kwargs.update(kwargs)
            super(TagField, self).__init__(**default_kwargs)
        def get_internal_type(self):
            return 'CharField'
    tagfield_help_text = _('Django-tagging was not found, tags will be treated as plain text.')


# Wether or not to use django-multilingual for event texts
USE_MULTILINGUAL = getattr(settings, 'EVENTAPP_USE_MULTILINGUAL', False) 
if USE_MULTILINGUAL:
    import multilingual


class Category(models.Model):
    """Categories for Events"""
    if USE_MULTILINGUAL:
        class Translation(multilingual.Translation):
            name = models.CharField(max_length=200)
            slug = models.SlugField(null=True, blank=True)
            description = models.TextField(null=True, blank=True)
    else:
        name = models.CharField(max_length=200)
        slug = models.SlugField(null=True, blank=True)
        description = models.TextField(null=True, blank=True)
   
class Event(models.Model):
    """Event Model used to store data for one event.
    TODO: Cover Image?
          Attachements?
          Geocoding of the location
    """

    start = models.DateTimeField(_('Start date and time'), blank=True, null=True)
    end = models.DateTimeField(_('End date and time'), blank=True, null=True)


    rsvp_link = models.URLField(_('RSVP Link'), blank=True, null=True, help_text=_('You can enter a link to a site where people can sign up for the event. Example: meetup.com or facebook.com'))

    # Location:
    location_address_1 = models.CharField(_('Address Line 1'), max_length=100, null=True, blank=True)   
    location_address_2 = models.CharField(_('Address Line 2'), max_length=100, null=True, blank=True)
    location_zip = models.CharField(_('ZIP Code'), max_length=10, null=True, blank=True)
    location_city = models.CharField(_('City'), max_length=30, null=True, blank=True)
    location_province = models.CharField(_('Region/Province/State'), max_length=30, null=True, blank=True)
    location_country = models.CharField(_('Country'), max_length=30, null=True, blank=True)

    categories = models.ManyToManyField(Category)
    tags = TagField()
    

    if USE_MULTILINGUAL:
        class Translation(multilingual.Translation):
            name = models.CharField(max_length=200)
            slug = models.SlugField(null=True, blank=True)
            description = models.TextField(null=True, blank=True)
            location_short_name = models.CharField(max_length=100, blank=True, null=True)
    else:
        name = models.CharField(max_length=200)
        slug = models.SlugField(null=True, blank=True)            
        description = models.TextField(null=True, blank=True)
        location_short_name = models.CharField(max_length=100, blank=True, null=True)
    
    date_created = models.DateTimeField(blank=True, auto_now_add=True)    
    
    

