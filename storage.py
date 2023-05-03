from typing import Union
import sqlite3

class NameNotFoundError(Exception):
    """Student/CCA/Activity name is not found."""
    pass


class RecordAlreadyExists(Exception):
    """
    Student/CCA/Activity record already exists.
    """
    pass

class Collection:
    """parent class for collections"""
    def __init__(self, dbname):
        self._dbname = dbname


    def _execute_dml(self, query, data):
        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()


            c.execute(query, data)

            conn.commit()

    def _execute_dql(self, query, data):
        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute(query, data)
            result = c.fetchall()

        if result:
            if len(result) == 1:
                result = dict(result[0])
                return result
            else:
                for i in range(len(result)):
                    result[i] = dict(result[i])
                return result
        else:
            return None


class ClassCollection(Collection):
    """
    methods:
    + find
    """
    def __init__(self, dbname: str, tblname: str):
        self._dbname = dbname
        self._tblname = tblname

    def __repr__(self):
        return f"ClassCollection(DB: {self._dbname}, TBL: {self._tblname})"

    def find_by_name(self, class_name):
        """
        takes in class name
        finds and returns class record

        returns None if record not found
        """
        find_by_name = f'''
                        SELECT *
                        FROM {self._tblname}
                        WHERE "name" = ?
                        '''
        result = self._execute_dql(find_by_name, (class_name,))
        return result

class StudentCollection(Collection):
    """
    Attributes:
    
    Methods:
    + find_by_name
    + find_by_class
    + insert
    + update
    + delete
    """

    def __init__(self, dbname: str, tblname: str):
        self._dbname = dbname
        self._tblname = tblname
        self._cc = ClassCollection(self._dbname, "class")

    def __repr__(self):
        return f"StudentCollection(DB: {self._dbname}, TBL: {self._tblname})"

    def find_by_name(self, name: str) -> 'Union[None, list[dict]]':
        """
        Takes in student name
        finds and returns the record in student table

        returns None if record not found
        """

        find_by_name = f'''
                SELECT
                "student"."id" AS "id",
                "student"."name" AS "name",
                "student"."age" AS "age",
                "class"."name" AS "class",
                "student"."year_enrolled" AS "year enrolled",
                "student"."grad_year" AS "graduating year"
                FROM "student"
                INNER JOIN "class"
                ON "student"."class_id" = "class"."id"
                
                WHERE "student"."name" = ?;
                '''
        
        result = self._execute_dql(find_by_name, (name,))
        return result
        
    def find_by_class(self, student_class):
        """
        Takes in student class
        finds and returns all students in the class

        returns None if no records found
        """
        class_rec = self._cc.find_by_name(student_class)
        if class_rec is None: #class doesnt exist
            return False
        
        class_id = class_rec['id']

        find_students = '''
                        SELECT 
                        "class"."name" AS "class",
                        "student"."name" AS "student name",
                        "student"."age" AS "student age"
                        FROM "student"
                        INNER JOIN "class"
                        ON "student"."class_id" = "class"."id"

                        WHERE "class"."id" = ?
                        '''
    
        result = self._execute_dql(find_students, (class_id,))
        return result

    def insert(self, record: dict) -> True:
        """
        Takes in dictionary containing student's name, age, class, year_enrolled, grad_year

        record = {"student_name": str,
                   "student_age": str,
                   "student_class": int,
                   "student_year_enrolled": int,
                   "student_grad_year": int}

        Inserts student data into table

        Returns True

        Raise error when student (name) already exists
        
        (done) Next step(0): Raise error when something unexpected occurs (perhaps wrong data type for age)
        Next step(1): Looks like data validation is necessary.
        """

        if self.find_by_name(record["student_name"]) is not None:  # Student name already exists
            return False

        class_rec = self._cc.find_by_name(record["student_class"])
        record['class_id'] = class_rec['id']

        insert = '''
                INSERT INTO "student" (
                "name",
                "age",
                "class_id",
                "year_enrolled",
                "grad_year"
                ) VALUES (
                :student_name, :student_age, :class_id, :student_year_enrolled, :student_grad_year)
                '''

        self._execute_dml(insert, record)

        return True

    def update(self, student_name, new_record) -> True:
        """
        Takes in student_name, and updated student name, age, year_enrolled, grad_year, student_subjects
        finds existing record
        return False if record doesnt exist
        
        Update with new student details

        new_record = {"student_name": str,
                   "student_age": str,
                   "student_class": int
                   "student_year_enrolled": str,
                   "student_grad_year": str}
        Returns True

        Next step(0): Raise error when new student details have wrong data type. Or when user is trying to edit a student who does not exist.
        """
        if self.find_by_name(student_name) is None:  #record doesnt exist
            return False

        class_rec = self._cc.find_by_name(new_record['student_class'])
        if class_rec is None:
            return False
        
        new_record['student_class_id'] = class_rec['id']

        update = '''
                UPDATE "student" SET 
                "name" = ?,
                "age" = ?,
                "class_id" = ?,
                "year_enrolled" = ?,
                "grad_year" = ?
                WHERE "name" = ?
                ''' 
        data = (new_record["student_name"],
                new_record["student_age"],
                new_record["student_class_id"],
                new_record["student_year_enrolled"],
                new_record["student_grad_year"],
                student_name)

        self._execute_dml(update, data)
        return True

    def delete(self, name) -> True:
        """
        Takes in student name
        Deletes student record from "students" table.

        Returns True

        Next step(0): Raise error when something unexpected occurs (perhaps name not found)
        Next step (1): Need to delete this student's record from the activities and cca records as well. This can probably call on the CCA/Activity Collection
        """
        if self.find_by_name(name) is None:  #record doesn't exist
            return False

        delete = '''
                DELETE FROM "student"
                WHERE "student"."name" = ?
                '''

        self._execute_dml(delete, (name,))
        return True

