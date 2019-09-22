from django.shortcuts import render
from django.http import HttpResponse
import server.ade_synchro.synchronization as sync


# Create your views here.
def index(request):
    return HttpResponse('Hello, World!')


def synchronization(request):

    try:
        events = sync.get_unamur_events()

    except sync.SynchronizationError:
        return HttpResponse('Failed to fetch ADE...')

    return HttpResponse('ADE fetched...')
