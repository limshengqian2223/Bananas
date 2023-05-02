from flask import Flask, render_template, request
from storage import *
#balls
#import from storage next time

app = Flask(__name__)

sc = StudentCollection('capstone.db', 'student')
cc = CCACollection('capstone.db', 'cca')
ac = ActivityCollection('capstone.db', 'activity')
sct = StudentCCATable('capstone.db')
sat = StudentActivityTable('capstone.db')

@app.route('/')
def index():
    """
    Landing Page - Not much
    -Documentation for first time users
    """
    return render_template('index.html')

@app.route('/new_student', methods=['GET','POST'])
def new_student():
    """ 
    Require: None
    Pass to DB: name, age. year enroll, grad year, class, student_subject (seperate table) (Inserting by DB)
    """
    if "registered" in request.args:
        record = dict(request.form)
        # student_name=request.form['student_name']
        # student_age=request.form['student_age']
        # student_class=request.form['student_age']
        # student_grad_year=request.form['student_grad_year']
        # student_year_enrolled=request.form['student_year_enrolled']

        # record = {'student_name':student_name,
        #                'student_age':student_age,
        #                'student_class':student_class,
        #                'student_grad_year':student_grad_year,
        #                'student_year_enrolled':student_year_enrolled}
        if sc.insert(record):
            return render_template('student_info.html',
                                  page_type='confirmed_student',
                                  student_info=record)
        else:
            return render_template('student_info.html',
                                  page_type='insert_student_fail',
                                  student_info=record)
        
    return render_template('student_info.html',
                          page_type='new_student',
                          title='CRM - Add New Student',
                          form_meta={'action':'/new_student?registered',
                                    'method':'post'},
                          form_data={"student_name":'',
                                    "student_class":'',
                                     "student_age":'',
                                    "student_grad_year":"",
                                    "student_year_enrolled":''})

@app.route('/new_student_cca', methods=['GET','POST'])
def new_student_cca():
    """
    Require: None
    Pass to DB: student's cca (Inserting by DB)

    Use students name to add in their cca
    """
    if "registered" in request.args:
        record = dict(request.form)
        # student_name=request.form['student_name']
        # student_cca=request.form['student_cca']
        # student_role=request.form['student_role']

        # record = {'student_name':student_name,
        #          'student_cca':student_cca,
        #          'student_role':student_role}

        if sct.insert(record):
            return render_template('student_info.html',
                                  page_type='confirmed_student_cca',
                                  student_info=record)
        else:
          return render_template('student_info.html',
                                  page_type='insert_student_cca_fail',
                                  student_info=record)
            
        
    return render_template('student_info.html',
                          page_type='new_student_cca',
                          title='CRM - Add New Student CCA',
                          form_meta={'action':'/new_student_cca?registered',
                                    'method':'post'},
                            form_data={'student_name':'',
                                      'student_cca':''})
                                      #'student_role':''})

@app.route('/new_student_activity', methods=['GET','POST'])
def new_student_activity():
    """
    Require: None
    Pass to DB: student's activity (Inserting by DB)

    Use students name to add in their activity
    """
    if "registered" in request.args:
        record = dict(request.form)
        
        # student_name = request.form['student_name']
        # student_activity = request.form['student_activity']
        # student_role = request.form['student_role']
        # student_award = request.form['student_award']
        # student_hours = request.form['student_hours']

        # record = {'student_name':student_name,
        #          'student_activity':student_activity,
        #          'student_role':student_role,
        #          'student_award':student_award,
        #          'student_hours':student_hours}

        if sat.insert(record):
            return render_template('student_info.html',
                                page_type='confirmed_student_activity',
                                student_info=record)
        else:
            return render_template('student_info.html',
                                  page_type='insert_activity_fail',
                                  student_info=record)
        
    return render_template('student_info.html',
                          page_type='new_student_activity',
                          title='CRM - Add New Student Activity',
                          form_meta={'action':'/new_student_activity?registered',
                                    'method':'post'},
                           form_data={'student_name':'',
                                     'student_activity':'',
                                     'student_role':'',
                                     'student_award':'',
                                     'student_hours':''})