class CCACollection(Collection):
    """
    Attributes:
    
    Methods:
    + find_by_name 
    + insert 
    + update
    + delete 
    """

    def __init__(self, dbname: str, tblname: str):
        self._dbname = dbname
        self._tblname = tblname

    def __repr__(self):
        return f"CCACollection(DB: {self._dbname}, TBL: {self._tblname})"

    def find_by_name(self, name):
        """
        Takes in cca name
        finds and returns the record in cca table

        returns None if record not found
        """

        find_by_name = f'''
                SELECT *
                FROM "{self._tblname}"
                WHERE "cca"."name" = ?;
                '''
        
        result = self._execute_dql(find_by_name, (name,))
        return result

    def insert(self, record: dict) -> True:
        """
        Takes in dictionary containing cca's name and type,

        record = {"cca_name": str,
                  "cca_type": str}

        Inserts cca data into table

        Returns True

        Raise error when cca (name) already exists
        
        Next step(0): Raise error when something unexpected occurs (perhaps wrong data type for age)
        Next step(1): Looks like data validation is necessary.
        """

        if self.find_by_name(
                record["cca_name"]) is not None:  # Student name already exists
            return False

        insert = '''
                INSERT INTO "cca" (
                "name",
                "type"
                ) VALUES (
                :cca_name, :cca_type)
                '''

        self._execute_dml(insert, record)
        return True

    def update(self, cca_name, new_record):
        """
        Takes in student_name & updated cca name & type
        finds existing record
        return False if record doesnt exist
        
        Update with new cca details

        new_record = {"cca_name": str,
                      "cca_type": str}
        Returns True

        Next step(0): Raise error when new cca details have wrong data type. Or when user is trying to edit a cca who does not exist.
        """
        if self.find_by_name(cca_name) is None:  #record doesnt exist
            return False

        update = '''
                UPDATE "cca" SET 
                "name" = ?,
                "type" = ?
                WHERE "name" = ?
                '''

        data = (new_record["cca_name"],
                new_record["cca_type"],
                cca_name)
        
        self._execute_dml(update, data)
        return True

    def delete(self, name):
        """
        Takes in CCA name
        Delete CCA from "cca" table (maybe when cca close down? Or user type in wrong cca name)

        Returns True

        Raise Error when no CCA does not exist

        Next step(0): Remove students and activities from CCAs, when a CCA is deleted.
        """
        if self.find_by_name(name) is None:  #record doesn't exist
            return False

        delete = '''
                DELETE FROM "cca"
                WHERE "cca"."name" = ?
                '''
        
        self._execute_dml(delete, (name,))
        return True


