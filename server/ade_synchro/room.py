import re
from server.models import Location


def get_event_room(event):
    """ Get the room of an event

    :postcondition: Create the room in the database if it is not already stored.
    :param event: The ical event that may contain a room (ics.Event)
    :return: The id of the room if it exists, otherwise None
    """

    room_name = get_room_name(event.location)

    if not room_name:
        return None

    room = Location.objects.filter(name=room_name).first()

    if room:
        return room.id

    new_room = Location(name=room_name)
    new_room.save()
    return new_room.id


def get_room_name(text):
    """ Get the name of any room according of any text from an activity

    :precondition: The description may contain at most one name of room
    :param text: Any text in an activity (str)
    :return: The name of the room (str) if there is one, otherwise None
    """

    match = re.search('[i,I][0-9]{2}', text)

    if match:
        span = match.span()
        room_name = text[span[0]:span[1]]
        return room_name.upper()
    else:
        return None