@app.route('/new_cca', methods=['GET','POST'])
def new_cca():
    """
    Require: None
    Pass to DB: name, type (Insert by DB)
    """
    if 'registered' in request.args:
        cca_name=request.form['cca_name']
        cca_type=request.form['cca_type']

        cca={'cca_name':cca_name,
            'cca_type':cca_type}
        if cc.insert(cca):
            return render_template('new_cca_activity.html',
                                   title='Add CCA Success',
                                  page_type='new_cca_registered',
                                  cca=cca)
        else:
            return render_template('new_cca_activity.html',
                                  page_type="add_cca_fail",
                                  cca=cca)
        
    return render_template('new_cca_activity.html',
                           title='Add New CCA',
                          page_type='new_cca',
                          form_meta={'action':'/new_cca?registered',
                          'method':'post'},
                          form_data={'cca_name':''})

@app.route('/new_activity', methods=['GET', 'POST'])
def new_activity():
    """
    Require: None
    Pass to DB: (Insert by DB)
    coordinated by who
    category:str{Achievement, Enrichment, Leadership, Service}
    
    """
    if 'registered' in request.args:
        activity = dict(request.form)
        print(activity)
        # activity_name=request.form['activity_name']
        # cca_name=request.form['cca_name']
        # activity_cat=request.form['activity_cat']
        # activity_sd=9
        # activity_ed=9
        # activity_desc=9

        # activity={'activity_name':activity_name,
        #           'cca_name':cca_name,
        #           'activity_cat':activity_cat}

        if ac.insert(activity):
            return render_template('new_cca_activity.html',
                                   title='Add Activity Success',
                                  page_type='new_activity_registered',
                                  activity=activity)
        else:
            return render_template('new_cca_activity.html',
                                  page_type="add_activity_fail",
                                  activity=activity)
        
    return render_template('new_cca_activity.html',
                           title='Add New Activity',
                          page_type='new_activity',
                          form_meta={'action':'/new_activity?registered',
                          'method':'post'},
                          form_data={'activity_name':'',
                                    'activity_coordinator':'',
                                    'activity_desc':''})

@app.route('/view_student_cca', methods=['GET', 'POST'])
def view_student_cca():
    """
    Require: student's cca (Finding by backend)

    user pass in: student name
    """
    # breakpoint()
    if request.method=="GET":

        return render_template('view_info.html',
                              title='View Student CCA',
                                page_type='view_cca',
                              form_meta={'action':'/view_student_cca',
                                        'method':'post'},
                              form_data={'student_name':''})
        
    if request.method=="POST":
        name=request.form["student_name"]
        
        record = sct.find(name)
        student_name = record[0]['student name']
        class_ = record[0]['student class']
        print(record)

        cca_list = []
        role_list = []
        for indiv in record:
            cca_list.append(indiv['cca name'])
            role_list.append(indiv['role'])
        # print(cca_list)
        
        return render_template('view_info.html',
                              title='View CCA',
                              page_type='view_cca_info',
                              cca_record=cca_list,
                              role_record=role_list,
                              name = student_name,
                              class_=class_)

    