class ActivityCollection(Collection):
    """
    Attributes:
    
    Methods:
    + find_by_name 
    + insert 
    + update
    + delete 
    """

    def __init__(self, dbname: str, tblname: str):
        self._dbname = dbname
        self._tblname = tblname
        self._ccac = CCACollection(self._dbname, "cca")

    def __repr__(self):
        return f"ActivityCollection(DB: {self._dbname}, TBL: {self._tblname})"

    def find_by_name(self, name):
        """
        Takes in activity name
        finds and returns the record in activity table

        returns None if record not found
        """

        find_by_name = f'''
                SELECT *
                FROM "{self._tblname}"
                WHERE "activity"."name" = ?;
                '''

        result = self._execute_dql(find_by_name, (name,))
        return result

    def insert(self, record: dict) -> True:
        """
        Takes in dictionary containing activity's name, start date, end date, description, and category

        record = {"activity_name": text,
                  "cca_name": text,-   #xy pass in the name but i insert the id
                  "activity_sd": int,   #using delimiters eg. 2023-01-30
                  "activity_ed": int / None,  
                  "activity_desc": str,
                  "activity_cat": str}

        Inserts activity data into table

        Returns None

        Raise error when activity (name) already exists
        
        Next step(0): Raise error when something unexpected occurs (perhaps wrong data type)
        Next step(1): Looks like data validation is necessary.
        """

        if self.find_by_name(record["activity_name"]) is not None:  # activity name already exists            
            return False

        cca_rec = self._ccac.find_by_name(record["cca_name"])

        if cca_rec is None:
            return False

        record["cca_id"] = cca_rec['id']

        insert = '''
                INSERT INTO "activity" (
                "name",
                "cca_id",
                "start_date",
                "end_date",
                "description",
                "category"
                ) VALUES (
                :activity_name, :cca_id, :activity_sd, :activity_ed, :activity_desc, :activity_cat)
                '''

        self._execute_dml(insert, record)
        return True

    def update(self, activity_name, new_record):
        """
        Takes in updated activity name, cca_name, activity sd, ed, desc, cat
        finds existing record
        return False if record doesnt exist
        
        Update with new activity details

        new_record = {"activity_name": str,
                      "cca_name": int,
                      "activity_sd": str,
                      "activity_ed": str,
                      "activity_desc": str,
                      "activity_cat": str}
        Returns None

        Next step(0): Raise error when new activity details have wrong data type. Or when user is trying to edit an activity that does not exist.
        """
        if self.find_by_name(activity_name) is None:  #record doesnt exist
            return False
        
        cca_rec = self._ccac.find_by_name(new_record["cca_name"])

        if cca_rec is None:
            return False

        new_record["cca_id"] = cca_rec["id"]

        update = '''
                UPDATE "activity" SET 
                "name" = ?,
                "cca_id" = ?,
                "start_date" = ?,
                "end_date" = ?,
                "description" = ?,
                "category" = ?
                WHERE "name" = ?
                '''
        data = (new_record["activity_name"],
                new_record["cca_id"],
                new_record["activity_sd"],
                new_record["activity_ed"],
                new_record["activity_desc"],
                new_record["activity_cat"],
                activity_name)
       
        self._execute_dml(update, data)
        return True

    def delete(self, name):
        """
        Takes in activity name
        Delete activity from "activity" table (maybe when cca close down? Or user type in wrong cca name)

        Returns None

        Raise Error when activity does not exist

        Next step(0): Remove students from activities, when an activity is deleted.
        """
        if self.find_by_name(name) is None:  #record doesn't exist
            return False

        delete = '''
                DELETE FROM "activity"
                WHERE "activity"."name" = ?
                '''
        
        self._execute_dml(delete, (name,))
        return True

