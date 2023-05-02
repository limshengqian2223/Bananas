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
        activity_name=request.form['activity_name']
        cca_name=request.form['cca_name']
        activity_cat=request.form['activity_cat']
        activity_sd=9
        activity_ed=9
        activity_desc=9

        activity={'activity_name':activity_name,
                  'cca_name':cca_name,
                  'activity_cat':activity_cat}

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
                                    'activity_coordinator':''})


@app.route('/view_student_profile', methods=['GET'])
def view_student_profile():
    """
    Require:
    1. student's name
    2. student's class
    3. student's subjects
    4. activities which the student has participated in
    5. CCAs which the studet has participated in.

    user pass in: Student's name whose profile they wish to find.
    """

    # Page 1, where users enter student name to find his/her records and profile
    if dict(request.args) == {}:
        return render_template('view_info.html',
                              title="View Student Profile",
                              page_type="find_student_profile",
                              form_meta={
                                  'action': '/view_student_profile',
                                  'method': 'get'
                              },
                              form_data={
                                  'student_name':''
                              },
                              error=None)
    else:
        form = dict(request.args)
        student_name = form["student_name"]
        
        # if student exists in the db
        if sc.find_by_name(student_name) is not None:
            student_record = sc.find_by_name(student_name)

            #the following few pop operations are to remove non essential fields from being displayed to the user.
            student_record.pop("id")

            student_cca_record = sct.find_by_name(student_name)
            student_activity_record = sat.find_by_name(student_name)

            if student_cca_record is not None:
                for record in student_cca_record:
                    record.pop("student class")
                    record.pop("student name")
                    
            if student_activity_record is not None:
                for record in student_activity_record:
                    record.pop("student class")
                    record.pop("student name")

            return render_template('view_info.html',
                                  title="View Student Profile",
                                  page_type="show_student_profile",
                                  student_record=student_record,
                                  student_cca_record=student_cca_record,
                                  student_activity_record=student_activity_record)
            

        # student does not exist in the db
        else:
            return render_template('view_info.html',
                                  title = "View Student Profile",
                                  page_type="find_student_profile",
                                  form_meta={
                                      'action': '/view_student_profile',
                                      'method': 'get'
                                  },
                                  form_data={
                                      'student_name': ''
                                  },
                                  error="student_not_found")


@app.route('/view_by_class', methods=['GET'])
def view_by_class():
    """
    Require: All the names of students in a given class

    user pass in: class name
    """
    if dict(request.args) == {}:
        return render_template('view_info.html',
                              title="View students in a class ",
                              page_type='find_class_profile',
                              form_meta={
                                  'action': '/view_by_class',
                                  'method': 'get'
                              },
                              form_data={
                                  'class_name':''
                              },
                              error=None)
    else:
        form = dict(request.args)
        class_name = form["class_name"]
        
        #NEED TO CHECK IF A CLASS EXISTS!
        # from pprint import pprint
        # list_of_students = sc.find_by_class(class_name)
        # pprint(list_of_students)

        # if sc.find_by_class(class_name)

        return render_template('view_info.html',
                              page_type="show_class_profile",
                              title="Show class profile",
                              list_of_students=list_of_students
                              )
        


@app.route('/view_by_cca', methods=['GET'])
def view_by_cca():
    """
    Require: All the names of students in given CCA

    user pass in: cca name
    """
    if dict(request.args) == {}:
        return render_template('view_info.html',
                              title='View by CCA',
                                page_type='find_cca_profile',
                              form_meta={'action':'/view_by_cca',
                                        'method':'get'},
                              form_data={'cca_name':''},
                              error=None)

    else:
        form = dict(request.args)
        cca_name = form["cca_name"]
        
        # If cca exists. 
        if (cc.find_by_name(cca_name)):
            
            list_of_members = sct.find_by_cca(cca_name)
            
            cca_info = cc.find_by_name(cca_name)
            if cca_info is not None:
                cca_info.pop("id")
            print(list_of_members)
            return render_template('view_info.html',
                                  title="Show CCA profile",
                                  page_type="show_cca_profile",
                                   cca_info=cca_info,
                                  list_of_members=list_of_members)

        else:
            return render_template('view_info.html',
                              title='View by CCA',
                                page_type='find_cca_profile',
                              form_meta={'action':'/view_by_cca',
                                        'method':'get'},
                              form_data={'cca_name':''},
                              error="cca_not_found")

    


@app.route('/view_student_activity', methods=['GET','POST'])
def view_student_activity():
    """
    Require: student's activities (Find by backend)

    pass in : name
    """
    return render_template('view_info.html',
                          title='View Student Activity',
                            page_type='view_activity',
                          form_meta={'action':'/view_student_activity',
                                    'method':'post'},
                          form_data={'student_name':''})
    
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
    return render_template('edit_info.html',
                          page_type='edit_membership_empty',
                          form_meta={'action':'/edit_membership',
                                    'method':'post'},
                           form_data={'name':''})

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