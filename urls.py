from django.conf.urls.defaults import *
from eventapp.feeds import UpcomingEvents, UpcomingEventsByCategory

feeds = {
    'upcoming': UpcomingEvents,
    'category': UpcomingEventsByCategory,
}


urlpatterns = patterns('',
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict':feeds}),
    
    url(r'^upcoming/$', 'eventapp.views.upcoming_events', name='eventapp_upcoming_events'),
    url(r'^category/(?P<slug>[-\w]+)/$', 'eventapp.views.upcoming_events_by_category', name='eventapp_upcoming_events_by_category'),

    #url(r'^(?P/(?P<slug>[-\w]+)/$', 'eventapp.views.upcoming_events', name='eventapp_upcoming_events'),
    url(r'(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'eventapp.views.view_event', name='eventapp_view_event'),
    #url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', dict(info_dict, template_name='blog/list.html')),
    #url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$','archive_day',dict(info_dict,template_name='blog/list.html')),
    #url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$','archive_month', dict(info_dict, template_name='blog/list.html')),
    #url(r'^(?P<year>\d{4})/$','archive_year', dict(info_dict, template_name='blog/list.html')),
    #url(r'^$','archive_index', dict(info_dict, template_name='blog/list.html')),
)
