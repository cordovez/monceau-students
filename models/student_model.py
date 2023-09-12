from dataclasses import dataclass

@dataclass
class Student:
    """ Class for simplifying student data
    """
    last_name: str
    first_name: str
    telephone: str
    mobile: str
    email: str
    employer: str
    course_type: str
    start_date: str
    end_date: str
    start_level: str
    hours: str
    hours_remaining: str
