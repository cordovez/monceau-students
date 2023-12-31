from __future__ import print_function

import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
# SCOPES = ['https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/calendar.readonly']
f = open('calendar_events.json')
data = json.load(f)
events = data['events']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token_v2.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('tokenv2.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
 
        for item in events:
            event = {
                "summary": item["summary"],
                "location": item["location"],
                "description": item["description"],
                "colorId": item["colorId"],
                "start": {
                    "dateTime": item["start"], 
                    "timeZone": "Europe/Paris"
                    },
                "end": {
                    "dateTime": item["end"], 
                    "timeZone": "Europe/Paris"
                    },
                "recurrence": item["recurrence"],
                "attendees": item["attendees"]
                
            }
            event = service.events().insert(calendarId="primary", body=event).execute()
        print( len(events), "events added")
       

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()