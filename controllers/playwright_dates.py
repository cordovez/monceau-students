from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import datetime
import re
import pprint

pp = pprint.PrettyPrinter(indent=4)


load_dotenv()
login_password = os.getenv("PASSWORD")
login_username = os.getenv("USERNAME")
base_url = os.getenv("BASE_URL")


def login_and_extract_dates():
    """
    function uses playwright to login to site and parse student information.
    The function returns a list of students with data in tuple pairs.
    """
    
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False, slow_mo=50)
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f'{base_url}/login.asp')
        page.fill('input#username', login_username)
        page.fill('input#password', login_password)
        page.click('button[type=submit]')
        
        page.goto(f'{base_url}/scheduling/view_month_trainer.asp')
        
        
        table_html = page.inner_html('div.dataTables_scroll')
        summary_html = page.inner_html('div.summaryColumns')
        
        soup = BeautifulSoup(table_html, 'html.parser')
        summary_soup = BeautifulSoup(summary_html, 'html.parser')
        
        table_head = soup.find('thead').tr.find_all('th')  
        row_data = soup.find('tbody').find_all('tr')
        
        
        # Get Month year
        date = summary_soup.find('p').find('span').text
        month, year = date.split(' ')
        
        
        # Get Dates on the table head for the month
        dates = []
        scheduled_classes = []
        for day in table_head: 
            label = day.text
            day_match = re.search(r'([A-Za-z]+)(\d+)', label)
            if day_match:
                day = day_match.group(1)
                date = day_match.group(2)
                dates.append((day, date))
                
        for row_index, row in enumerate(row_data, start=1):
            # print( '\nRow:', row_index,)    
            # print( "*"*40)   
             
            cells = row.find_all('td')
            

            for col_index, cell in enumerate(cells, start=1):
                scheduled_cells = cell.select('.slot-time')
                student = cell.find('strong')
                info = [item for item in cell.find_all('span', class_='slot-text')]
                
                for cell in scheduled_cells:
                    if cell is not None:
                        class_dictionary = {}
                        class_dictionary['time'] = cell.text 
                        class_dictionary['duration'] = info[2].text.split(' ')[1]
                        full_name = student.text.split(', ')
                        
                        if len(full_name) >= 2:
                            class_dictionary['last_name'] = full_name[0].title()
                            class_dictionary['first_name'] = full_name[1]
                        else:
                            class_dictionary['name'] = student.text.title()
                       
                        class_dictionary['day'] = col_index
                        class_dictionary['employer'] = info[1].text.title()
                        class_dictionary['location'] = info[3].text
                        
                        scheduled_classes.append(class_dictionary)
                    
        return scheduled_classes

           



            
if __name__ == "__main__":
   login_and_extract_dates() 