@app.route('/view_student_activity', methods=['GET','POST'])
def view_student_activity():
    """
    Require: student's activities (Find by backend)

    pass in : name
    """
    if request.method == 'GET':
        return render_template('view_info.html',
                              title='View Student Activity',
                                page_type='view_activity',
                              form_meta={'action':'/view_student_activity',
                                        'method':'post'},
                              form_data={'student_name':''})

    if request.method == 'POST':
        name=request.form["student_name"]
        
        record = sat.find(name)
        student_name = record[0]['student name']
        class_ = record[0]['student class']
        # print(record)

        activity_list = []
        role_list = []
        award_list = []
        hours_list = []
        
        for indiv in record:
            activity_list.append(indiv['cca name'])
            role_list.append(indiv['role'])
            award_list.append(indiv['award'])
            hours_list.append(indiv['hours'])
        # print(cca_list)
        
        return render_template('view_info.html',
                              title='View rubbish',
                              page_type='view_activity_info',
                              cca_record=cca_list,
                              role_record=role_list,
                              award_record=award_list,
                              hours_record=hours_list,
                              name = student_name,
                              class_=class_)
        
@app.route('/edit_student', methods=['GET','POST'])
def edit_student():
    """
    Require: Student record (Find by backend)

    Pass to DB :edited student Record (Update by DB)
    """
    if request.method == 'GET':
        return render_template('edit_info.html',
                              page_type='edit_student_empty',
                              form_meta={'action':'/edit_student',
                                        'method':'post'},
                               form_data={'name':''})
    elif request.method == 'POST':
        # breakpoint()
        if 'registered' in request.args:
            record = dict(request.form)
            prev_name = record['prev_name']
            del record['prev_name']
            # sc.update(prev_name, record)

            return render_template('edit_info.html',
                                  page_type='edit_student_success',
                                  record = record)
            
        name = request.form['name']
        if sc.find(name) is not None:
            # print(record)
            record = sc.find(name)
            del record['id']
            return render_template('edit_info.html',
                              page_type='edit_student_details',
                              form_meta={'action':'/edit_student?registered',
                                        'method':'post'},
                                  form_data=record,
                                  prev_name=record['name'])
            
        else:
            return render_template('edit_info.html',
                                  page_type='edit_student_empty',
                                  form_meta={'action':'/edit_student',
                                            'method':'post'},
                                  form_data={'name':''},
                                  error='This Student does not exists!')        


@app.route('/edit_membership', methods=['GET','POST'])
def edit_membership():
    """
    Require: Student CCA record (Find by backend)
    
    pass in: edited student CCA record (Update by DB)
    """
    if request.method == 'GET':
        return render_template('edit_info.html',
                              page_type='edit_membership_empty',
                              form_meta={'action':'/edit_membership',
                                        'method':'post'},
                               form_data={'name':''})
    elif request.method == 'POST':
        # breakpoint()
        if 'registered' in request.args:
            record = dict(request.form)
            # prev_name = record['prev_name']
            # del record['prev_name']
            # sct.update(record['name'], record)

            return render_template('edit_info.html',
                                  page_type='edit_membership_success',
                                  record = record)
            
        name = request.form['name']
        if sct.find(name) is not None:
            # breakpoint()
            # print(record)
            record = sct.find(name)
            print(record)
            cca_list = []
            for indiv in record:
                cca_list.append(indiv['cca name'])
            name = record[0]['student name']
            class_ = record[0]['student class']
                
            if 'edit' in request.args:
                # breakpoint()
                # print(request.args)
                return render_template('edit_info.html',
                                  page_type='edit_indiv_membership_details',
                                  form_meta={'action':'/edit_membership?registered',
                                            'method':'post'},
                                    form_data={'student_name':name})
            
            return render_template('edit_info.html',
                                  page_type='edit_membership_choose',
                                  record = cca_list,
                                  name = name,
                                  class_ = class_)
            
        else:
            return render_template('edit_info.html',
                                  page_type='edit_membership_empty',
                                  form_meta={'action':'/edit_membership',
                                            'method':'post'},
                                  form_data={'name':''},
                                  error='This Student does not exists!')

@app.route('/edit_participation', methods=['GET','POST'])
def edit_participation():
    """
    pass in: edited student activity record (Find by DB)
    
    Require: Student activity record (Update by DB)
    """
    return render_template('edit_info.html',
                          page_type='edit_participation_empty',
                          form_meta={'action':'/edit_participation',
                                    'method':'post'},
                           form_data={'name':''})
    