#junction tables
class StudentCCATable(Collection):
    """
    methods:
    +find_by_name(student_name)
    +insert(record)
    +update(student_name, cca_name, new_record)
    +delete(student_name, cca_name)
    """

    def __init__(self, dbname):
        self._dbname = dbname
        self._sc = StudentCollection(self._dbname, "student")
        self._ccac = CCACollection(self._dbname, "cca")

    def __repr__(self):
        return f"StudentCCATable(DB: {self._dbname})"

    def find_by_name(self, student_name):
        """
        Takes in student name
        
        joins student & cca tables

        returns a list of records of ccas the student is in
        
        returns None if record not found
        """

        find_by_name = '''
                        SELECT 
                        "student"."name" AS "student name",
                        "class"."name" AS "student class",

                        "cca"."name" AS "cca name",
                        "student_cca"."role" as "role"
                        FROM "student"
                        INNER JOIN "student_cca"
                        ON "student"."id" = "student_cca"."student_id"
                        INNER JOIN "cca"
                        ON "student_cca"."cca_id" = "cca"."id"
                        INNER JOIN "class"
                        ON "student"."class_id" = "class"."id"
                        
                        '''
                        # WHERE "student"."name" = ?

        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute(find_by_name)

            result = c.fetchall()

        if result:
            for i in range(len(result)):
                result[i] = dict(result[i])

            return result

        else:
            return None

    def find_by_cca(self, cca_name):
        """
        Takes in cca name
        finds and returns a list of records of the students in the cca

        returns None if record not found
        """
        find_by_cca = '''
                    SELECT 
                    "cca"."name" AS "cca",
                    "student"."name" AS "student name"
                    FROM "student_cca"
                    INNER JOIN "cca"
                    ON "student_cca"."cca_id" = "cca"."id"
                    INNER JOIN "student"
                    ON "student_cca"."student_id" = "student"."id"

                    WHERE "cca"."name" = ?
                    '''
        with sqlite3.connect('capstone.db') as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute(find_by_cca, (cca_name,))
            result = c.fetchall()

        if result:
            for i in range(len(result)):
                result[i] = dict(result[i])

            return result
        else:
            return None        

    def insert(self, record):
        """
        checks if student exists
        inserts new student cca record

        record = {"student_name": str,
                  "student_cca": str,
                  "student_role": str
                 }

        get the student & cca id & insert into junction table

        (to be inserted) record = {"student_id": str,
                                    "cca_id": str,
                                    "student_role": str
                                    }
        """
        student_rec = self._sc.find_by_name(record['student_name'])
        cca_rec = self._ccac.find_by_name(record['student_cca'])

        if (student_rec is None) or (cca_rec is None): #student or CCA doesnt exist
            return False

        existing_rec = self.find_by_name(record['student_name'])

        # if existing_rec is not None:
            # for rec in existing_rec:
            #     # if (rec['student name'] == record['student_name']) and (rec['cca name'] == record['student_cca']):
            #         # return False
            #     print(rec)

        print(existing_rec)

        record['student_id'] = student_rec['id']
        record['cca_id'] = cca_rec['id']

        insert = '''
                INSERT INTO "student_cca" (
                "student_id",
                "cca_id",
                "role"
                ) VALUES (
                :student_id, :cca_id, :student_role
                )
                '''

        # with sqlite3.connect(self._dbname) as conn:
        #     c = conn.cursor()

        #     c.execute(insert, record)

        #     conn.commit()

        # return True
    
    def update(self, student_name, cca_name, new_record):
        """
        takes in student_name, cca_name,
        and updated cca_name, rols
        **note: student name cannot be updated
        
        find_by_names existing record
        return False if record doesnt exist

        new_record = {"student_cca": str,
                      "student_role": str
                     }
        returns True
        """
        existing_rec = self.find_by_name(student_name) #type(existing_rec) = list

        if existing_rec is None: #student doesnt exist in student_cca table
            # print('record doesnt exist')
            return False
        
        #find_by_nameing the record to update
        rec_to_update = {}
        for rec in existing_rec:
            if rec["cca name"] == cca_name:
                rec_to_update = rec

        if rec_to_update == {}: #student record with particular cca doesnt exist
            # print('no record to update')
            return False
        
        #checking if new_record already exists in db
        for rec in existing_rec:
            if (rec['student name'] == student_name) and (rec['cca name'] == new_record['student_cca']):
                # print('new record alr exists')
                return False

        student_rec = self._sc.find_by_name(student_name)
        old_cca_rec = self._ccac.find_by_name(cca_name)
        new_cca_rec = self._ccac.find_by_name(new_record['student_cca']) #checking if new cca exists
        
        # print(student_rec)
        # print(old_cca_rec)
        # print(new_cca_rec)

        if (student_rec is None) or (old_cca_rec is None) or (new_cca_rec is None):
            return False
        
        student_id = student_rec["id"]
        new_cca_id = new_cca_rec["id"]
        old_cca_id = old_cca_rec["id"]
        
        update = '''
                UPDATE "student_cca" SET
                "cca_id" = ?,
                "role" = ?
                WHERE "student_id" = ? and "cca_id" = ?
                '''

        with sqlite3.connect('capstone.db') as conn:
            c = conn.cursor()

            c.execute(update, (new_cca_id, new_record['student_role'], student_id, old_cca_id))

            conn.commit()

        return True

    def delete(self, student_name, cca_name):
        """
        Takes in student name
        Delete record from student_cca table

        Returns True

        returns False when record doesnt exist
        """
        if self.find_by_name(student_name) is None:  #record doesnt exist
            return False

        student_rec = self._sc.find_by_name(student_name)
        cca_rec = self._ccac.find_by_name(cca_name)

        if (student_rec is None) or (cca_rec is None): #student/cca doesnt exist
            return False

        student_id = student_rec['id']
        cca_id = cca_rec['id']

        delete = '''
                DELETE FROM "student_cca"
                WHERE "student_id" = ? and "cca_id" = ?
                '''

        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()

            c.execute(delete, (student_id, cca_id))

            conn.commit()

        return True

