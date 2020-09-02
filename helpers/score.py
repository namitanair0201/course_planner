from collections import OrderedDict 
import pandas as pd

def bcs(courses_taken):
    res = dict()
    c_numbers = courses_taken['c_number'].values
    catA = sum(list(map(int,courses_taken.loc[courses_taken['c_category']== 'A','c_credits'].values)) )
    catB = sum(list(map(int,courses_taken.loc[courses_taken['c_category']== 'B','c_credits'].values)) )
    catC = sum(list(map(int,courses_taken.loc[courses_taken['c_category']== 'C','c_credits'].values)) )
    psyc = sum(list(map(int,courses_taken.loc[courses_taken['psych']== '1','c_credits'].values)) )
    subs = sum(list(map(int,courses_taken.loc[courses_taken['subs']== '1','c_credits'].values)))
    phd = sum(list(map(int,courses_taken['c_credits'].values)))
    res['area_requirements']= []
    if '621' in c_numbers:
        res['area_requirements'] = "All Requirements Met" #all satisfied
    else:
        if not all(c in c_numbers for c in ['500','501']):
            res['area_requirements'] = ["PSYC 500/501"]
        if not all(c in c_numbers for c in ['502','503']):
            res['area_requirements'].append('PSYC 502/503')
    res['A'] = 8 - catA if catA < 8 else 0
    res['B'] = 4-catB if catB <4 else 0
    res['C'] = 4-catC if catC <4 else 0 
    res['BC'] = 16 - (catB+ catC) if (catB+ catC) < 16 else 0
    res['phd'] = 60 - phd if phd < 60 else 0
    res['subs'] = 36 - subs if subs < 36 else 0
    res['psyc'] = 24 - psyc if psyc < 24 else 0
    
    return res

def quantp(courses_taken):
    res = dict()
    no_catA = len(list(courses_taken.loc[courses_taken['c_category']== 'A','c_number']))
    catA = sum(list(map(int,courses_taken.loc[courses_taken['c_category']== 'A','c_credits'].values)) )
    catB = sum(list(map(int,courses_taken.loc[courses_taken['c_category']== 'B','c_credits'].values)) )
    catC = sum(list(map(int,courses_taken.loc[courses_taken['c_category']== 'C','c_credits'].values)) )
    psyc = sum(list(map(int,courses_taken.loc[courses_taken['psych']== '1','c_credits'].values)) )
    subs = sum(list(map(int,courses_taken.loc[courses_taken['subs']== '1','c_credits'].values)))
    phd = sum(list(map(int,courses_taken['c_credits'].values)))

    res['area_requirements'] = ["All Requirements Met"] if no_catA >= 6 else [str(6-no_catA) + " category A Courses Required" ]
    res['A'] = 8 - catA if catA < 8 else 0
    res['B'] = 4-catB if catB <4 else 0
    res['C'] = 4-catC if catC <4 else 0
    res['BC'] = 16 - (catB+ catC) if (catB+ catC) < 16 else 0
    res['phd'] = 60 - phd if phd < 60 else 0
    res['subs'] = 36 - subs if subs < 36 else 0
    res['psyc'] = 24 - psyc if psyc < 24 else 0

    return res

def dp(courses_taken):
    res = dict()
    catA = sum(list(map(int,courses_taken.loc[courses_taken['c_category']== 'A','c_credits'].values)) )
    catB = sum(list(map(int,courses_taken.loc[courses_taken['c_category']== 'B','c_credits'].values)) )
    catC = sum(list(map(int,courses_taken.loc[courses_taken['c_category']== 'C','c_credits'].values)) )
    psyc = sum(list(map(int,courses_taken.loc[courses_taken['psych']== '1','c_credits'].values)) )
    subs = sum(list(map(int,courses_taken.loc[courses_taken['subs']== '1','c_credits'].values)))
    phd = sum(list(map(int,courses_taken['c_credits'].values)))
    c_numbers = courses_taken['c_number'].values
    res['area_requirements'] = ""
    if not all(c in c_numbers for c in ['500','501']):
        res['area_requirements'] = ["PSYC 500/501"]
        if not any(c in c_numbers for c in ['502','573','575']):
            res['area_requirements'].append("PSYC 502/573/575") #not satisfied
    else:
        res['area_requirements'] = ["All Requirements Met"] #satisfied

    res['A'] = 8 - catA if catA < 8 else 0
    res['B'] = 4-catB if catB <4 else 0  
    res['C'] = 4-catC if catC <4 else 0
    res['BC'] = 16 - (catB+ catC) if (catB+ catC) < 16 else 0
    res['phd'] = 60 - phd if phd < 60 else 0
    res['subs'] = 36 - subs if subs < 36 else 0
    res['psyc'] = 24 - psyc if psyc < 24 else 0

    return res

