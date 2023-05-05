from flask import Flask, render_template, request
from storage import *
from helper_function import empty_fields
#balls
#import from storage next time

app = Flask(__name__)

sc = StudentCollection('capstone.db', 'student')
cc = CCACollection('capstone.db', 'cca')
ac = ActivityCollection('capstone.db', 'activity')
sct = StudentCCATable('capstone.db')
sat = StudentActivityTable('capstone.db')

class_list = [
        '2201', '2202', '2203', '2204', '2205', '2206', '2207', '2208', '2209',
        '2210', '2211', '2212', '2213', '2214', '2215', '2216', '2217', '2218',
        '2219', '2220', '2221', '2222', '2223', '2224', '2225', '2226', '2227',
        '2228', '2229', '2230', '2301', '2302', '2303', '2304', '2305', '2306',
        '2307', '2308', '2309', '2310', '2311', '2312', '2313', '2314', '2315',
        '2316', '2317', '2318', '2319', '2320', '2321', '2322', '2323', '2324',
        '2325', '2326', '2327', '2328', '2329', '2330'
    ]


@app.route('/')
def index():
    """
    Landing Page - Not much
    -Documentation for first time users
    """
    return render_template('index.html')


@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    """ 
    Require: None
    Pass to DB: name, age. year enroll, grad year, class, student_subject (seperate table) (Inserting by DB)
    """
    list_empty_fields= None
    if "registered" in request.args:
        record = dict(request.form)
        # print(record) 

        list_empty_fields = empty_fields(record)
        if list_empty_fields:
            return render_template('student_info.html',
                                   page_type='insert_student_fail',
                                   student_info=record,
                                   title="Add New Student - Fail",
                                   error='There are empty fields',
                                   empty_fields=list_empty_fields)
        
        
        if sc.insert(record):
            del record['class_id']
            return render_template('student_info.html',
                                   page_type='confirmed_student',
                                   student_info=record,
                                   title='Add New Student - Success')
        else:
            return render_template('student_info.html',
                                   page_type='insert_student_fail',
                                   student_info=record,
                                   title="Add New Student - Fail",
                                  error="Student Already Exists!")

    return render_template('student_info.html',
                           page_type='new_student',
                           title='Add New Student',
                           form_meta={
                               'action': '/new_student?registered',
                               'method': 'post'
                           },
                           form_data={
                               "student_name": '',
                               "student_age": '',
                               "student_year_enrolled": '',
                               "student_grad_year": ''
                           },
                           class_list=class_list)


@app.route('/new_student_cca', methods=['GET', 'POST'])
def new_student_cca():
    """
    Require: None
    Pass to DB: student's cca (Inserting by DB)

    Use students name to add in their cca
    """
    list_empty_fields = None
    if "registered" in request.args:
        record = dict(request.form)
        
        list_empty_fields = empty_fields(record)
        if list_empty_fields:
            return render_template('student_info.html',
                                   page_type='insert_student_cca_fail',
                                   student_info=record,
                                   title="Add New Student CCA - Fail",
                                   error='empty_fields',
                                   empty_fields=list_empty_fields)
            
        status, message = sct.insert(record)
        if status:
            del record['student_id']
            del record['cca_id']
            return render_template('student_info.html',
                                   page_type='confirmed_student_cca',
                                   student_info=record,
                                   error=None,
                                   title="Add Student Membership - Success")
        else:
            return render_template('student_info.html',
                                   page_type='insert_student_cca_fail',
                                   student_info=record,
                                   error=message,
                                   title="Add Student Membership - Fail")

    return render_template('student_info.html',
                           page_type='new_student_cca',
                           title='CRM - Add New Student CCA',
                           form_meta={
                               'action': '/new_student_cca?registered',
                               'method': 'post'
                           },
                           form_data={
                               'student_name': '',
                               'student_cca': ''
                           },
                           error=None)


