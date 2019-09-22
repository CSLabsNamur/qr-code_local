import re
from server.models import Location


def get_event_local(event):
    """ Get the local of an event

    :postcondition: Create the local in the database if it is not already stored.
    :param event: The ical event that may contain a local (ics.Event)
    :return: The id of the local if it exists, otherwise None
    """

    local_name = get_local_name(event.location)

    if not local_name:
        return None

    local = Location.objects.filter(name=local_name).first()

    if local:
        return local.id

    new_local = Location(name=local_name)
    new_local.save()
    return new_local.id


def get_local_name(text):
    """ Get the name of any local according of any text from an activity

    :precondition: The description may contain at most one name of local
    :param text: Any text in an activity (str)
    :return: The name of the local (str) if there is one, otherwise None
    """

    match = re.search('[i,I][0-9]{2}', text)

    if match:
        span = match.span()
        local_name = text[span[0]:span[1]]
        return local_name.upper()
    else:
        return None
