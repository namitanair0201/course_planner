import csv
file_name = '../static/assets/courses.csv'
def read_from_csv(file_name):
    course_names, course_numbers, check_dict = [],[],{}

    with open(file_name, newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        db = list(reader)

    for course in db:
        check_dict[course['c_number']]=course
        check_dict[course['c_name']]=course
        course_names.append(course['c_name'])
        course_numbers.append(course['c_number'])

    return course_names, course_numbers, check_dict, db