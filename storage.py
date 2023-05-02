from typing import Union
import sqlite3

#for normal tables: find & delete shld be the same


class NameNotFoundError(Exception):
    """Student/CCA/Activity name is not found."""
    pass


class RecordAlreadyExists(Exception):
    """
    Student/CCA/Activity record already exists.
    """
    pass


    # class Collection: parent class
#     """
#     parent class for student, cca, and activity

#     attributes:
#     -dbname

#     methods:
#     +insert() #child
#     +find()
#     +findall()
#     +update() #child
#     # +delete() optional for now
#     """
#     def __init__(self, dbname, tblname):
#         self._dbname = dbname
#         self._tblname = tblname

#     def __repr__(self):
#         return f"Collection(DB: {self._dbname}, TBL: {self._tblname})"

#     def insert(self):
#         """
#         to be implemented in child classes
#         """
#         print("not implemented in child class yet")

#     def find(self, name):
#         """

#         """

#     # def findall(self):
#     #     """
#     #     return all records
#     #     """

#     # def delete(self, name: str, ):
#     #     """
#     #     deletes the record with
#     #     """

# def update(self, prev_record, new_record):
#         """
#         takes in prev_record (the record to be updated), and new_record (info to update record with)
#         """
#         pass

#     def _execute_dql(self, query):
#         """retrieve records etc"""
#         with sqlite3.connect(self._dbname) as conn:
#             c = conn.cursor()

#             c.execute(query)
#             result = c.fetchall()

#         #conn.close()

#         return result

#     def _execute_dml(self, query, params):
#         """insert, delete, update etc"""
#         with sqlite3.connect(self._dbname) as conn:
#             c = conn.cursor()

#             c.execute(query, params)
#             result = c.fetchall()

#             conn.commit()
#         #conn.close()

#         return result


class StudentCollection:
    """
    Attributes:
    
    Methods:
    + find
    + insert
    + update
    + delete
    """

    def __init__(self, dbname: str, tblname: str):
        self._dbname = dbname
        self._tblname = tblname

    def find(self, name: str) -> 'Union[None, list[dict]]':
        """
        Takes in student name
        Finds the record in student table

        returns None if record not found
        """

        find = f'''
                SELECT *
                FROM "{self._tblname}"
                WHERE "student"."name" = ?;
                '''

        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute(find, (name, ))

            result = c.fetchone()

        if result:
            return dict(result)

        else:
            return None

    # def find_all(self) ->:
    #     """
    #     Returns all record of students
    #     """
    #     pass

    def insert(self, record: dict) -> None:
        """
        Takes in dictionary containing student's name, age, class, year_enrolled, grad_year

        record = {"student_name": str,
                   "student_age": str,
                   "student_class": int
                   "student_year_enrolled": str,
                   "student_grad_year": str}

        Inserts student data into table

        Returns None

        Raise error when student (name) already exists
        
        (done) Next step(0): Raise error when something unexpected occurs (perhaps wrong data type for age)
        Next step(1): Looks like data validation is necessary.
        """

        if self.find(record["student_name"]
                     ) is not None:  # Student name already exists
            raise RecordAlreadyExists

        insert = '''
                INSERT INTO "student" (
                "name",
                "age",
                "class",
                "year_enrolled",
                "grad_year"
                ) VALUES (
                :student_name, :student_age, :student_class, :student_year_enrolled, :student_grad_year)
                '''

        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()

            c.execute(insert, record)

            conn.commit()

    def update(self, old_name, new_record
               ):  #decide how we are gonna find the exising record first
        """
        Takes in updated student name, age, year_enrolled, grad_year, student_subjects
        Finds existing record
        Update with new student details

        Returns None

        Next step(0): Raise error when new student details have wrong data type. Or when user is trying to edit a student who does not exist.
        """
        pass

    def delete(self, name):
        """
        Takes in student name
        Deletes student record from "students" table.

        Returns None

        Next step(0): Raise error when something unexpected occurs (perhaps name not found)
        Next step (1): Need to delete this student's record from the activities and cca records as well. This can probably call on the CCA/Activity Collection
        """
        if self.find(name) is None:  #record doesn't exist
            raise NameNotFoundError

        delete = '''
                DELETE FROM "student"
                WHERE "student"."name" = ?
                '''

        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()

            c.execute(delete, (name, ))

            conn.commit()

        print(f'{name} deleted')
        return None

    # def add_student_membership(self):
    #     """
    #     Takes in student name, CCA name, student's role in CCA
    #     Adds student membership in given CCA, with given role.

    #     Returns None

    #     Raise error when student or cca does not exist.

    #     Next step(0):

    #     FOR DORA: this process will occur in the junction table. (Also possible for it to be implemented in the cca class. What if we just have a new table)
    #     """
    #     pass

    # def update_student_membership(self):
    #     pass


