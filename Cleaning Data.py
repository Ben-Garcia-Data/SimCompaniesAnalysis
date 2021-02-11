import os
import ast
import json
import datetime

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

def general_cleanup():
    for db_number in db_numbers_that_can_be_sold:
        cleaned_up_datapoints = 0
        bad_datapoints = 0
        good_data = []
        #print(db_number)
        id = db_number['id']
        print(number_name_dict[id])
        file_name = str(id) + '- Q' + str(0) + '.txt'
        #print(file_name)

        try:
            with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales', file_name),
                      "r") as file1:
                data = file1.readlines()
                file1.close()
                # print('DATA: ' + str(data))
                # print("")

        except FileNotFoundError:
            data = []
            print(str(file_name) + ' not found')


        for x in data:
            try:
                if isinstance(x, str):
                    x = eval(x)
            except:
                print('This is bad data:')
                print(x)
                bad_datapoints = bad_datapoints + 1
                continue


            if x['quality'] != 0:
                new_quality = x['quality']
                cleaned_up_datapoints = cleaned_up_datapoints + 1
                #print('New Q: ' + str(new_quality))

                file_name = str(id) + '- Q' + str(new_quality) + '.txt'
                # Open the file in append & read mode ('a+')
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales',
                                       str(file_name)), "a+") as file_object:

                    file_object.write('\n')
                    file_object.write(str(x))

                    file_object.close()
            else:
                good_data.append(x)


        file_name = os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales', str(id) + '- Q' + str(0) +'.txt')
        print(file_name)
        os.remove(file_name)

        #print('All good data: ' + str(good_data))
        for x in good_data:
            # print('loop = ' + str(loop))
            content = x.copy()
            #print('Writing to ' + str(file_name) + ", " + str(content))

            # Open the file in append & read mode ('a+')
            with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales',
                                   str(file_name)), "a+") as file_object:
                file_object.write(str(content))
                file_object.write('\n')

            file_object.close()

        print('Bad datapoints: ' + str(bad_datapoints))
        print('Cleaned Up datapoints: ' + str(cleaned_up_datapoints))
        print("")

def final_cleanup():
    print('Final Cleanup')
    for x in db_numbers_that_can_be_sold:
        db_number = x['id']
        for x in range(9):
            file_name = str(db_number) + '- Q' + str(x) + '.txt'
            #print(file_name)
            try:
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales', file_name),
                          "r") as file1:
                    data = file1.readlines()
                    file1.close()
            except FileNotFoundError:
                data = []
                continue

            if data[0] == "\n":
                print('Empty line here: ' + str(file_name))
                new_data = data[1:len(data)]
                print(new_data)
                target = os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales', file_name)
                os.remove(target)
                with open(target,"a+") as file1:
                    for line in new_data:
                        file1.write(str(line))
                        file1.write('\n')
                    file1.close()

            if data[0] in ['1\n', '2\n', '3\n', '4\n', '5\n', '6\n', '7\n', '8\n', '9\n']:
                print('Bad data here: ' + str(file_name))
                new_data = data[1:len(data)]
                print(new_data)
                target = os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales', file_name)
                os.remove(target)
                with open(target, "a+") as file1:
                    for line in new_data:
                        file1.write(str(line))
                        file1.write('\n')
                    file1.close()

#general_cleanup()
final_cleanup()