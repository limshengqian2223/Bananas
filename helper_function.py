from typing import Union

def empty_fields(registration_record: dict) -> [str]:
    """
    Takes in registration record, validates that the registration record has no empty fields.
    
    takes in a dict, returns a list of strings
    """
    empty_fields = []
    for field_name, value in registration_record.items():
        if value.strip() == '':
            empty_fields.append(field_name)
            
    return empty_fields

def type_converter(registration_record: dict) -> [str]:
    """
    Takes in registration/edit record, validates that the values in the record are of the correct data type.
    student_age : int
    student_year_enrolled : int
    student_grad_year : int

    returns a list of strings of fields which have wrong data type
    """
    wrong_type_fields = []
    for field_name, value in registration_record.items():
        if "age" in field_name or "year" in field_name or "hours" in field_name:
            if not value.isdigit():
                wrong_type_fields.append(field_name)
            else:
                registration_record[field_name] = int(value)
    return wrong_type_fields
    