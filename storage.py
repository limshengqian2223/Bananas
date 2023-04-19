from typing import Union 
import sqlite3

class Collection:
    """
    parent class for student, cca, and activity

    attributes:
    -dbname
    
    methods:
    +insert() #child
    +find()
    +findall()
    +update() #child
    # +delete() optional for now
    """
    def __init__(self, dbname):
        self._dbname = dbname

    def __repr__(self):
        return f"Collection({self._dbname})"

    def insert(self):
        """
        to be implemented in child classes
        """
        pass

    def find(self, name):
        """
        takes in student name
        
        returns all records with matching name
        """
        pass

    # def findall(self):
    #     """
    #     return all records
    #     """

    # def delete(self, name: str, ):
    #     """
    #     deletes the record with
    #     """

    def update(self, prev_record, new_record):
        """
        takes in prev_record (the record to be updated), and new_record (info to update record with)
        """
        pass

    def _execute_dql(self, query):
        """retrieve records etc"""
        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor() 
    
            c.execute(query)
            result = c.fetchall()
    
        #conn.close()
        
        return result
            
    def _execute_dml(self, query, params):
        """insert, delete, update etc"""
        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()

            c.execute(query, params)
            result = c.fetchall()

            conn.commit()
        #conn.close()

        return result            
    
class StudentCollection(Collection):
    """
    
    """

class CCACollection(Collection):
    """
    
    """

class ActivityCollection(Collection):
    """
    
    """