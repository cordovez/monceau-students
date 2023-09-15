# from utils.playwright_html import get_page_html

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
# from dotenv import load_dotenv
# import os
from datetime import datetime
import pytz

import re
import pprint
from collections import namedtuple
# from utils.playwright_html import get_page_html

pp = pprint.PrettyPrinter(indent=4)


# load_dotenv()
# login_password = os.getenv("PASSWORD")
# login_username = os.getenv("USERNAME")
# base_url = os.getenv("BASE_URL")


def get_summary_info(html)-> dict:
    """Function returns the year, month, and hours scheduled"""
    
    page_html = BeautifulSoup(html, 'html.parser')
    summary = page_html.find('div', class_='summaryColumns')
    date = summary.find('p').find('span').text
    month, year = date.split(' ')
    hours_list = summary.find('div').find_all('div')
    hours_scheduled = hours_list[1].find('p').find('span').text
    
    return {'year': year, 'month':month, 'hours scheduled': hours_scheduled}


def get_calendar_dates(html)-> list[tuple]:
    """funtion returns a list of named tuples for the dates on the head of 
    the source calendar. For example Date(index=3, day='Thursday', date='7)
    
    The index is included to help me match scheduled classes (cell) to the 
    corresponding date (column)
    """
    
    Date = namedtuple('Date', 'index day date')
    page_html = BeautifulSoup(html, 'html.parser')
    column_heads = page_html.find('table').thead.tr.find_all('th')
    
    dirty_dates = [item.text for item in column_heads] 
    clean_dates =[]
    
    for index, item in enumerate(dirty_dates, start=1):
        day_match = re.search(r'([A-Za-z]+)(\d+)', item)
        day_of_the_week = day_match.group(1)
        date_of_the_month = day_match.group(2)
        date = Date(index, day_of_the_week, date_of_the_month)
        clean_dates.append(date)   
    
    return clean_dates


def get_scheduled_classes(html) -> list[dict]:
    """ function retrieves all cells in the table which have a class scheduled,
    and returns a list with the information of each scheduled class as a dictionary.
    
    The value of column_day is used to match with the dates on the 
    table head returned by get_calendar_dates().
    """
    page_html = BeautifulSoup(html, 'html.parser')
    row_data = page_html.find('tbody').find_all('tr')
    scheduled_classes = []
    
    # for each row
    for row in row_data:
            
        cells = row.find_all('td')
        
        # navigate across all the cells
        for col_index, cell in enumerate(cells, start=1):
            scheduled_cells = cell.select('.slot-time')
            student = cell.find('strong')
            info = [item for item in cell.find_all('span', class_='slot-text')]
            
            # find cells with scheduled classes
            for cell in scheduled_cells:
                if cell is not None:
                    class_dictionary = {}
                    class_dictionary['start_time'], class_dictionary['end_time'] = cell.text.split(' - ')
                    class_dictionary['duration'] = info[2].text.split(' ')[1]
                    full_name = student.text.split(', ')
                    class_dictionary['full_name'] = student.text
                    
                    if len(full_name) >= 2:
                        class_dictionary['last_name'] = full_name[0].title()
                        class_dictionary['first_name'] = full_name[1]
                    else:
                        class_dictionary['name'] = student.text.title()
                    
                    class_dictionary['column_day'] = col_index
                    class_dictionary['employer'] = info[1].text.title()
                    class_dictionary['location'] = info[3].text
                    
                    scheduled_classes.append(class_dictionary)
                
    return scheduled_classes

def convert_to_datetimes(year:str, month:str, calendar_dates:list, 
                         events: list):
    local_tz = pytz.timezone('Europe/Paris')
    current_year = year
    current_month = month
    new_events = []
    for event in events:
        new_event = {**event}
        
        for date in calendar_dates:
                if date.index == new_event['column_day']:
                    new_event['day'] = date.day
                    new_event['date'] = date.date 
                    new_event['year'] = current_year
                    new_event['month'] = current_month
                    new_events.append(new_event)
                    
                    # Datetime
                    start_str = f"{date.date} {current_month} {current_year}, {new_event['start_time']}"
                    end_str = f"{date.date} {current_month} {current_year}, {new_event['end_time']}"
                    
                    # Parse the start and end times
                    start_time = datetime.strptime(start_str, '%d %B %Y, %H:%M')
                    end_time = datetime.strptime(end_str, '%d %B %Y, %H:%M')
                    
                    # Apply the local timezone to the times
                    start_time = local_tz.localize(start_time)
                    end_time = local_tz.localize(end_time)
                    
                    new_event["start_time"] = start_time.isoformat()
                    new_event["end_time"] = end_time.isoformat()
                    
                
    return new_events