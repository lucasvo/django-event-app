from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist

from eventapp.models import Event, Category

SITE_NAME = 'eventapp.com'

class lazy_string(object):
    def __init__(self, function, *args, **kwargs):
        self.function=function
        self.args=args
        self.kwargs=kwargs
        
    def __str__(self):
        if not hasattr(self, 'str'):
            self.str=self.function(*self.args, **self.kwargs)
        return self.str

def lazy_reverse(*args, **kwargs):
    return lazy_string(reverse, *args, **kwargs)



class UpcomingEventsByCategory(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
             raise ObjectDoesNotExist
        return Category.objects.get(slug__exact=bits[0])

    def title(self, obj):
        return _('Events in Category %s' % obj)
    
    def link(self, obj):
        return reverse('eventapp_upcoming_events_by_category', None, () ,{'slug': obj.slug })

    def items(self, obj):
        return Event.objects.filter(categories=obj, is_published=True).order_by('-start')[:5]
class UpcomingEvents(Feed):
    title = "%s Events" % SITE_NAME
    #link = lazy_reverse('eventapp_upcoming_events') 
    #link = _reverse('eventapp_upcoming_events') 
    #link = '/'
    description = _("Upcoming events for %s" % SITE_NAME)

    def __init__(self, *args, **kwargs):
        Feed.__init__(self, *args, **kwargs)
        self.link = reverse('eventapp_upcoming_events') 

    def items(self):
        return Event.objects.filter(is_published=True).order_by('-start')[:5]

