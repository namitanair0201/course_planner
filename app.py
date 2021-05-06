from flask import Flask, render_template, request
from helpers.readcsv import read_from_csv, read_student_info, save_student_info, save_new_course, read_notes, save_notes, delete_a_course
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

        student_info['name'], student_info['usc_id'], student_info['major'], student_info['years'] = form_submitted['name'], form_submitted['usc_id'], form_submitted['major'], [form_submitted['year_of_joining']]
        student_info['image_link']=""
        student_info[form_submitted['year_of_joining']] = {'fall':[],'spring':[],'summer':[]}

        if student_info['usc_id'] in [x['usc_id'] for x in students_info]:
            error = 'USC id matches to an existing users'
        else:
            save_student_info(student_data_path+str(student_info['usc_id'])+'.csv', student_info)
            message = 'New user added successfully'
        
            notes_path = 'static/assets/notes/'+str(student_info['usc_id'])+'.json'
            notes = {'general':''}
            notes[form_submitted['year_of_joining']] = {'fall':{},'spring':{},'summer':{}}
            save_notes(notes_path,notes)

    elif 'remove' in form_submitted:
        os.remove(student_data_path+form_submitted['remove']+".csv")
        os.remove('static/assets/notes/'+form_submitted['remove']+".json")
        message = 'User with USC ID: '+form_submitted['remove']+' removed successfully'


    students_paths = glob.glob(student_data_path+'*.csv')
    students_info = sorted([read_student_info(student_path,check_dict) for student_path in students_paths], key = lambda x: x["name"])
    
    return render_template('main.html', students_info=students_info, message=message, error = error)


@app.route('/courses', methods=['GET','POST'])
def Courses():
    course_names, course_numbers, check_dict, db  = read_from_csv('static/assets/courses.csv')

    form_submitted = request.form
    message,error = '',''
    #students_paths = glob.glob(student_data_path+'*.csv')
    #students_info = [read_student_info(student_path,check_dict) for student_path in students_paths]
    if 'remove_course' in form_submitted:
        course_number = form_submitted['remove_course'].split()[-1]
        filtered = list(filter(lambda x: x['c_number']!=course_number, db))
        
        check_dict = {}
        for course in filtered:
            check_dict[course['c_number']]=course
            check_dict[course['c_name']]=course

        try:
            students_paths = glob.glob(student_data_path+'*.csv')
            students_info = [read_student_info(student_path,check_dict) for student_path in students_paths]
            delete_a_course(filtered)
            message = 'Successfully removed '+course_number
            db = filtered
        except:
            error = course_number+' is taken by one or more student(s)'

    return render_template('courses.html', db=db, message=message, error = error)

@app.route('/petitions/<int:ref_number>', methods=['GET','POST'])
def petitions(ref_number):
    return render_template('petitions.html', ref_number = ref_number)


@app.route('/<int:usc_id>', methods=['GET','POST'])
def Hello_world(usc_id):

    course_names, course_numbers, check_dict, db  = read_from_csv('static/assets/courses.csv')
    notes_path = 'static/assets/notes/'+str(usc_id)+'.json'
    notes = read_notes(notes_path)
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
            # notes[year][term][form_submitted['c_number']]=''
            # save_notes(notes_path,notes)

        elif 'c_name' in form_submitted and form_submitted['c_name'] in check_dict:
            student_info[year][term].append(check_dict[form_submitted['c_name']])
            message = 'Successfully added course '+str(form_submitted['c_number'])
            # notes[year][term][form_submitted['c_number']]=''
            # save_notes(notes_path,notes)

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
        notes[new_year]={'fall':{},'spring':{},'summer':{}}
        save_notes(notes_path,notes)

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

            del notes[year]
            save_notes(notes_path,notes)

    elif 'remove' in form_submitted:
        text = form_submitted['remove'].split()
        term = text[3]
        year = text[5]
        c_number = text[1]
        for course_taken in student_info[year][term]:
            if course_taken['c_number'] == c_number:
                student_info[year][term].remove(course_taken)
                if course_taken['c_number'] in notes[year][term]:
                    del notes[year][term][course_taken['c_number']]
                save_notes(notes_path,notes)

        removed = 'Successfully removed '+str(c_number)
    elif 'year' in form_submitted:
        new_year = form_submitted['new_year']
        
        if not student_info['years']:
            student_info['years'] = [new_year]
        if new_year not in student_info['years']:
            student_info['years'].append(new_year)
            student_info[new_year]={'fall':[],'spring':[],'summer':[]}
            message = 'Successfully added '+new_year

            notes[new_year]={'fall':{},'spring':{},'summer':{}}
            save_notes(notes_path,notes)
        else:
            error = 'Selected year already exists'
    
    elif 'major' in form_submitted:
        major = form_submitted['major']
        message = 'Successfully selected ' + major
        student_info['major'] = major

    elif 'save_notes' in form_submitted:
        general = form_submitted['general_notes']
        notes['general'] = general
        save_notes(notes_path,notes)
    
    elif 'save_course_note' in form_submitted:
        year = form_submitted['notes_modal_year']
        term = form_submitted['notes_modal_term']
        c_num = form_submitted['notes_modal_c_num']
        text = form_submitted['notes_modal_text']
        if year not in notes:
            notes[year] = {'fall':{},'spring':{},'summer':{}}
        notes[year][term][c_num] = text
        save_notes(notes_path,notes)
    
    if student_info['years']:
        student_info['years'].sort()
    
    student_info['notes'] = notes

    save_student_info(student_data_path+str(usc_id)+'.csv', student_info)
    
    res = score(student_info)
    
    return render_template('index.html', usc_id = usc_id, student_info=student_info, res=res, course_names=course_names, course_numbers=course_numbers, message=message, removed=removed,error=error)

if __name__ == '__main__':
    app.run(debug=True)