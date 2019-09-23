from django.http import HttpResponse
from django.shortcuts import render
from server.models import Location, Activity
import server.ade_synchro.synchronization as sync
import server.ade_synchro.room as rooms
import arrow


def index(request):
    return HttpResponse('Hello, World!')


def synchronization_view(request):

    try:
        events = sync.get_unamur_events()

        for event in events:
            location_id = rooms.get_event_room(event)
            print('Location id:', location_id)

            begin = arrow.get(event.begin).datetime
            end = arrow.get(event.end).datetime

            activity = Activity(begin=begin, end=end, summary=str(event.description))

            if location_id:
                activity.location_id = location_id

            activity.save()

    except sync.SynchronizationError:
        return HttpResponse('Failed to fetch ADE...')

    return HttpResponse('ADE fetched...')


def location_view(request, name=''):

    if len(name) < 1:
        return HttpResponse(status=404)

    location_name = name.upper()
    location = Location.objects.filter(name=location_name).first()

    if not location:
        return HttpResponse('This location does not exist!', status=200)

    context = {
        'location': location
    }

    return render(request, 'location.html', context)
