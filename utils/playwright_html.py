from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()
login_password = os.getenv("PASSWORD")
login_username = os.getenv("USERNAME")
base_url = os.getenv("BASE_URL")


def get_page_html(path_to_page:str):
    """
    function uses playwright to login to site and uses the path_to_page to grab 
    and return the html for that page. 
    """
    
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False, slow_mo=50)
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f'{base_url}/login.asp')
        page.fill('input#username', login_username)
        page.fill('input#password', login_password)
        page.click('button[type=submit]')
        
        page.goto(f'{base_url}/{path_to_page}')
        body = page.inner_html('body')
        return body