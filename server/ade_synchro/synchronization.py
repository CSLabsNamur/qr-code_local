import datetime
import ics
import ics.parse
import requests


class SynchronizationError(Exception):
    """ Raised when the synchronization fails """
    pass


def get_unamur_ade_ical_url(first_date, last_date):
    """ Get an url of the Ade of Unamur for an ical file

    :precondition: first_date and last_date are dates in iso format
    :precondition: first_date is not a date after last_date

    :param first_date: The first date parameter of the ical (str)
    :param last_date: The last date parameter of the ical (str)
    :return: An url of the ADE of Unamur that response an ical file (str)
    """
    resources = [
        # Fac INFO
        1957, 186, 185, 1495, 2870, 2044,
        2049, 1597, 1492, 1816, 3329, 3297,
        2874, 962, 967, 586, 585, 3005, 1594,
        975, 2043, 660, 665, 418, 412, 635,
        636, 1522, 2899, 679, 2946, 1521, 3083,
        2943, 2944, 43, 1516, 976, 1372, 1419,
        2696, 2697
    ]

    url = 'https://www.unamur.be/jsp/custom/modules/plannings/anonymous_cal.jsp' \
          '?firstDate=%s&lastDate=%s&projectId=%s&login=web&password=web&calType=ical&resources=%s' % (
              first_date,
              last_date,
              7,
              ','.join([str(res) for res in resources])
          )

    print(url)

    return url


def get_unamur_events():
    """ Get the events from the ADE of Unamur,
        from one week ago until the end of the academic year (12 september).

        :throws SynchronizationError: if the application fails to synchronize with ADE
        :return: The ical events from ADE of Unamur (Set[ics.Event])
    """

    now = datetime.date.today()
    begin = now - datetime.timedelta(weeks=1)
    end = datetime.date(year=now.year, month=9, day=12)

    if now >= end:
        end = datetime.date(year=end.year+1, month=end.month, day=end.day)

    ade_first_date = begin.isoformat()
    ade_last_date = end.isoformat()

    url = get_unamur_ade_ical_url(ade_first_date, ade_last_date)

    try:
        response = requests.get(url)
        calendar = ics.Calendar(response.text)

        return calendar.events

    except (requests.ConnectionError, ics.parse.ParseError):
        raise SynchronizationError('Failed to fetch the events from the ADE of Unamur')



