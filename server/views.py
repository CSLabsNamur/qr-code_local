from django.shortcuts import render
from django.http import HttpResponse
import server.ade_synchro.synchronization as sync
import server.ade_synchro.local as local


def index(request):
    return HttpResponse('Hello, World!')


def synchronization(request):

    try:
        events = sync.get_unamur_events()

        for event in events:
            location_id = local.get_event_local(event)

    except sync.SynchronizationError:
        return HttpResponse('Failed to fetch ADE...')

    return HttpResponse('ADE fetched...')