@app.route('/delete_student', methods=['GET', 'POST'])
def delete_student():
    if request.method == 'GET':
        return render_template('delete_details.html',
                              page_type='delete_student_empty',
                              form_meta={'action':'/delete_student',
                                        'method':'post'},
                              form_data={'name':''})
    elif request.method == 'POST':
        name = request.form['name']
        if sc.delete(name) is None:
            return render_template('delete_details.html',
                                  page_type='delete_student_success',
                                  name=name)
        else:
            return render_template('delete_details.html',
                                  page_type='delete_student_empty',
                                  form_meta={'action':'/delete_student',
                                            'method':'post'},
                                  form_data={'name':''},
                                  error='This student does not exists! Try again.')

@app.route('/delete_student_cca', methods=['GET', 'POST'])
def delete_student_cca():
    if request.method == 'GET':
        return render_template('delete_details.html',
                              page_type='delete_student_cca_empty',
                              form_meta={'action':'/delete_student_cca',
                                        'method':'post'},
                              form_data={'name':''})

    elif request.method == 'POST':
        name = request.form['name']
        # go = False
        # if go:
        if sct.delete(name) is None:
            return render_template('delete_details.html',
                                  page_type='delete_student_cca_success',
                                  name=name)
        else:
            return render_template('delete_details.html',
                                  page_type='delete_student_cca_empty',
                                  form_meta={'action':'/delete_student_cca',
                                            'method':'post'},
                                  form_data={'name':''},
                                  error='This student does not exists! Try again.')

@app.route('/delete_student_activity', methods=['GET', 'POST'])
def delete_student_activity():
    if request.method == 'GET':
        return render_template('delete_details.html',
                              page_type='delete_student_activity_empty',
                              form_meta={'action':'/delete_student_activity',
                                        'method':'post'},
                              form_data={'name':''})
    elif request.method == 'POST':
        name = request.form['name']
        if sat.delete(name) is None:
            return render_template('delete_details.html',
                                  page_type='delete_student_activity_success',
                                  name=name)
        else:
            return render_template('delete_details.html',
                                  page_type='delete_student_activity_empty',
                                  form_meta={'action':'/delete_student_activity',
                                            'method':'post'},
                                  form_data={'name':''},
                                  error='This student does not exists! Try again.')
            
@app.route('/delete_cca', methods=['GET', 'POST'])
def delete_cca():
    if request.method == 'GET':
        return render_template('delete_details.html',
                              page_type='delete_cca_empty',
                              form_meta={'action':'/delete_cca',
                                        'method':'post'},
                              form_data={'cca_name':''})
    elif request.method == 'POST':
        name = request.form['name']
        if cc.delete(name) is None:
            return render_template('delete_details.html',
                                  page_type='delete_cca_success',
                                  name=name)
        else:
            return render_template('delete_details.html',
                                  page_type='delete_cca_empty',
                                  form_meta={'action':'/delete_cca',
                                            'method':'post'},
                                  form_data={'name':''},
                                  error='This CCA does not exists! Try again.')

@app.route('/delete_activity', methods=['GET', 'POST'])
def delete_activity():
    if request.method == 'GET':
        return render_template('delete_details.html',
                              page_type='delete_activity_empty',
                              form_meta={'action':'/delete_activity',
                                        'method':'post'},
                              form_data={'activity_name':''})
    elif request.method == 'POST':
        name = request.form['name']
        if ac.delete(name) is None:
            return render_template('delete_details.html',
                                  page_type='delete_activity_success',
                                  name=name)
        else:
            return render_template('delete_details.html',
                                  page_type='delete_activity_empty',
                                  form_meta={'action':'/delete_activity',
                                            'method':'post'},
                                  form_data={'name':''},
                                  error='This activity does not exists! Try again.')