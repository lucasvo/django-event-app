from django.shortcuts import render_to_response, get_object_or_404

from eventapp.models import Event, Category

def upcoming_events(request):
    return "AAA"
def upcoming_events_by_category(request, slug):
    #return "AAA"
    print slug
    from django.http import HttpResponse
    return HttpResponse('')


def view_event(request, year, month, day, slug):
    event = get_object_or_404(Event, start_date__year=year, start_date__month=month, start_date__day=day, slug__exact=slug)
    print event
    return slug
