from typing import Union 
import sqlite3

class Collection:
    """
    parent class for student, cca, and activity

    attributes:
    -dbname
    
    methods:
    +insert() #child
    +find() #same (?)
    # +findall()
    # +delete() #same (?)
    +update() #child
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

def _execute_dql(query, **kwargs):
    """retrieve records etc"""
    pass
        
def _execute_dml(query, params):
    """insert, delete, update etc"""
    pass

class StudentCollection(Collection):
    pass

class CCACollection(Collection):
    pass

class ActivityCollection(Collection):
    pass