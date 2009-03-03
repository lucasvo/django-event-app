def upcoming_events(request):
    return "AAA"
def upcoming_events_by_category(request, slug):
    #return "AAA"
    print slug
    from django.http import HttpResponse
    return HttpResponse('')


def view_event(request, year, month, day, slug):
    return slug
