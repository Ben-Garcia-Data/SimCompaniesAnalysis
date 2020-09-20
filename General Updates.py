import requests
import os
import time

game_updated = True
def game_has_been_updated():
    # Makes a list of all db numbers and a dict of all numbers:names
    resources_url = "https://www.simcompanies.com/api/v3/en/encyclopedia/resources/"

    response = requests.get(resources_url).json()
    db_numbers = []
    numbers_dict = {}
    print(response)
    for i in response:
        db_numbers.append(i['db_letter'])
        numbers_dict[i['db_letter']] = i['name']
    print("I found the follow items:")
    print(str(numbers_dict))

    with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', "numbers_dict.txt"),
              "w") as file1:
        file1.write(str(numbers_dict))
        file1.close()

    market_url = "https://www.simcompanies.com/api/v2/market/"
    db_numbers_that_can_be_sold = []
    db_numbers_that_cannot_be_sold = []

    for x in db_numbers:
        url = market_url + str(x)
        try:
            market_response = requests.get(url).json()
        except:
            print("Error")
        print(url)
        time.sleep(1)

        if len(market_response) == 0:
            db_numbers_that_cannot_be_sold.append(x)

        else:
            db_numbers_that_can_be_sold.append(x)

    with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', "db_numbers_that_cannot_be_sold.txt"),
              "w") as file1:
        file1.write(str(db_numbers_that_cannot_be_sold))
        file1.close()

    with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', "db_numbers_that_can_be_sold.txt"),
              "w") as file1:
        file1.write(str(db_numbers_that_can_be_sold))
        file1.close()


if game_updated == True:
    game_has_been_updated()