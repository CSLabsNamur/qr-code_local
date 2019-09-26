import arrow
import server.ade_synchro.room as rooms
from server.models import Activity


def save_activities(events):
    """ Save the activities in the database

    :param events: The events from the ADE (Set[ics.Event])
    """

    # higher is the bulk size, better are the performances, but higher is the memory usage
    activities_bulk_max_size = 100
    activities_bulk = []
    activities_number = 0

    print('Save activities from the ADE...')

    for event in events:
        location_id = rooms.get_event_room(event)

        begin = arrow.get(event.begin).datetime
        end = arrow.get(event.end).datetime

        activity = Activity(begin=begin, end=end, summary=event.description)

        print('===== Add activity')
        print('-- (%s) to (%s)' % (begin, end))

        if location_id:
            activity.location_id = location_id
            print('-- location id (%s)' % location_id)

        activities_bulk.append(activity)
        activities_number += 1

        if activities_number > activities_bulk_max_size:
            Activity.objects.bulk_create(activities_bulk)
            activities_bulk = []
            activities_number = 0

    print('... done')


def flush_activities():
    """ Flush the activities in the database
    """
    print('Remove old activities...')
    Activity.objects.all().delete()
    print('... done')