@app.route('/new_student_activity', methods=['GET', 'POST'])
def new_student_activity():
    """
    Require: None
    Pass to DB: student's activity (Inserting by DB)

    Use students name to add in their activity
    """
    list_empty_fields = None
    
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

        list_empty_fields = empty_fields(record)
        if list_empty_fields:
            return render_template('student_info.html',
                                   page_type='insert_student_activity_fail',
                                   student_info=record,
                                   title="Add New Student Activity - Fail",
                                   error='empty_fields',
                                   empty_fields=list_empty_fields)
            
        status, message = sat.insert(record)
        if status:
            del record['student_id']
            del record["activity_id"]
            return render_template('student_info.html',
                                   page_type='confirmed_student_activity',
                                   student_info=record,
                                   error=None,
                                   title="Add New Student Activity - Success")
        else:
            return render_template('student_info.html',
                                   page_type='insert_student_activity_fail',
                                   student_info=record,
                                   error=message,
                                   title="Add New Student Activity - Fail")

    return render_template('student_info.html',
                           page_type='new_student_activity',
                           title='Add New Student Activity',
                           form_meta={
                               'action': '/new_student_activity?registered',
                               'method': 'post'
                           },
                           form_data={
                               'student_name': '',
                               'student_activity': '',
                               'student_role': '',
                               'student_award': '',
                               'student_hours': ''
                           })


@app.route('/new_cca', methods=['GET', 'POST'])
def new_cca():
    """
    Require: None
    Pass to DB: name, type (Insert by DB)
    """
    list_empty_fields = None
    if 'registered' in request.args:
        cca_name = request.form['cca_name']
        cca_type = request.form['cca_type']

        cca = {'cca_name': cca_name, 'cca_type': cca_type}

        record = dict(request.form)
        
        list_empty_fields = empty_fields(record)
        if list_empty_fields:
            return render_template('new_cca_activity.html',
                                   page_type='add_cca_fail',
                                   cca=cca,
                                   title="Add New CCA - Fail",
                                   error='empty_fields',
                                   empty_fields=list_empty_fields)     
        
        if cc.insert(cca):
            return render_template('new_cca_activity.html',
                                   title='Add CCA - Success',
                                   page_type='new_cca_registered',
                                   cca=cca)
        else:
            return render_template('new_cca_activity.html',
                                   page_type="add_cca_fail",
                                   cca=cca,
                                   title="Add CCA - Fail",
                                  error='already_exist')

    return render_template('new_cca_activity.html',
                           title='Add New CCA',
                           page_type='new_cca',
                           form_meta={
                               'action': '/new_cca?registered',
                               'method': 'post'
                           },
                           form_data={'cca_name': ''})


@app.route('/new_activity', methods=['GET', 'POST'])
def new_activity():
    """
    Require: None
    Pass to DB: (Insert by DB)
    coordinated by who
    category:str{Achievement, Enrichment, Leadership, Service}
    
    """
    list_empty_fields = None
    if 'registered' in request.args:
        activity = dict(request.form)
        # print(activity)
        # activity_name=request.form['activity_name']
        # cca_name=request.form['cca_name']
        # activity_cat=request.form['activity_cat']
        # activity_sd=9
        # activity_ed=9
        # activity_desc=9

        # activity={'activity_name':activity_name,
        #           'cca_name':cca_name,
        #           'activity_cat':activity_cat}

        list_empty_fields = empty_fields(activity)
        if list_empty_fields:
            return render_template('new_cca_activity.html',
                                   page_type='add_activity_fail',
                                   activity=activity,
                                   title="Add New Activity - Fail",
                                   error='empty_fields',
                                   empty_fields=list_empty_fields)     

        
        if ac.insert(activity):
            activity['activity_end_date'] = activity.pop('activity_sd')
            activity['activity_start_date'] = activity.pop('activity_ed')
            activity['activity_category'] = activity.pop('activity_cat')
            del activity['cca_id']
            del activity["ac"]
            return render_template('new_cca_activity.html',
                                   title='Add Activity - Success',
                                   page_type='new_activity_registered',
                                   activity=activity)
        else:
            return render_template('new_cca_activity.html',
                                   page_type="add_activity_fail",
                                   activity=activity,
                                   title="Add New Activity - Fail",
                                  error='already_exist')

    return render_template('new_cca_activity.html',
                           title='Add New Activity',
                           page_type='new_activity',
                           form_meta={
                               'action': '/new_activity?registered',
                               'method': 'post'
                           },
                           form_data={
                               'activity_name': '',
                               'cca_name': '',
                               'activity_desc': ''
                           })


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
                               form_data={'student_name': ''},
                               error=None)
    else:
        form = dict(request.args)
        student_name = form["student_name"]

        # if student exists in the db
        if sc.find_by_name(student_name) is not None:
            student_record = sc.find_by_name(student_name)

            #the following few pop operations are to remove non essential fields from being displayed to the user.
            student_record.pop("id")
            # print(student_record)
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

            # Final page to display everything about the student
            return render_template(
                'view_info.html',
                title="View Student Profile",
                page_type="show_student_profile",
                student_record=student_record,
                student_cca_record=student_cca_record,
                student_activity_record=student_activity_record)

        # student does not exist in the db
        else:
            return render_template('view_info.html',
                                   title="View Student Profile",
                                   page_type="find_student_profile",
                                   form_meta={
                                       'action': '/view_student_profile',
                                       'method': 'get'
                                   },
                                   form_data={'student_name': ''},
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
                               form_data={'class_name': ''},
                               error=None,
                              class_list=class_list)
    else:
        form = dict(request.args)
        class_name = form["class_name"]
                   
        list_of_students = sc.find_by_class(int(class_name))

        if sc.find_by_class(class_name):

            # band-aid fix. If only one student is in the class, backend returns a dictionary
            # instead of a list. dictionary cannot be iterated and students in the class are
            # not displayed
            if type(list_of_students) == dict:
                list_of_students = [list_of_students]
            return render_template('view_info.html',
                                   page_type="show_class_profile",
                                   title="Show class profile",
                                   list_of_students=list_of_students,
                                   error=None)
        else:
            return render_template('view_info.html',
                                   title="View students in a class ",
                                   page_type='find_class_profile',
                                   form_meta={
                                       'action': '/view_by_class',
                                       'method': 'get'
                                   },
                                   form_data={'class_name': ''},
                                   error="class_no_records",
                                  class_list=class_list)


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
                               form_meta={
                                   'action': '/view_by_cca',
                                   'method': 'get'
                               },
                               form_data={'cca_name': ''},
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
                                   form_meta={
                                       'action': '/view_by_cca',
                                       'method': 'get'
                                   },
                                   form_data={'cca_name': ''},
                                   error="cca_not_found")


