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
# NOT YET SUPPORTED: 
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

    def __unicode__(self):
        return self.name

    def save(self):
        """Auto-populate an empty slug field from the Category name and
        if it conflicts with an existing slug then append a number and try
        saving again.
        """
        import re
        from django.template.defaultfilters import slugify
        
        if not self.slug:
            self.slug = slugify(self.name)  # Where self.name is the field used for 'pre-populate from'
        
        while True:
            try:
                super(Category, self).save()
            # Assuming the IntegrityError is due to a slug fight
            except IntegrityError:
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break

   
class Event(models.Model):
    """Event Model used to store data for one event.
    TODO: Cover Image?
          Attachements?
          Geocoding of the location
    """

    start_date = models.DateTimeField(_('Start date and time'), blank=True, null=True)
    end_date = models.DateTimeField(_('End date and time'), blank=True, null=True)


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
    is_published = models.BooleanField(blank=True, default=True)    

    def __unicode__(self):
        FORMAT = '%H:%M %d/%m/%Y'
        return u"%s (%s - %s)" % (self.name, self.start.strftime(FORMAT),  self.end.strftime(FORMAT))
 
    @models.permalink
    def get_absolute_url(self):
       return ('eventapp_view_event', (), {
            'year': self.start.year,
            'month': '%02d' % self.start.month,
            'day': '%02d' % self.start.day,
            'slug':self.slug
            }
            )

    def save(self):
        """Auto-populate an empty slug field from the Category name and
        if it conflicts with an existing slug then append a number and try
        saving again.
        """
        import re
        from django.template.defaultfilters import slugify
        
        if not self.slug:
            self.slug = slugify(self.name)  # Where self.name is the field used for 'pre-populate from'
        
        while True:
            try:
                super(Event, self).save()
            # Assuming the IntegrityError is due to a slug fight
            except IntegrityError:
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break