# class StudentSubjectTable:
#     """
#     methods:
#     +find_by_name(student_name)
#     +insert(record)
#     +
#     """

#     def __init__(self, dbname):
#         self._dbname = dbname

#     def __repr__(self):
#         return f"StudentSubjectTable(DB: {self._dbname})"

#     def find_by_name(self, student_name):
#         """
#         Takes in student name
        
#         joins student & subject tables
        
#         returns None if record not found
#         """
#         join_and_find_by_name = '''
#                         SELECT
#                         "student"."name" AS "student name",
#                         "student"."class" AS "student class"
#                         "subject"."name" AS "subject name"
#                         FROM "student"

#                         INNER JOIN "student_subject"
#                         ON "student"."id" = "student_subject"."student_id"
#                         INNER JOIN "subject"
#                         ON "student_subject"."subject_id" = "subject"."id"
                        
#                         WHERE "student"."name" = ?
#                         '''

#         with sqlite3.connect(self._dbname) as conn:
#             conn.row_factory = sqlite3.Row
#             c = conn.cursor()

#             c.execute(join_and_find_by_name, (student_name, ))

#             result = c.fetchall()

#             if result:
#                 for i in range(len(result)):
#                     result[i] = dict(result[i])

#                 return result

#             else:
#                 return None

#     def insert(self, record):
#         """
#         checks if student exists
#         inserts new student cca record

#         record = {}
#         """
#         pass