@app.route('/view_by_activity', methods=['GET'])
def view_by_activity():
    """
    Require: All the names of students in given activity

    user pass in: activity name
    """
    if dict(request.args) == {}:
        # Page 1. For user to enter activity name of activty they wish to view
        return render_template('view_info.html',
                               title='View by Activity',
                               page_type='find_activity_profile',
                               form_meta={
                                   'action': '/view_by_activity',
                                   'method': 'get'
                               },
                               form_data={'activity_name': ''},
                               error=None)

    else:
        form = dict(request.args)
        activity_name = form["activity_name"]

        # If cca exists.
        if (ac.find_by_name(activity_name)):

            list_of_members = sat.find_by_activity(activity_name)

            activity_info = ac.find_by_name(activity_name)
            if activity_info is not None:
                activity_info.pop("id")
            print(activity_info)
            return render_template('view_info.html',
                                   title="Show Activity profile",
                                   page_type="show_activity_profile",
                                   activity_info=activity_info,
                                   list_of_members=list_of_members)

        # If cca doest not exist
        else:
            return render_template('view_info.html',
                                   title='View by CCA',
                                   page_type='find_activity_profile',
                                   form_meta={
                                       'action': '/view_by_activity',
                                       'method': 'get'
                                   },
                                   form_data={'activity_name': ''},
                                   error="activity_not_found")


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    """
    Require: Student record (Find by backend)

    Pass to DB :edited student Record (Update by DB)
    """
    if request.method == 'GET':
        return render_template('edit_info.html',
                               page_type='edit_student_empty',
                               form_meta={
                                   'action': '/edit_student',
                                   'method': 'post'
                               },
                               form_data={'name': ''},
                               title="Edit Student Record")
    elif request.method == 'POST':
        if 'registered' in request.args:
            record = dict(request.form)
            prev_name = record['prev_name']
            del record['prev_name']

            status, message = sc.update(prev_name, record)
            if status:
                # all clear
                # remove unnecessary fields from being displayed
                del record["student_class_id"]
                return render_template('edit_info.html',
                                       page_type='edit_student_success',
                                       record=record,
                                       title="Edit Student Record - Success")
            else:
                # new class doesnt exist. autofill to previous state
                # command directly below is to re-obtain the original student class.
                record["student_class"] = sc.find_by_name(
                    record["student_name"])["class"]
                print(record)
                
            list_empty_fields = None   
            list_empty_fields = empty_fields(record)
            if list_empty_fields:          
                return render_template('student_info.html',
                                       page_type='edit_student_details',
                                       student_info=record,
                                       title="Add New Student - Fail",
                                       error='empty_fields',
                                       empty_fields=list_empty_fields)
                
                return render_template('edit_info.html',
                                       page_type='edit_student_details',
                                       form_meta={
                                           'action':
                                           '/edit_student?registered',
                                           'method': 'post'
                                       },
                                       form_data={
                                           "student_name":
                                           record["student_name"],
                                           "student_class":
                                           record["student_class"],
                                           "student_age":
                                           record["student_age"],
                                           "student_year_enrolled":
                                           record["student_year_enrolled"],
                                           "student_grad_year":
                                           record["student_grad_year"]
                                       },
                                       prev_name=record["student_name"],
                                       error=message,
                                       class_list=class_list,
                                       title="Edit Student Details")

        name = request.form['name']
        if sc.find_by_name(name) is not None:
            
            # student exists
            record = sc.find_by_name(name)
            del record['id']
            return render_template('edit_info.html',
                                   page_type='edit_student_details',
                                   form_meta={
                                       'action': '/edit_student?registered',
                                       'method': 'post'
                                   },
                                   form_data={
                                       "student_name":
                                       record["name"],
                                       "student_class":
                                       str(record["class"]),
                                       "student_age":
                                       record["age"],
                                       "student_year_enrolled":
                                       record["year enrolled"],
                                       "student_grad_year":
                                       record["graduating year"]
                                   },
                                   class_list=class_list,
                                   prev_name=record['name'],
                                   title="Edit Student Details")

        else:
            # student does not exist
            return render_template('edit_info.html',
                                   page_type='edit_student_empty',
                                   form_meta={
                                       'action': '/edit_student',
                                       'method': 'post'
                                   },
                                   form_data={'name': ''},
                                   error='This Student does not exists!',
                                   title="Edit Student Details")


