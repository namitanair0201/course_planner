from flask import Flask, render_template, request
from helpers.readcsv import read_from_csv, read_student_info, save_student_info
import glob
app = Flask(__name__)

student_data_path = './static/assets/students/'

course_names, course_numbers, check_dict, db  = read_from_csv('static/assets/courses.csv')


@app.route('/', methods=['GET'])
def Main():
    students_paths = glob.glob(student_data_path+'*.csv')
    students_info = [read_student_info(student_path,check_dict) for student_path in students_paths]
    return render_template('main.html', students_info=students_info)

@app.route('/<int:usc_id>', methods=['GET','POST'])
def Hello_world(usc_id):
    error,message,removed = '','',''
    form_submitted = request.form

    student_info = read_student_info(student_data_path+str(usc_id)+'.csv',check_dict)
    if student_info['years']:
        student_info['years'].sort()
    if 'add_course' in form_submitted:
        text = form_submitted['add_course'].split()
        term = text[2]
        year = text[4]
        if (('c_number' in form_submitted) and (form_submitted['c_number'] in check_dict)):
            student_info[year][term].append(check_dict[form_submitted['c_number']])
            message = 'Successfully added course '+str(form_submitted['c_number'])
        elif 'c_name' in form_submitted and form_submitted['c_name'] in check_dict:
            student_info[year][term].append(check_dict[form_submitted['c_name']])
            message = 'Successfully added course '+str(form_submitted['c_number'])
        else:
            error = 'Course name/number does not exist in DB'
    elif 'remove_year' in form_submitted:
        year = form_submitted['remove_year'].split()[-1]
        student_info['years'].remove(year)
        student_info.pop(year)
        message = 'Successfully removed '+year

    elif 'remove' in form_submitted:
        text = form_submitted['remove'].split()
        term = text[3]
        year = text[5]
        c_number = text[1]
        for course_taken in student_info[year][term]:
            if course_taken['c_number'] == c_number:
                student_info[year][term].remove(course_taken)
        removed = 'Successfully removed '+str(c_number)
    elif 'year' in form_submitted:
        new_year = form_submitted['new_year']
        
        if not student_info['years']:
            student_info['years'] = [new_year]
        if new_year not in student_info['years']:
            student_info['years'].append(new_year)
            student_info[new_year]={'fall':[],'spring':[],'summer':[]}
            message = 'Successfully added '+new_year
        else:
            error = 'Selected year already exists'
    
    if student_info['years']:
        student_info['years'].sort()
    save_student_info(student_data_path+str(usc_id)+'.csv', student_info)
    return render_template('index.html', student_info=student_info, course_names=course_names, course_numbers=course_numbers, message=message, removed=removed,error=error)

if __name__ == '__main__':
    app.run(debug=True)