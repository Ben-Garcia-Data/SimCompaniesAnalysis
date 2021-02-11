import os
import datetime

now = datetime.datetime.utcnow()
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

for db_number in db_numbers_that_can_be_sold:
    # print(db_number)
    for x in range(9):
        file_name = str(db_number['id']) + '- Q' + str(x) + '.txt'
        #print(file_name)
        try:
            with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales', file_name),
                      "r") as file1:
                data = file1.readlines()
                file1.close()
        except FileNotFoundError:
             continue

        try:
            if isinstance(data[0], str):
                data[0] = eval(data[0])
                #print(type(data))
                #print(type(data[0]))
        except SyntaxError:
            print('Data' + str(data))
            new_output = []
            #print('Edited: ' + str(file_name))


            for line in range(len(data)):
                text = str(data[line])
                new_output.append(text.strip('\n'))

                ##os.remove(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales', file_name))
            print('New output: ' + str(new_output))
            #print("")
            continue

    for x in range(9):
        file_name = str(db_number['id']) + '- Q' + str(x) + ' NEW.txt'
        try:
            os.remove(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales', file_name))
            print('Removed: ' + str(file_name))
        except FileNotFoundError:
            continue