@app.route('/edit_membership', methods=['GET', 'POST'])
def edit_membership():
    """
    Require: Student CCA record (Find by backend)
    
    pass in: edited student CCA record (Update by DB)
    """
    if request.method == 'GET':
        # Page 1: Where users enter the student name to see all the records which can be editted
        if dict(request.args) == {}:
            return render_template('edit_info.html',
                                   page_type='edit_membership_empty',
                                   form_meta={
                                       'action': '/edit_membership',
                                       'method': 'post'
                                   },
                                   form_data={'name': ''},
                                   title="Edit Student CCA")

        elif "cca" in dict(request.args).keys():
            # Page 3: Users have selected which CCA record to edit.
            # Allowing users to edit the chosen CCA record
            args = dict(request.args)
            return render_template('edit_info.html',
                                   page_type='edit_indiv_membership_details',
                                   form_meta={
                                       'action': '/edit_membership?registered',
                                       'method': 'post'
                                   },
                                   form_data={
                                       'student_name': args["name"],
                                       'student_cca': args["cca"],
                                       'student_role': args["role"]
                                   },
                                   error=None,
                                   title="Edit Student CCA")
    elif request.method == 'POST':
        if 'registered' in request.args:
            record = dict(request.form)
            status, message = sct.update(record['student_name'],
                                         record["pre_student_cca"], record)

            if status:
                # all clear
                # removing unnecessary fields for user.
                del record["pre_student_cca"]
                return render_template('edit_info.html',
                                       page_type='edit_membership_success',
                                       record=record,
                                       title="Edit Student CCA - Success")
            else:
                # back to previous page. new cca provided doesnt exist
                return render_template(
                    'edit_info.html',
                    page_type='edit_indiv_membership_details',
                    form_meta={
                        'action': '/edit_membership?registered',
                        'method': 'post'
                    },
                    form_data={
                        'student_name': record['student_name'],
                        'student_cca': record['pre_student_cca']
                    },
                    error=message,
                    title="Edit Student CCA")

        # student name to find his/her records. Obtained from Page 1 form
        name = request.form['name']

        # if student has records
        if sct.find_by_name(name) is not None:
            records = sct.find_by_name(name)
            
            # cca_list = []
            # for indiv in record:
            #     cca_list.append(indiv['cca name'])
            name = records[0]['student name']
            class_ = records[0]['student class']

            # Page 2, displaying all the CCAs that the given student has joined
            # print(record)
            return render_template('edit_info.html',
                                   page_type='edit_membership_choose',
                                   records=records,
                                   name=name,
                                   class_=class_,
                                   title="Edit Student CCA")

        else:
            # student has no cca records
            return render_template('edit_info.html',
                                   page_type='edit_membership_empty',
                                   form_meta={
                                       'action': '/edit_membership',
                                       'method': 'post'
                                   },
                                   form_data={'name': ''},
                                   error='student_not_found',
                                   title="Edit Student CCA")


