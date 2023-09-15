from fastapi import APIRouter
import json

from controllers.monthly_schedule_data import (get_scheduled_classes,
                                               get_summary_info,
                                               get_calendar_dates,
                                               convert_to_datetimes)
from utils.playwright_html import get_page_html
from models.calendar_event_model import Event

from utils.simplify import simplify_student_data

events_router = APIRouter()

@events_router.get('/monthly')
def get_monthly_schedules():
    # playwright logs in and gathers html
    html = get_page_html("scheduling/view_month_trainer.asp")
    
    # parse html
    summary = get_summary_info(html)
    dates_in_the_month = get_calendar_dates(html)
    appointments = get_scheduled_classes(html)
    
    # clean data
    events = convert_to_datetimes(summary["year"], summary["month"],
                                  dates_in_the_month, appointments)

    # convert to Models
    calendar_events = []
    event_dicts = [] 
    for event in events:
        event_color = None
        if event['location'] == "client offices":
            event_color = 6
        elif event['location'] == "visio": 
            event_color = 10
            
        event_dict = {
            "summary": event['full_name'],
            "location": event['location'],
            "description": event['employer'],
            "colorId": event_color,
            "start": event['start_time'],
            "end": event['end_time'],
            "recurrence": [],
            "attendees": []
        }
        
        event_dicts.append(event_dict)
        
    # for event in events:
    #     event['start_time']
    #     event_color = None
    #     # chose colour
    #     if event['location'] == "client offices":
    #         event_color = 6
    #     elif event['location'] == "visio": 
    #         event_color = 10
    #     else:
    #         event_color = None 
            
    #     calendar_event = Event( summary=event['full_name'], 
    #                            location=event['location'], 
    #                            description=event['employer'], 
    #                            colorId=event_color, 
    #                            start=event['start_time'], 
    #                            end=event['end_time'], 
    #                            recurrence=[], 
    #                            attendees=[])
    #     calendar_events.append(calendar_event) 

        # convert to JSON to print
        # cal_event_dict = json.dumps(calendar_event.__dict__)
        # event_dicts.append(cal_event_dict)
        
        # Serialize the list of dictionaries to JSON
    response_json = {
        "events": event_dicts
    }
    
    with open('calendar_events.json', 'w') as file:
        json.dump(response_json, file, indent=4)
                       
    return response_json 

