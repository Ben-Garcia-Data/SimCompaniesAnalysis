import os
import plotly.graph_objects as go
from TargetCalculations import calculate_targets

file_name = 'db_numbers_that_can_be_sold'
with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', str(file_name)) + '.txt', "r") as file1:
    db_numbers_that_can_be_sold = eval(file1.read())
    file1.close()

file_name = 'numbers_dict'
with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files',
                       str(file_name)) + '.txt', "r") as file1:
    number_name_dict = file1.read()
    file1.close()
    number_name_dict = eval(number_name_dict)

db_number = 53
x = 6

file_name = str(db_number) + '- Q' + str(x) + '.txt'
print(file_name)
try:
    with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales', file_name),
              "r") as file1:
        data = file1.readlines()
        file1.close()
except:
    print('File not found')

print(data)
print(data[0])
print(type(data[0]))

if data[0] == '6\n':
    print('hi')