@app.route('/edit_participation', methods=['GET', 'POST'])
def edit_participation():
    """
    pass in: edited student activity record (Find by DB)
    
    Require: Student activity record (Update by DB)
    """

    if request.method == 'GET':
        # Page 1: Where users enter the student name to see all the records which can be editted
        # print(f"request.args: {dict(request.args)}")
        if (dict(request.args) == {}):
            return render_template('edit_info.html',
                                   page_type='edit_participation_empty',
                                   form_meta={
                                       'action': '/edit_participation',
                                       'method': 'post'
                                   },
                                   form_data={'name': ''},
                                   title="Edit Student Participation")

        elif "student_activity" in dict(request.args).keys():
            # Page 3: Users have selected which activity record to edit.
            # Allowing users to edit the chosen activity record
            args = dict(request.args)
            return render_template(
                'edit_info.html',
                page_type='edit_indiv_participation_details',
                form_meta={
                    'action': '/edit_participation?registered',
                    'method': 'post'
                },
                form_data=args,
                title="Edit Student Participation")
    elif request.method == 'POST':
        if 'registered' in request.args:
            record = dict(request.form)
            status, message = sat.update(record['student_name'],
                                         record['pre_student_activity'],
                                         record)
            if status:
                #all clear
                # removing unnecessary fields for user.
                del record["pre_student_activity"]
                return render_template('edit_info.html',
                                       page_type='edit_participation_success',
                                       record=record,
                                       title="Edit Student Participation")
            else:
                # back to previous page
                # print(record)
                record["student_activity"] = record["pre_student_activity"]
                return render_template(
                    'edit_info.html',
                    page_type='edit_indiv_participation_details',
                    form_meta={
                        'action': '/edit_participation?registered',
                        'method': 'post'
                    },
                    form_data=record,
                    error=message,
                    title="Edit Student Participation")

        # student name to find his/her records. Obtained from Page 1 form
        name = request.form['name']

        # if student has records
        if sat.find_by_name(name) is not None:
            record = sat.find_by_name(name)
            # print(record)

            name = record[0]["student name"]
            class_ = record[0]["student class"]
            # Page 2, displaying all the CCAs that the given student has joined
            return render_template('edit_info.html',
                                   page_type='edit_participation_choose',
                                   record=record,
                                   name=name,
                                   class_=class_,
                                   title="Edit Student Participation")

        else:
            # student has no cca records
            return render_template('edit_info.html',
                                   page_type='edit_participation_empty',
                                   form_meta={
                                       'action': '/edit_participation',
                                       'method': 'post'
                                   },
                                   form_data={'name': ''},
                                   error='student_not_found',
                                   title="Edit Student Participation")


@app.route('/delete_student', methods=['GET', 'POST'])
def delete_student():
    if request.method == 'GET':
        return render_template('delete_details.html',
                               page_type='delete_student_empty',
                               form_meta={
                                   'action': '/delete_student',
                                   'method': 'post'
                               },
                               form_data={'name': ''},
                               title="Delete Student")

    elif request.method == 'POST':
        name = request.form['name']
        if sc.delete(name):
            return render_template('delete_details.html',
                                   page_type='delete_student_success',
                                   name=name,
                                   title='Delete Student - Success')
        else:
            return render_template(
                'delete_details.html',
                page_type='delete_student_empty',
                form_meta={
                    'action': '/delete_student',
                    'method': 'post'
                },
                form_data={'name': ''},
                error='This student does not exists! Try again.',
                title="Delete Student")


