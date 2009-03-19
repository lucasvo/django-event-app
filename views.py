from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from eventapp.models import Event, Category

def upcoming_events(request):
    return render_to_response('cal_base.html', { }, context_instance=RequestContext(request))

def upcoming_events_by_category(request, slug):
    #return "AAA"
    print slug
    return HttpResponse('')

def view_event(request, year, month, day, slug=None):
    context = {}
    event_list = []
    events = Event.objects.filter(start__year=year,start__month=month)
    for event in events:
        if int(day) in range(int(event.start.day),int(event.start.day+(event.end-event.start).days),1):
            event_list.append(event)
    context['events'] = event_list
    context['year'] = year
    context['month'] = month
    context['day'] = day
    return render_to_response('display_events.html',context,context_instance=RequestContext(request))
