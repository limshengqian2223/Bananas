#place to test cod
import storage 

sc = storage.StudentCollection('capstone.db', 'student')

# record = {"student_name": 'sq',
#                    "student_age": 69,
#                    "year_enrolled": 2069,
#                    "grad_year": 2070}
# sc.insert(record)
result = sc.find('sq')
print(result)
for object in result:
    print(object)