from dataclasses import dataclass
@dataclass
class DateObject:
    dateTime: str
    timeZone: str = "Europe/Paris"
    
@dataclass
class Event:
    """summary: str
    location: str
    description: str
    colorId: int
    start: DateObject
    end: DateObject
    recurrence: list
    attendees: list"""
    summary: str
    location: str
    description: str
    colorId: int
    start: DateObject
    end: DateObject
    recurrence: list
    attendees: list