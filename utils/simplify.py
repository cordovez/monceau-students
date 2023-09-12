from models.student_model import Student

def simplify_student_data(raw_data) -> list:
    students :list = []
    for student in raw_data:
        student_name = list(student.values())[0]["trainee"]
        last_name, first_name = student_name.split(',')
        
        telephone = list(student.values())[0]["telephone"]
        mobile = list(student.values())[0]["mobile"]
        email = list(student.values())[0]["email address"]
        employer = list(student.values())[0]["client"]
        course_type = list(student.values())[0]["course type"]
        start_date = list(student.values())[0]["start date"]
        end_date = list(student.values())[0]["end date"]
        start_level = list(student.values())[0]["start level"]
        hours = list(student.values())[0]["hours per trainee"]
        hours_remaining = list(student.values())[0]["hours remaining"]
        
        
        students.append(Student(last_name , first_name, telephone, mobile, 
                                email, employer, course_type, start_date, 
                                end_date, start_level, hours, hours_remaining))
    return students
        