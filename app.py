from flask import Flask, render_template, request
from helpers.readcsv import read_from_csv, read_student_info, save_student_info
app = Flask(__name__)

#DOUBT1: WHY ARE WE STORING STUFF LIKE A DICTIONARY INSIDE A TABLE?
#GET Flask name

course_names, course_numbers, check_dict, db  = read_from_csv('static/assets/courses.csv')

@app.route('/<int:usc_id>', methods=['GET','POST'])
def Hello_world(usc_id):
    error,save_msg = '',''

    form_submitted = request.form
    courses_taken = []

    student_info = read_student_info('static/assets/students/'+str(usc_id)+'.csv',check_dict)

    if 'btn' in form_submitted and form_submitted['btn'] == 'Add':
        if (('c_number' in form_submitted) and (form_submitted['c_number'] in check_dict)):
            courses_taken.append(check_dict[form_submitted['c_number']])
        elif 'c_name' in form_submitted and form_submitted['c_name'] in check_dict:
            courses_taken.append(check_dict[form_submitted['c_name']])
        else:
            error = 'Course name/number does not exist in DB'
    elif 'remove' in form_submitted:
        for course_taken in courses_taken:
            if course_taken['c_number'] == form_submitted['remove'][7:]:
                courses_taken.remove(course_taken)

    elif 'btn' in form_submitted and form_submitted['btn'] == 'Save / Export':
        if save_student_info('static/assets/students/123.csv', student_info):
            save_msg = 'Saved!'
        else:
            error = 'Error in saving'

    return render_template('index.html', student_info=student_info, course_names=course_names, course_numbers=course_numbers, save_msg=save_msg, error=error)

if __name__ == '__main__':
    app.run(debug=True)