class CCACollection:
    """
    Attributes:
    
    Methods:
    + find 
    + insert 
    + update (optional)
    + delete 
    """

    def __init__(self, dbname: str, tblname: str):
        self._dbname = dbname
        self._tblname = tblname

    def find(self, name):
        """
        Takes in cca name
        Finds the record in cca table

        returns None if record not found
        """

        find = f'''
                SELECT *
                FROM "{self._tblname}"
                WHERE "cca"."name" = ?;
                '''

        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute(find, (name, ))

            result = c.fetchone()

        if result:
            return dict(result)

        else:
            return None

    def insert(self, record: dict) -> None:
        """
        Takes in dictionary containing cca's name and type,

        record = {"cca_name": str,
                  "cca_type": str}

        Inserts cca data into table

        Returns None

        Raise error when cca (name) already exists
        
        Next step(0): Raise error when something unexpected occurs (perhaps wrong data type for age)
        Next step(1): Looks like data validation is necessary.
        """

        if self.find(
                record["cca_name"]) is not None:  # Student name already exists
            raise RecordAlreadyExists

        insert = '''
                INSERT INTO "cca" (
                "name",
                "type"
                ) VALUES (
                :cca_name, :cca_type)
                '''

        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()

            c.execute(insert, record)

            conn.commit()

    def update(self, new_record):  #same as student collection
        """
        Takes in updated cca_name, cca_type
        Finds existing record
        Update with new cca details

        Returns None

        Next step(0): Raise error when new cca details have wrong data type. Or when user is trying to edit a cca who does not exist.
        """
        pass

    def delete(self, name):
        """
        Takes in CCA name
        Delete CCA from "cca" table (maybe when cca close down? Or user type in wrong cca name)

        Returns None

        Raise Error when no CCA does not exist

        Next step(0): Remove students and activities from CCAs, when a CCA is deleted.
        """
        if self.find(name) is None:  #record doesn't exist
            raise NameNotFoundError

        delete = '''
                DELETE FROM "cca"
                WHERE "cca"."name" = ?
                '''

        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()

            c.execute(delete, (name, ))

            conn.commit()

        print(f'{name} deleted')
        return None


class ActivityCollection:
    """
    Attributes:
    
    Methods:
    + find 
    + insert 
    + update (optional)
    + delete 
    """

    def __init__(self, dbname: str, tblname: str):
        self._dbname = dbname
        self._tblname = tblname

    def find(self, name):
        """
        Takes in activity name
        Finds the record in activity table

        returns None if record not found
        """

        find = f'''
                SELECT *
                FROM "{self._tblname}"
                WHERE "activity"."name" = ?;
                '''

        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute(find, (name, ))

            result = c.fetchall()

        if result:
            for i in range(len(result)):
                result[i] = dict(result[i])

            return result

        else:
            return None

    def insert(self, record: dict) -> None:
        """
        Takes in dictionary containing activity's name, start date, end date, description, and category

        record = {"activity_name": text,
                  "activity_sd": int,    #IMPT: are we using delimiters? eg. 2023-01-30
                  "activity_ed": int / None,    #what are the keys tht im gna get from xy
                  "activity_desc": str,
                  "activity_cat": str}

        Inserts activity data into table

        Returns None

        Raise error when activity (name) already exists
        
        Next step(0): Raise error when something unexpected occurs (perhaps wrong data type)
        Next step(1): Looks like data validation is necessary.
        """

        if self.find(record["activity_name"]
                     ) is not None:  # activity name already exists
            raise RecordAlreadyExists

        insert = '''
                INSERT INTO "activity" (
                "name",
                "start_date",
                "end_date",
                "description",
                "category"
                ) VALUES (
                :activity_name, :activity_sd), :activity_ed, :activity_desc, :activity_cat
                '''

        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()

            c.execute(insert, record)

            conn.commit()

    def update(self, new_record):
        """
        Takes in updated cca_name, cca_type
        Finds existing record
        Update with new cca details

        Returns None

        Next step(0): Raise error when new cca details have wrong data type. Or when user is trying to edit a cca who does not exist.
        """
        pass

    def delete(self, name):
        """
        Takes in CCA name
        Delete CCA from "cca" table (maybe when cca close down? Or user type in wrong cca name)

        Returns None

        Raise Error when no CCA does not exist

        Next step(0): Remove students and activities from CCAs, when a CCA is deleted.
        """
        if self.find(name) is None:  #record doesn't exist
            raise NameNotFoundError

        delete = '''
                DELETE FROM "activity"
                WHERE "activity"."name" = ?
                '''

        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()

            c.execute(delete, (name, ))

            conn.commit()

        return None