@app.route('/delete_student_cca', methods=['GET', 'POST'])
def delete_student_cca():
    if request.method == 'GET':
        # print(dict(request.args))
        request_args = dict(request.args)
        print(request_args)

        if request_args != {}:
            sct.delete(request_args['student_name'], request_args['cca_name'])
            return render_template('delete_details.html',
                                   page_type='delete_student_cca_success',
                                   name=request_args['student_name'],
                                   title='Delete Student CCA')

        return render_template('delete_details.html',
                               page_type='delete_student_cca_empty',
                               form_meta={
                                   'action': '/delete_student_cca',
                                   'method': 'post'
                               },
                               form_data={'name': ''},
                               title="Delete Student CCA")

    elif request.method == 'POST':
        name = request.form['name']
        # go = False
        # if go:
        temp = sct.find_by_name(name)
        if temp is None:
            return render_template(
                'delete_details.html',
                page_type='delete_student_cca_empty',
                form_meta={
                    'action': '/delete_student_cca',
                    'method': 'post'
                },
                form_data={'name': ''},
                error='This student does not exists! Try again.',
                title='Delete Student CCA')

        else:
            cca_list = []
            for rec in temp:
                cca_list.append(rec['cca name'])

            return render_template('delete_details.html',
                                   page_type='delete_student_cca_choose',
                                   form_meta={
                                       'action': '/delete_student_cca',
                                       'method': 'get'
                                   },
                                   cca_list=cca_list,
                                   name=name,
                                   title='Delete Student CCA')


@app.route('/delete_student_activity', methods=['GET', 'POST'])
def delete_student_activity():
    if request.method == 'GET':
        # print(dict(request.args))
        request_args = dict(request.args)
        print(request_args)

        if request_args != {}:
            sat.delete(request_args['student_name'],
                       request_args['activity_name'])
            return render_template('delete_details.html',
                                   page_type='delete_activity_success',
                                   name=request_args['student_name'],
                                   title='Delete Student Activity - Success')

        return render_template('delete_details.html',
                               page_type='delete_student_activity_empty',
                               form_meta={
                                   'action': '/delete_student_activity',
                                   'method': 'post'
                               },
                               form_data={'name': ''},
                               title='Delete Student Activity')

    elif request.method == 'POST':
        name = request.form['name']
        # go = False
        # if go:
        temp = sat.find_by_name(name)
        if temp is None:
            return render_template(
                'delete_details.html',
                page_type='delete_student_activity_empty',
                form_meta={
                    'action': '/delete_student_activity',
                    'method': 'post'
                },
                form_data={'name': ''},
                error='This student does not exists! Try again.',
                title='Delete Student Activity')

        else:
            activity_list = []
            for rec in temp:
                activity_list.append(rec['activity name'])

            return render_template('delete_details.html',
                                   page_type='delete_student_activity_choose',
                                   form_meta={
                                       'action': '/delete_student_activity',
                                       'method': 'get'
                                   },
                                   activity_list=activity_list,
                                   name=name,
                                   title='Delete Student Activity')


@app.route('/delete_cca', methods=['GET', 'POST'])
def delete_cca():
    if request.method == 'GET':
        return render_template('delete_details.html',
                               page_type='delete_cca_empty',
                               form_meta={
                                   'action': '/delete_cca',
                                   'method': 'post'
                               },
                               form_data={'cca_name': ''},
                               title='Delete CCA')
    elif request.method == 'POST':
        # print(request.form)
        name = request.form['cca_name']
        if cc.delete(name):
            return render_template('delete_details.html',
                                   page_type='delete_cca_success',
                                   name=name,
                                   title="Delete CCA")
        else:
            return render_template(
                'delete_details.html',
                page_type='delete_cca_empty',
                form_meta={
                    'action': '/delete_cca',
                    'method': 'post'
                },
                form_data={'name': ''},
                error='This CCA does not exists! Try again.',
                title="Delete CCA")


@app.route('/delete_activity', methods=['GET', 'POST'])
def delete_activity():
    if request.method == 'GET':
        return render_template('delete_details.html',
                               page_type='delete_activity_empty',
                               form_meta={
                                   'action': '/delete_activity',
                                   'method': 'post'
                               },
                               form_data={'activity_name': ''},
                               title="Delete Activity")
    elif request.method == 'POST':
        # print(request.form)
        name = request.form['activity_name']
        if ac.delete(name):
            return render_template('delete_details.html',
                                   page_type='delete_activity_success',
                                   name=name,
                                   title='Delete Activity')
        else:
            return render_template(
                'delete_details.html',
                page_type='delete_activity_empty',
                form_meta={
                    'action': '/delete_activity',
                    'method': 'post'
                },
                form_data={'name': ''},
                error='This activity does not exists! Try again.',
                title='Delete Activity')
