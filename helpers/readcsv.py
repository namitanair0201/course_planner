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

def read_student_info(file_name, check_dict):
    with open(file_name, newline='\n') as csvfile:
        result = {}
        csv_reader = csv.reader(csvfile, delimiter=',')
        csv_reader = list(csv_reader)
        _,result['name'] = csv_reader[0]
        _,result['usc_id'] = csv_reader[1]
        _,result['program'] = csv_reader[2]
        result['years'] = csv_reader[3][1:]
        for each_year in range(4,4*(len(result['years'])+1),4):
            result[csv_reader[each_year][0]]={'fall':[check_dict[x] for x in csv_reader[each_year+1][1:]],'spring':[check_dict[x] for x in csv_reader[each_year+2][1:]],'summer':[check_dict[x] for x in csv_reader[each_year+3][1:]]}
        return result

def save_student_info(file_name, student_info):
    s_vals = student_info
    print( "YAHA pe", s_vals)
    text_to_save = "name,"+s_vals['name']+"\n"
    text_to_save += "usc_id,"+s_vals['usc_id']+"\n"
    text_to_save += "program,"+s_vals['program']+"\n"
    text_to_save += "years,"+",".join(s_vals['years']) + "\n"
    
    print(text_to_save)
    n = len(s_vals['years'])
    
    for i in range(n):
        text_to_save += s_vals["years"][i]+ '\n'
        
        text_to_save += 'fall,'
        for j in s_vals[s_vals["years"][i]]['fall']:
            text_to_save += j['c_number']+','
        text_to_save = text_to_save[:-1]+'\n'

        text_to_save += 'spring,'
        for j in s_vals[s_vals["years"][i]]['spring']:
            text_to_save += j['c_number']+','
        text_to_save = text_to_save[:-1]+'\n'

        text_to_save += 'summer,'
        for j in s_vals[s_vals["years"][i]]['summer']:
            text_to_save += j['c_number']+','
        text_to_save = text_to_save[:-1]+'\n'

    f = open(file_name,'w')
    f.write(text_to_save)
    f.close()
