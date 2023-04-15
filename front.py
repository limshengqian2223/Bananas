from flask import Flask, render_template, request
#balls
#import from storage next time

app = Flask(__name__)

@app.route('/')
def index():
    """
    Landing Page - Not much
    -Documentation for first time users
    """
    pass

@app.route('/new_student', methods=['POST'])
def new_student():
    """ 
    Require: None
    Pass to DB: name, age. year enroll, grad year, student_subject (seperate table) (Inserting by DB)
    """
    pass

@app.route('/new_student_cca', methods=['POST'])
def new_student_cca():
    """
    Require: None
    Pass to DB: student's cca (Inserting by DB)

    Use students name to add in their cca
    """
    pass

@app.route('/new_student_activity', methods=['POST'])
def new_student_activity():
    """
    Require: None
    Pass to DB: student's activity (Inserting by DB)

    Use students name to add in their activity
    """
    pass

@app.route('/new_cca', methods=['POST'])
def new_cca():
    """
    Require: None
    Pass to DB: name, type (Insert by DB)
    """
    pass

@app.route('/new_activity', methods=['POST'])
def new_activity():
    """
    Require: None
    Pass to DB: (Insert by DB)
    coordinated by who
    category:str{Achievement, Enrichment, Leadership, Service}
    Award:str
    Hours:int
    """
    pass

@app.route('/view_student_cca', methods=['GET', 'POST'])
def view_student_cca():
    """
    Require: student's cca (Finding by backend)

    user pass in: student name
    """
    pass

@app.route('/view_student_activity', methods=['GET','POST'])
def view_student_activity():
    """
    Require: student's activities (Find by backend)

    pass in : name
    """
    pass
    
@app.route('/edit_student', methods=['GET','POST'])
def edit_student():
    """
    Require: Student record (Find by backend)

    Pass to DB :edited student Record (Update by DB)
    """
    pass

@app.route('/edit_membership', methods=['GET','POST'])
def edit_membership():
    """
    Require: Student CCA record (Find by backend)
    
    pass in: edited student CCA record (Update by DB)
    """
    pass

@app.route('/edit_participation', methods=['GET','POST'])
def edit_participation():
    """
    pass in: edited student activity record (Find by DB)
    
    Require: Student activity record (Update by DB)
    """
    pass