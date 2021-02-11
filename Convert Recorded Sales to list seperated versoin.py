import os
import time
import datetime

file_name = 'db_numbers_that_can_be_sold'
with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files',
                       str(file_name)) + '.txt', "r") as file1:
    db_numbers_that_can_be_sold = eval(file1.read())

file_name = 'numbers_dict'
with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files',
                        str(file_name)) + '.txt', "r") as file1:
    numbers_dict = eval(file1.read())
    file1.close()

for x in db_numbers_that_can_be_sold:
    db_number = x['id']
    #print(db_number)
    for quality in range(0,9):
        if quality == 10:
            print('skip bcus Q10')
        else:
            file_name = str(db_number) + '- Q' + str(quality)
            print(file_name)
            try:
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files/RecordedSales',
                                       str(file_name)) + '.txt', "r") as file1:
                    data = eval(file1.read())
            except FileNotFoundError:
                """print('File not found')"""
            #print(data)

            file_name = str(db_number) + '- Q' + str(quality)
            # print('Writing to ' + str(db_file_name) + ", " + str(content))
            if len(data) > 0:
                loop = 0
                total_time_1 = []
                total_time_2 = []
                total_time_3 = []
                total_time_4 = []
                total_time_5 = []

                #print('Data: ' + str(data))
                #print(type(data))
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales2',
                                       str(file_name)) + '.txt', "a+") as file_object:

                    for write_me in data:
                            time_0 = time.time()
                            time_1 = time.time()
                            # Move read cursor to the start of file.
                            file_object.seek(0)
                            time_2 = time.time()
                            # If file is not empty then append '\n'
                            data = file_object.read(100)
                            time_3 = time.time()
                            if len(data) > 0:
                                file_object.write("\n")
                            time_4 = time.time()
                            # Append text at the end of file
                            file_object.write(str(write_me))
                            time_5 = time.time()

                            #print('Timings report...')
                            #print('Open file: ' + str(time_1 - time_0))
                            #print('Seek: ' + str(time_2 - time_1))
                            #print('read: ' + str(time_3 - time_2))
                            #print('write new line: ' + str(time_4 - time_3))
                            #print('write data: ' + str(time_5 - time_4))
                            #total_time_1.append(time_1 - time_0)
                            #total_time_2.append(time_2 - time_1)
                            #total_time_3.append(time_3 - time_2)
                            #total_time_4.append(time_4 - time_3)
                            #total_time_5.append(time_5 - time_4)

                            loop = loop + 1

                def avg(listed):
                    return str(sum(listed)/len(listed))

                total_times = total_time_1 + total_time_2 + total_time_3 + total_time_4 + total_time_5
                #avg(total_times)

                print('Loops: ' + str(loop))
                #print('Timings report...')
                #print('Total time: ' + avg(total_times))
                #print('Open file: ' + avg(total_time_1))
                #print('Seek: ' + avg(total_time_2))
                #print('read: ' + avg(total_time_3))
                #print('write new line: ' + avg(total_time_4))
                #print('write data: ' + avg(total_time_5))
                print("")



