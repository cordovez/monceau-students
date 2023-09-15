from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
login_password = os.getenv("PASSWORD")
login_username = os.getenv("USERNAME")
base_url = os.getenv("BASE_URL")

def past_three_years():
    today = datetime.date.today()
    three_years_ago = today - datetime.timedelta(days=365 * 3)
    return three_years_ago

def login_and_extract_students() -> list:
    """
    function uses playwright to login to site and parse student information.
    The function returns a list of students with data in tuple pairs.
    """
    start_date = past_three_years()
    
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False, slow_mo=50)
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f'{base_url}/login.asp')
        page.fill('input#username', login_username)
        page.fill('input#password', login_password)
        page.click('button[type=submit]')
        
        page.goto(f'{base_url}/stagiaires/traineeContract_listing_trainer.asp?startDate={start_date}')
        
        
        html = page.inner_html('div.dataTables_scroll')
        soup = BeautifulSoup(html, 'html.parser')
        
        
        table_head = soup.find('thead').tr.find_all('th')  
        row_data = soup.find('tbody').find_all('tr')
        
        
        labels = [] 
        student_data = [] 
        students = []

        for th in table_head:
            if th.text:  
                labels.append(th.text.strip())  
            elif th.img and 'alt' in th.img.attrs:  
                labels.append(th.img['alt'])
                
    
        for td in row_data:
            if td.text:
                # clean_data = td.text.strip().replace('\n', '')
                clean_data = [item for item in td.text.strip().split('\n')]
                student_data.append(clean_data)
                
        for student in student_data:
            result = zip(labels, student)
            students.append(list(result))

        return students
            