class StudentActivityTable(Collection):
    """
    methods:
    +find_by_name(student_name)
    +insert(record)
    +update(record)
    +delete(student_name)
    """

    def __init__(self, dbname):
        self._dbname = dbname
        self._sc = StudentCollection('capstone.db', 'student')
        self._ac = ActivityCollection('capstone.db', 'activity')

    def __repr__(self):
        return f"StudentActivityTable(DB: {self._dbname})"

    def find_by_name(self, student_name):
        """
        Takes in student name
        
        joins student & activity tables
        
        returns None if record not found
        """
        join_and_find_by_name = '''
                        SELECT
                        "student"."name" AS "student name",
                        "class"."name" AS "student class",

                        "activity"."name" AS "activity name",
                        "student_activity"."role" AS "role",
                        "student_activity"."award" AS "award",
                        "student_activity"."hours" AS "hours"
                        FROM "student"
                        INNER JOIN "student_activity"
                        ON "student"."id" = "student_activity"."student_id"
                        INNER JOIN "activity"
                        ON "student_activity"."activity_id" = "activity"."id"
                        INNER JOIN "class"
                        ON "student"."class_id" = "class"."id"
                        
                        WHERE "student"."name" = ?
                        '''

        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute(join_and_find_by_name, (student_name, ))

            result = c.fetchall()

            if result:
                for i in range(len(result)):
                    result[i] = dict(result[i])

                return result

            else:
                return None

    def insert(self, record):
        """
        checks if student & activity exists
        
        record = {'student_name': str,
                  'student_activity': str,
                  'student_role': str/None (default = participant),
                  'student_award': str/None,
                  'student_hours': int}

        inserts new activity record

        (to be inserted) record = {'student_id': int,
                                   'activity_id': int,
                                   'student_role': str/None (default = participant),
                                   'student_award': str/None,
                                   'student_hours': int}
        """
        student_rec = self._sc.find_by_name(record["student_name"])
        activity_rec = self._ac.find_by_name(record["student_activity"])

        if (student_rec is None) or (activity_rec is None):
            return False

        existing_rec = self.find_by_name(record["student_name"])

        if existing_rec is not None:
            for rec in existing_rec:
                if (rec["student name"] == record["student_name"]) and (
                        rec["activity name"] == record["student_activity"]) and (
                            rec["role"] == record["student_role"]):
                    return False  #record alr exists

        record["student_id"] = student_rec["id"]
        record["activity_id"] = activity_rec["id"]

        insert = '''
                INSERT INTO "student_activity" (
                "student_id",
                "activity_id",
                "role",
                "award",
                "hours"
                ) VALUES (
                :student_id, :activity_id, :student_role, :student_award, :student_hours
                )
                '''

        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()

            c.execute(insert, record)

            conn.commit()

        return True

    def update(self, student_name, activity_name, new_record):
        """
        takes in student_name, activity_name,
        and updated activity name, role, award, hours
        **note: student name cannot be updated
        
        find_by_names existing record
        return False if record doesnt exist

        new_record = {'student_activity': str,
                    'student_role': str/None (default = participant),
                    'student_award': str/None,
                    'student_hours': int}
        returns True
        """
        existing_rec = self.find_by_name(student_name) #type(existing_rec) = list
        
        if existing_rec is None: #student doesnt exist in student_cca table
            return False
        
        #find_by_nameing the record to update
        rec_to_update = {}
        for rec in existing_rec:
            if rec["activity name"] == activity_name:
                rec_to_update = rec

        if rec_to_update == {}: #student record with particular cca doesnt exist
            return False
        
        student_rec = self._sc.find_by_name(student_name)
        old_activity_rec = self._ac.find_by_name(activity_name)
        new_activity_rec = self._ac.find_by_name(new_record['student_activity']) #checking if new activity exists

        if (student_rec is None) or (old_activity_rec is None) or (new_activity_rec is None):
            return False

        student_id = student_rec["id"]
        old_activity_id = old_activity_rec["id"]
        new_activity_id = new_activity_rec["id"]

        if new_record["student_role"] is None:
            new_record["student_role"] = 'participant'

        update = '''
                UPDATE "student_activity" SET
                "activity_id" = ?,
                "role" = ?,
                "award" = ?,
                "hours" = ?
                WHERE "student_id" = ? and "activity_id" = ?
                '''

        with sqlite3.connect('capstone.db') as conn:
            c = conn.cursor()

            c.execute(update, (new_activity_id, new_record["student_role"], new_record["student_award"], new_record["student_hours"], student_id, old_activity_id))

            conn.commit()

        return True

    def delete(self, student_name, activity_name):
        """
        Takes in student name and activity_name
        Delete record from student_activity table

        Returns True

        returns False when record doesnt exist
        """
        if self.find_by_name(student_name) is None:  #record doesnt exist
            return False

        student_rec = self._sc.find_by_name(student_name)
        activity_rec = self._ac.find_by_name(activity_name)

        if (student_rec is None) or (activity_rec is None): #student/activity doesnt exist
            return False
        
        student_id = student_rec['id']
        activity_id = activity_rec['id']

        print(student_id, activity_id)

        delete = '''
                DELETE FROM "student_activity"
                WHERE "student_id" = ? and "activity_id" = ?
                '''

        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()

            c.execute(delete, (student_id, activity_id ))

            conn.commit()

        return True