def empty_fields(registration_record):
    """
    Takes in registration record, validates that the registration record has no empty fields.
    
    takes in a dict, returns a list of strings
    """
    empty_fields = []
    for field_name, value in registration_record.items():
        if value.strip() == '':
            empty_fields.append(field_name)
            
    return empty_fields