#junction tables
class StudentCCATable:
    """
    methods:
    +find(student_name)
    +insert(record)
    +update(record)
    """

    
    def __init__(self, dbname):
        self._dbname = dbname
        self._sc = StudentCollection(self._dbname, "student")
        self._ccac = CCACollection(self._dbname, "cca")

        
    def __repr__(self):
        return f"StudentCCATable(DB: {self._dbname})"

    
    def find(self, student_name):
        """
        Takes in student name
        
        joins student & cca tables
        
        returns None if record not found
        """
        
        join_and_find = '''
                        SELECT 
                        "student"."name" AS "student name",
                        "student"."class" AS "student class",
                        "cca"."name" AS "cca name",
                        "student_cca"."role" as "role"
                        FROM "student"
                        INNER JOIN "student_cca"
                        ON "student"."id" = "student_cca"."student_id"
                        INNER JOIN "cca"
                        ON "student_cca"."cca_id" = "cca"."id"
                        
                        WHERE "student"."name" = ?
                        '''

        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute(join_and_find, (student_name, ))

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
                                    "cca_id": str
                                    "student_role": str
                                    }
        """        
        student_id = self._sc.find(record['student_name'])["id"]
        cca_id = self._ccac.find(record['student_cca'])["id"]
        
        #If student or CCA doesnt exist raise NameNotFoundError
        if (student_id is None) or (cca_id is None):
            raise NameNotFoundError
            
        existing_rec = self.find(record['student_name'])
        
        for rec in existing_rec:
            if (rec['student name'] == record['student_name']) and (rec['cca name'] == record['student_cca']):
                raise RecordAlreadyExists

        record['student_id'] = student_id
        record['cca_id'] = cca_id

        insert = '''
                INSERT INTO "student_cca" (
                "student_id",
                "cca_id",
                "role"
                ) VALUES (
                :student_id, :cca_id, :student_role
                )
                '''

        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()

            c.execute(insert, record)

            conn.commit()

class StudentSubjectTable:
    """
    methods:
    +find(student_name)
    +insert(record)
    """

    def __init__(self, dbname):
        self._dbname = dbname

    def __repr__(self):
        return f"StudentSubjectTable(DB: {self._dbname})"

    def find(self, student_name):
        """
        Takes in student name
        
        joins student & subject tables
        
        returns None if record not found
        """
        join_and_find = '''
                        SELECT
                        "student"."name" AS "student name",
                        "student"."class" AS "student class"
                        "subject"."name" AS "subject name"
                        FROM "student"

                        INNER JOIN "student_subject"
                        ON "student"."id" = "student_subject"."student_id"
                        INNER JOIN "subject"
                        ON "student_subject"."subject_id" = "subject"."id"
                        
                        WHERE "student"."name" = ?
                        '''

        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute(join_and_find, (student_name, ))

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

        record = {}
        """
        pass
        
class StudentActivityTable:
    """
    methods:
    +find(student_name)
    +insert(record)
    """

    def __init__(self, dbname):
        self._dbname = dbname

    def __repr__(self):
        return f"StudentActivityTable(DB: {self._dbname})"

    def find(self, student_name):
        """
        Takes in student name
        
        joins student & activity tables
        
        returns None if record not found
        """
        join_and_find = '''
                        SELECT
                        "student"."name" AS "student name",
                        "student"."class" AS "student class"
                        "activity"."name" AS "activity name",
                        "student_activity"."role" AS "role",
                        "student_activity"."award" AS "award",
                        "student_activity"."hours" AS "hours"
                        FROM "student"
                        INNER JOIN "student_activity"
                        ON "student"."id" = "student_activity"."student_id"
                        INNER JOIN "activity"
                        ON "student_activity"."activity_id" = "activity"."id"
                        
                        WHERE "student"."name" = ?
                        '''

        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute(join_and_find, (student_name, ))

            result = c.fetchall()

            if result:
                for i in range(len(result)):
                    result[i] = dict(result[i])

                return result

            else:
                return None
