from models.student_model import Student

from utils.simplify import simplify_student_data
          
def convert_tuples_to_dict(list_of_tuples: list) -> list:
    """
    function takes a list of students and their data as tuple pairs and returns
    a list of dictionaries, one for each student.
    """
    students_list = []
    for student in list_of_tuples:
        student_dict = {}
        for label, data in student:
            student_dict[label] = data
            name = student_dict['trainee']
        students_list.append({name : student_dict})
        
    
    
    return students_list

        

