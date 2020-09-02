from flask import Flask, render_template, request
from helpers.readcsv import read_from_csv, read_student_info, save_student_info, save_new_course
from helpers.score import bcs,quantp,dp,socialp,getCourseList,score
import glob
import os

app = Flask(__name__)

student_data_path = './static/assets/students/'

@app.route('/', methods=['GET','POST'])
def Main():
    course_names, course_numbers, check_dict, db  = read_from_csv('static/assets/courses.csv')

    form_submitted = request.form
    message,error = '',''
    students_paths = glob.glob(student_data_path+'*.csv')
    students_info = [read_student_info(student_path,check_dict) for student_path in students_paths]
    if 'new_student' in form_submitted:
        student_info = {}

        student_info['name'], student_info['image_link'], student_info['usc_id'], student_info['major'], student_info['years'] = form_submitted['name'], form_submitted['image_link'], form_submitted['usc_id'], form_submitted['major'], [form_submitted['year_of_joining']]
        
        student_info[form_submitted['year_of_joining']] = {'fall':[],'spring':[],'summer':[]}

        if student_info['image_link']=='':
            student_info['image_link'] = 'https://media3.giphy.com/media/bhJqCi6LVaDPG/giphy.gif'

        if student_info['usc_id'] in [x['usc_id'] for x in students_info]:
            error = 'USC id matches to an existing users'
        else:
            save_student_info(student_data_path+str(student_info['usc_id'])+'.csv', student_info)
            message = 'New user added successfully'
    
    elif 'remove' in form_submitted:
        os.remove(student_data_path+form_submitted['remove']+".csv")
        message = 'User with USC ID: '+form_submitted['remove']+' removed successfully'


    students_paths = glob.glob(student_data_path+'*.csv')
    students_info = [read_student_info(student_path,check_dict) for student_path in students_paths]
    
    return render_template('main.html', students_info=students_info, message=message, error = error)

@app.route('/<int:usc_id>', methods=['GET','POST'])
def Hello_world(usc_id):

    course_names, course_numbers, check_dict, db  = read_from_csv('static/assets/courses.csv')

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
    
    elif 'custom_course' in form_submitted:
        # subs, psyc = '0','0'
        # if form_submitted['subs'] == 'YES':
        #     subs = '1'
        # if form_submitted['psyc'] != 'NON-PSYC':
        #     psyc = '1'
        
        course_dict = {"c_number":form_submitted['c_number'],"c_name":form_submitted['c_name'],"c_category":"D","c_credits":form_submitted['c_credits'],"subs":form_submitted['subs'],"psych":form_submitted['psych']}

        if form_submitted['c_number'] not in check_dict:
            save_new_course(course_dict)
            message = 'Successfully added a new course '+str(form_submitted['c_number'])
        else:
            error = 'Course already exists '+form_submitted['c_number']

        new_year = form_submitted['year']
        if not student_info['years']:
            student_info['years'] = [new_year]
            #student_info[new_year]={'fall':[],'spring':[],'summer':[]}

        if new_year not in student_info['years']:
            student_info['years'].append(new_year)
            student_info[new_year]={'fall':[],'spring':[],'summer':[]}
        
        student_info[new_year][form_submitted['c_term']].append(course_dict)
        check_dict[form_submitted['c_number']]=course_dict

    elif 'remove_year' in form_submitted:
        if len(student_info['years']) == 1:
            error = 'Minimum one year required'
        else:
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
    
    elif 'major' in form_submitted:
        major = form_submitted['major']
        message = 'Successfully selected ' + major
        student_info['major'] = major

    if student_info['years']:
        student_info['years'].sort()
    
    save_student_info(student_data_path+str(usc_id)+'.csv', student_info)
    
    res = score(student_info)

    return render_template('index.html', student_info=student_info, res=res, course_names=course_names, course_numbers=course_numbers, message=message, removed=removed,error=error)

if __name__ == '__main__':
    app.run(debug=True)