from fastapi import APIRouter
from controllers.student_roster_data import parse_student_data
from controllers.results_to_dict import convert_tuples_to_dict
from controllers.monthly_schedule_data import get_scheduled_classes
from utils.playwright_html import get_page_html
from utils.generate_path_to_students import path_to_students

from utils.simplify import simplify_student_data

student_router = APIRouter()

@student_router.get("/raw") 
def get_all_students() -> list :
    """
    log into Monceau intranet and scrape student data

    Returns:
        list of dictionaries
    """
    path = path_to_students()
    html = get_page_html(path)
    data = parse_student_data(html)
    students = convert_tuples_to_dict(data)
    return students
    
@student_router.get("/minimal") 
def get_all_students_minimal() -> list :
    """
    log into Monceau intranet and scrape student data

    Returns:
        list of dictionaries
    """
    path = path_to_students()
    html = get_page_html(path)
    data = parse_student_data(html)
    long_form = convert_tuples_to_dict(data)
    short_form = simplify_student_data(long_form)
    
    
    return short_form

@student_router.get('/classes')
def get_all_classes():
    html = get_page_html("scheduling/view_month_trainer.asp")
    data = get_scheduled_classes(html)
    return data