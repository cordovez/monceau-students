class DateObject:
    dateTime: str
    timeZone: str = "Europe/Paris"

class Event:
    summary: str
    location: str
    description: str
    colorId: int
    start: DateObject
    end: DateObject
    recurrence: list
    attendees: list