def socialp(courses_taken):
    res = dict()
    c_numbers = courses_taken['c_number'].values
    cc_numbers = list(courses_taken.loc[courses_taken['c_category']== 'C','c_number'])
    catA = sum(list(map(int,courses_taken.loc[courses_taken['c_category']== 'A','c_credits'].values)) )
    catB = sum(list(map(int,courses_taken.loc[courses_taken['c_category']== 'B','c_credits'].values)) )
    catC = sum(list(map(int,courses_taken.loc[courses_taken['c_category']== 'C','c_credits'].values)) )
    psyc = sum(list(map(int,courses_taken.loc[courses_taken['psych']== '1','c_credits'].values)) )
    subs = sum(list(map(int,courses_taken.loc[courses_taken['subs']== '1','c_credits'].values)))
    phd = sum(list(map(int,courses_taken['c_credits'].values)))

    no_catA = len(list(map(int,courses_taken.loc[courses_taken['c_category']=='A','c_credits'].values)))
    no_catB = len(list(map(int,courses_taken.loc[courses_taken['c_category']=='B','c_credits'].values)))

    if no_catA >=3:
        if '616' in c_numbers:
            res['area_requirements'] = ["Category A Requirements Met"]
        else:
            res['area_requirements'] = ["PSYC 616 Required"]
    else:
        if '616' not in c_numbers:
            res['area_requirements'] = ["PSYC 616 Required"]
            if 2-no_catA > 0:
                res['area_requirements'].append( str(2-no_catA) + " Category A Courses Required")
            else:
                res['area_requirements'].append("Category A Requirements Met")
        else:
            res['area_requirements'] = [str(3-no_catA) + " Category A Courses Required"]
            res['area_requirements'].append( "PSYC 616 Requirement met")
   
    if no_catB >= 1:
        res['area_requirements'].append("Category B Requirements Met")
    else:
        res['area_requirements'].append("1 Category B Course Required")
    count=0
    count = cc_numbers.count('612')
    if count>=3:
        if '512' in c_numbers:
            res['area_requirements'].append("Category C Requirements Met")
        else:
            res['area_requirements'].append("PSYC 512 Course Required")
    else:
        if '512' not in c_numbers:
            res['area_requirements'].append("PSYC 512 Course Required")
        res['area_requirements'].append("PSYC 612 courses required [3]")

    res['A'] = 8 - catA if catA < 8 else 0
    res['B'] = 4-catB if catB <4 else 0  
    res['C'] = 4-catC if catC <4 else 0
    res['BC'] = 16 - (catB+ catC) if (catB+ catC) < 16 else 0
    res['phd'] = 60 - phd if phd < 60 else 0
    res['subs'] = 36 - subs if subs < 36 else 0
    res['psyc'] = 24 - psyc if psyc < 24 else 0

    return res

def getCourseList(student_info):
    courses_taken = []
    for year in student_info['years']:
        semester = ['fall','spring','summer']
        for sem in semester:
            for course_in_sem in student_info[year][sem]:
                courses_taken.append(course_in_sem)
    
    return pd.DataFrame(courses_taken)

def score(student_info):
    courses_taken = getCourseList(student_info)
    if courses_taken.empty== False:

        if student_info['major'] == 'Brain Cognitive Sciences':
            return bcs(courses_taken)
        if student_info['major'] == 'Developmental Psychology':
            return dp(courses_taken)
        if student_info['major'] == 'Social Psychology':
            return socialp(courses_taken)
        if student_info['major'] == 'Quantitative Psychology':
            return quantp(courses_taken)
    return 0
