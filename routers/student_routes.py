from fastapi import APIRouter
from controllers.playwright_students import login_and_extract_students
from controllers.results_to_dict import convert_tuples_to_dict

from utils.simplify import simplify_student_data

student_router = APIRouter()

@student_router.get("/raw") 
def get_all_students() -> list :
    """
    log into Monceau intranet and scrape student data

    Returns:
        list of dictionaries
    """
    data = login_and_extract_students()
    students = convert_tuples_to_dict(data)
    return students
    
@student_router.get("/minimal") 
def get_all_students_minimal() -> list :
    """
    log into Monceau intranet and scrape student data

    Returns:
        list of dictionaries
    """
    data = login_and_extract_students()
    long_form = convert_tuples_to_dict(data)
    short_form = simplify_student_data(long_form)
    
    
    return short_form