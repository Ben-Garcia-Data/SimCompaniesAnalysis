import os
import time
import requests
import random
import collections, functools, operator
import math

file_name = 'db_numbers_that_can_be_sold'
with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', str(file_name)) + '.txt', "r") as file1:
    db_numbers_that_can_be_sold = eval(file1.read())
    file1.close()

file_name = 'db_numbers_that_cannot_be_sold'
with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', str(file_name)) + '.txt', "r") as file1:
    db_numbers_that_cannot_be_sold = eval(file1.read())
    file1.close()

file_name = 'numbers_dict'
with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', str(file_name)) + '.txt', "r") as file1:
    number_name_dict = file1.read()
    file1.close()
    number_name_dict = eval(number_name_dict)

all_db_numbers = db_numbers_that_cannot_be_sold
for x in db_numbers_that_can_be_sold:
    all_db_numbers.append(x['id'])


# This can be the main function I can call that uses updated exchange target prices to recalculate profit margins.

# Returns a list of dicts, 1 for each Q I've seen sold, with their 95th and 5th percentile price targets. These
# price targets are still a bit iffy, but will improve the more I get data thru main.py

def More_Step_Production(list_of_ingredients, target_quality, step):
    # This super simple for loop allows me to iterate through all the supplied db numbers. If it is just one (must
    # still be in a list) then we get just the 1, but if we have more than 1 then we can keep looping for however
    # many we need.

    # We get slightly different inputs so we handle them slightly differently.
    output_list = []
    # print('List of ingredients: ' + str(list_of_ingredients))
    for db_number_data in list_of_ingredients:
        # print(db_number_data)
        # print(db_number_data)
        db_number = db_number_data['db_number']
        old_quantity = db_number_data['quantity']
        # print("I'm looking at " + str(db_number_data))

        # I removed this and everything dies so... don't remove this if statement.
        if db_number != 1:
            encyclopedia_url = 'https://www.simcompanies.com/api/v3/en/encyclopedia/resources'
            market_state = 0  # 0 = Recession, 1 = Normal, 2 = Boom
            url = encyclopedia_url + '/' + str(market_state) + '/' + str(db_number) + '/'

            # print(url)
            # Gets the encyclopedia Data
            def encyclopedia_fetch(url):

                try:
                    encyclopedia_response = requests.get(url).json()
                except TimeoutError:
                    print("TimeoutError, could not get API data")
                    time.sleep(5)
                    encyclopedia_response = encyclopedia_fetch(url)

                # Saves the file for future use.
                file_name = db_number
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\Encyclopedia',
                                       str(file_name)) + '.txt',
                          "w") as file1:
                    file1.write(str(encyclopedia_response))
                    file1.close()

                return encyclopedia_response

            # Looks for a saved encyclopedia entry, if it can't find one then it looks online
            try:
                file_name = db_number
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\Encyclopedia',
                                       str(file_name)) + '.txt',
                          "r") as file1:
                    response = eval(file1.read())
                    file1.close()
                    # print('Got the file from disk')
            except FileNotFoundError:
                print('File not found. Grabbing one from the internet.')
                response = encyclopedia_fetch(url)

            # print('Response: ' + str(response))

            product_name = response['name']
            needed_for = response['neededFor']

            # Make a list of dicts of every product that goes into making this.
            produced_from = response['producedFrom']
            produced_from_formatted = []
            for product in produced_from:
                # print(product)
                id = product['resource']['db_letter']
                quantity = product['amount']
                product_dict = {}
                product_dict['db_number'] = id
                product_dict['quantity'] = (quantity * old_quantity)
                if (target_quality - step - 1) <= 0:
                    quality = 0
                else:
                    quality = target_quality - step - 1

                product_dict['quality'] = quality
                product_dict['unique_ID'] = random.random()
                # print('product_dict: ' + str(product_dict))
                produced_from_formatted.append(product_dict)
                # print('produced from formatted: ' + str(produced_from_formatted))

        elif db_number == 1:
            produced_from_formatted = db_number_data
            # print('This is power')

        try:
            output_list.append(produced_from_formatted)
            # print('Output list: ' + str(output_list))
        except UnboundLocalError:
            # Now that there is an elif above, I don't think this ever occours but I'll leave it here just in case.
            # print('UnboundLocalError (I think this means it was power)')
            output_list.append(db_number_data)
            # print('After unbound: ' + str(db_number_data))

    # print(output_list)
    # Solves a whole load of ugly formatting shiz

    output = []
    for x in output_list:
        # print('X is: ' + str(x))

        if isinstance(x, list):
            output = output + x
        if isinstance(x, dict):
            output.append(x)

    # print('Output list: ' + str(output_list))
    # print('Output: '+str(output))
    # print("")
    return output

    # Now that I have a list which gives me all the required ingredients and their quantities, I need to find
    # out the sourcing price for those times.


def Any_Step_Production(db_number, target_quality, steps, loops):
    # This will input the 1 db number and output a list of dicts with the input product and the quantity needed for
    # only 1 step.

    # NO LONGER USED
    def One_Step_Production(db_numbers):
        # This super simple for loop allows me to iterate through all the supplied db numbers. If it is just one (must
        # still be in a list) then we get just the 1, but if we have more than 1 then we can keep looping for however
        # many we need.
        output_list = []
        produced_from_formatted = []
        for db_number in db_numbers:
            encyclopedia_url = 'https://www.simcompanies.com/api/v3/en/encyclopedia/resources'
            market_state = 0  # 0 = Recession, 1 = Normal, 2 = Boom
            url = encyclopedia_url + '/' + str(market_state) + '/' + str(db_number) + '/'

            # print(url)
            # Gets the encyclopedia Data
            def encyclopedia_fetch(url):

                try:
                    encyclopedia_response = requests.get(url).json()
                except TimeoutError:
                    print("TimeoutError, could not get API data")
                    time.sleep(5)
                    encyclopedia_response = encyclopedia_fetch(url)

                # Saves the file for future use.
                file_name = db_number
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\Encyclopedia',
                                       str(file_name)) + '.txt',
                          "w") as file1:
                    file1.write(str(encyclopedia_response))
                    file1.close()

                return encyclopedia_response

            # Looks for a saved encyclopedia entry, if it can't find one then it looks online
            try:
                file_name = db_number
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\Encyclopedia',
                                       str(file_name)) + '.txt',
                          "r") as file1:
                    response = eval(file1.read())
                    file1.close()
                    # print('Got the file from disk')
            except FileNotFoundError:
                print('File not found. Grabbing one from the internet.')
                response = encyclopedia_fetch(url)

            # print('Response: ' + str(response))

            product_name = response['name']
            needed_for = response['neededFor']

            # Make a list of dicts of every product that goes into making this.
            produced_from = response['producedFrom']
            for product in produced_from:
                id = product['db_number']['db_letter']
                quantity = product['amount']
                product_dict = {}
                product_dict['db_number'] = id
                product_dict['quantity'] = quantity
                # print('product_dict: ' + str(product_dict))
                produced_from_formatted.append(product_dict)

            # output_list.append(produced_from_formatted)

        return produced_from_formatted

        # Now that I have a list which gives me all the required ingredients and their quantities, I need to find
        # out the sourcing price for those times."""

    # Because we have to handle multiply of ingredients, I'm using a very similar but crucially different function
    # for all the steps after 1.

    # Formats the data so we don't need to do somethin weird for the first loop
    data = {}
    data['db_number'] = db_number
    data['quantity'] = loops
    data['quality'] = target_quality
    data = [data]
    #print(steps)
    for step in range(steps + 1):
        #print('Step ' + str(step))
        data = More_Step_Production(data, 0, step)
        #print('After step ' + str(step) + ':' + str(data))
        # print("")

    temp = {}
    paired_ids = []
    all_pairs = []

    # print('Pre matching')
    # for x in data:
    # print(x)
    # print("")

    for x in data:

        # print('x' + str(x))
        db_num1 = x['db_number']
        quantity1 = x['quantity']
        quality1 = x['quality']
        paired_ids.clear()
        for y in data:
            # print('y' + str(y))
            db_num2 = y['db_number']
            quantity2 = y['quantity']
            quality2 = y['quality']
            temp.clear()
            if y != x:
                # print('Non matching:')
                # print(y)
                # print(x)
                # print('y: ' + str(y) + ', does not match x: ' + str(x))
                # print(db_num1,db_num2)
                # print(quantity1,quantity2)
                # print(quality1,quality2)
                if db_num1 == db_num2 and quality1 == quality2:
                    temp['db_number'] = db_num1
                    temp['quality'] = quality1
                    temp['quantity'] = quantity1 + quantity2
                    # print('Paired: ' + str(temp))
                    # print('Looking for '+  str(x) + str(id(x)) + ' in ' + str(data))
                    position = data.index(x)
                    # print('Before removing: ' + str(data))
                    # print('Removed: ' + str(x) + ', ' + str(y))
                    data.remove(x)
                    data.remove(y)
                    data.insert(position - 1, temp.copy())
                    x = temp.copy()
                    # print('After insterted: ' + str(data))
                    db_num1 = x['db_number']
                    quantity1 = x['quantity']
                    quality1 = x['quality']

        # print("")

    # print('After pairing' + str(data))

    return data


# Ok, so now I can calculate the ingredients needed for any number of steps. Here are what I still need:
# Work out the profit per hour per level.
# Profit per hour:
# Calculate the cost of ingredients from exchange data using the Any_Step_Production output (relatively easy). DONE
# Use the potential sale price (I can't realistically get the top 95% the whole time if I make a high quantity of them.
# 50% is more realistic. Use this to calculate profit per unit.
# Then multiply profit per unit by produced per hour.
# Then divide by total buildings used depending on how many steps there were. Keep a note of how may of each this is,
#
# Chart Profit per Hour per Level for every product and every Q. Then manually go through the top 20 or so and work
# out why they aren't realistic. Adapt the code to stop these being so stupidly profitable, get something more realistic.

# Perhaps Profit per Hour per Level for retail too? Probably a bit hard but looking back at some old excel files
# would help.

def Ingredient_Costs(input):
    # Returns an array of [meh price, best price] Note that best price is not actually best possible price but both
    # prices help for a comparison with other goods for estimating profit.

    meh_case_total_cost = 0
    best_case_total_cost = 0
    #print('Ingredient costs input: ' + str(input))
    # Seperates each ingredient
    for ingredient in input:
        db_number = ingredient['db_number']
        quality = ingredient['quality']
        quantity = ingredient['quantity']
        try:
            file_name = str(db_number) + '.txt'
            with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\TargetCalulations', file_name),
                      "r") as file1:
                target_prices = eval(file1.read())
                file1.close()
            # print(target_prices)
        except FileNotFoundError:
            # print('WARNING: The price for this does not include the cost of the ' +str(number_name_dict[db_number]) + ' as you would need to source it but it is not listed on the exchange and hence I have no data for it!')
            return 'NOMARKETDATA'

        # print('Target Prices: ' + str(target_prices))
        # Sets the data we want to match the quality for this ingredient
        market_info = 'NULL'
        for x in target_prices:
            # print(x)
            if x['quality'] == quality:
                market_info = x
                break
        # print(market_info)

        if market_info == 'NULL':
            # print("I have no data for this, but it could potentially be sold on the exchange so it's a valid item to look at!")
            return 'NOMARKETDATA'

        meh_case_total_cost = meh_case_total_cost + (quantity * market_info['average_market_price'])
        best_case_total_cost = best_case_total_cost + (quantity * market_info['best_market_buy_price'])

    # print(meh_case_total_cost)
    # print(best_case_total_cost)
    # print("")
    return {'meh_price': meh_case_total_cost, 'best_price': best_case_total_cost}


def Worker_Costs(db_number,loop):
    # Worker costs = Quantity * (Building running cost / items produced per hour)
    # Building levels are irellevant at this stage, but the admin costs should be applied to the worker costs later.
    quantity = loop

    try:
        file_name = str(db_number) + '.txt'
        with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\Encyclopedia', file_name),
                  "r") as file1:
            encyclopedia_data = eval(file1.read())
            file1.close()
        # print(target_prices)
    except FileNotFoundError:
        print('Error could not find file: ' + str(file_name))

    produced_per_hour = encyclopedia_data['producedAnHour']
    building = encyclopedia_data['producedAt']['db_letter']
    #print('Produced per hour: ' + str(produced_per_hour))
    #print('BUildig: ' + str(building))

    # print(encyclopedia_data)
    wages = encyclopedia_data['baseSalary']

    cost = quantity * (wages / produced_per_hour)

    #This following data can give you the worker cost of the 1st level ingredients. That's not actually what we want here.
    r"""
    for ingredient in input:
        db_number = ingredient['db_number']
        quantity = ingredient['quantity']
        #print('Quantity ' + str(quantity))
        #print(db_number)
        try:
            file_name = str(db_number) + '.txt'
            with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\Encyclopedia', file_name),
                      "r") as file1:
                encyclopedia_data = eval(file1.read())
                file1.close()
            # print(target_prices)
        except FileNotFoundError:
            print('Error could not find file: ' + str(file_name))

        produced_per_hour = encyclopedia_data['producedAnHour']
        building = encyclopedia_data['producedAt']['db_letter']
        print('Produced per hour: ' + str(produced_per_hour))
        print('BUildig: ' + str(building))

        # print(encyclopedia_data)
        wages = encyclopedia_data['baseSalary']

        cost = quantity * (wages / produced_per_hour)
        costs = costs + cost
    """
    # print(costs)
    # print("")
    return cost


def Combine_duplicates(a):
    # ONLY combines if it has matching db numbs, does not consider quality.
    temp = {}
    paired_ids = []
    for x in a:

        # print('x' + str(x))
        db_num1 = x['db_number']
        quantity1 = x['quantity']
        paired_ids.clear()
        for y in a:
            # print('y' + str(y))
            db_num2 = y['db_number']
            quantity2 = y['quantity']
            temp.clear()
            if y != x:
                # print('Non matching:')
                # print(y)
                # print(x)
                # print('y: ' + str(y) + ', does not match x: ' + str(x))
                # print(db_num1,db_num2)
                # print(quantity1,quantity2)
                # print(quality1,quality2)
                if db_num1 == db_num2:
                    temp['db_number'] = db_num1
                    temp['quantity'] = quantity1 + quantity2
                    # print('Paired: ' + str(temp))
                    # print('Removed: ' + str(x) + ', ' + str(y))
                    position = a.index(x)
                    a.remove(x)
                    a.remove(y)
                    a.insert(position - 1, temp.copy())
                    x = temp.copy()
                    db_num1 = x['db_number']
                    quantity1 = x['quantity']
        # print("")
    return a


# Input the standard variables, output a list of every item you make at step 1 AND every item you make at step 2 ect ect.
def all_steps_ingredients_combined(db_num, steps, loops):
    # We can just use this code as it already does exactly what we need, plus a bit more.
    everything_to_make = []
    for step in range(steps):
        if step == 0:
            d = {'db_number': db_num, 'quantity': loops, 'quality': 0}
            data = More_Step_Production([d], 0, 1)
        if step > 0:
            data = More_Step_Production(data, 0, 1)
        # print(data)

        # Blatenly stolen this bit of code from the other function
        temp = {}
        paired_ids = []
        for x in data:

            # print('x' + str(x))
            db_num1 = x['db_number']
            quantity1 = x['quantity']
            paired_ids.clear()
            for y in data:
                # print('y' + str(y))
                db_num2 = y['db_number']
                quantity2 = y['quantity']
                temp.clear()
                if y != x:
                    # print('Non matching:')
                    # print(y)
                    # print(x)
                    # print('y: ' + str(y) + ', does not match x: ' + str(x))
                    # print(db_num1,db_num2)
                    # print(quantity1,quantity2)
                    # print(quality1,quality2)
                    if db_num1 == db_num2:
                        temp['db_number'] = db_num1
                        temp['quantity'] = quantity1 + quantity2
                        # print('Paired: ' + str(temp))
                        # print('Removed: ' + str(x) + ', ' + str(y))
                        position = data.index(x)
                        data.remove(x)
                        data.remove(y)
                        data.insert(position - 1, temp.copy())
                        x = temp.copy()
                        db_num1 = x['db_number']
                        quantity1 = x['quantity']
            # print("")

        # Add it to the list of everything we make so we can calculate how long thats gonna take.
        everything_to_make.extend(data)

        # Remove the power so it doesn't get double logged.
        for x in data:
            if x['db_number'] == 1:
                data.remove(x)
                # print('Removed ' + str(x))

        for x in data:
            # print('x in data' + str(x))
            db_number = x['db_number']
            try:
                file_name = str(db_num) + '.txt'
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\Encyclopedia', file_name),
                          "r") as file1:
                    info = eval(file1.read())
                    file1.close()
                # print(target_prices)
            except FileNotFoundError:
                print('WARNING: The price for this does not include the cost of the ' + str(number_name_dict[
                                                                                                db_number]) + ' as it is not listed on the exchange and hence I have no data for it!')
        # print("")

    # NB: This wasn't included before but it looked like it belonger here so.. I put it here.
    everything_to_make = Combine_duplicates(everything_to_make)
    return everything_to_make


# I have realised I don't need 90% of this. Feel free to repurpose this function. Also not 100% sure it's iterating properly.
def time_to_make(ingredients):
    total_time_to_make = 0
    for x in ingredients:
        db_number = x['db_number']
        quantity = x['quantity']
        try:
            file_name = str(db_number) + '.txt'
            with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\Encyclopedia', file_name),
                      "r") as file1:
                encyclopedia_info = eval(file1.read())
                file1.close()
        except FileNotFoundError:
            print('File not found for: ' + str(number_name_dict[db_number]))

        # print(encyclopedia_info)
        produced_per_hour = encyclopedia_info['producedAnHour']
        time_to_produce = 1 / produced_per_hour
        subtotal_time_to_produce = time_to_produce * quantity
        # print(subtotal_time_to_produce)
        total_time_to_make = total_time_to_make + subtotal_time_to_produce
    return total_time_to_make


def buildings_needed(db_number, steps, slots, loops, encyclopedia_info):
    # This is gonna get complex, because I want to work out the best way to balance out the slots as well as the levels.
    all_ingredients = all_steps_ingredients_combined(db_number, steps, loops)
    total_levels = 0
    #print('ALl ingredients: ' + str(all_ingredients))

    # print(encyclopedia_info)
    main_produced_per_hour = encyclopedia_info['producedAnHour']
    main_building = encyclopedia_info['producedAt']['name']

    #print('Main produced per H: ' + str(main_produced_per_hour))
    buildings_needed_dict = {}
    buildings_needed_dict[main_building] = loops
    # Work out how many factories we need to make main_produced_per_hour of the top level unit. I think?

    for x in all_ingredients:
        db_number = x['db_number']
        quantity = x['quantity']

        file_name = db_number
        with open(
                os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\Encyclopedia', str(file_name)) + '.txt',
                "r") as file1:
            encyclopedia_info = eval(file1.read())
            file1.close()

        #quantity_produced_per_hour = encyclopedia_data['producedAnHour']


        #print(x)

        ingredient_produced_per_hour = encyclopedia_info['producedAnHour']

        building = encyclopedia_info['producedAt']['name']

        #print('Ingredient produced per H: ' + str(ingredient_produced_per_hour))

        ingredient_factories_needed = (main_produced_per_hour * quantity) / ingredient_produced_per_hour

        #print(str(encyclopedia_info['producedAt']['name']) +' needed: ' + str(ingredient_factories_needed))
        try:
            buildings_needed_dict[building] = buildings_needed_dict[main_building] + ingredient_factories_needed
        except KeyError:
            buildings_needed_dict[building] = ingredient_factories_needed

        total_levels = total_levels + ingredient_factories_needed
    #print("")
    #print(buildings_needed_dict)
    # print(sum(buildings_needed_dict.values()))

    # Not sure how to do this rn at it's 2:30, but basically we need to guarentee both that every main_building will be in
    # the final list, the list will have a length of 'slots' and that we don't just divide by 2 and double the
    # spaces. We have to divide the lvls of this main_building until it is no longer the max level main_building, then record
    # that we have done that but also be able to go back to it and divide it again.

    # print(buildings_needed_dict)

    def split_levels(nr_variables, value):
        cents = value * 100

        base = cents // nr_variables
        rem = int(cents % nr_variables)

        return [(base + 1) / 100] * rem + [base / 100] * (nr_variables - rem)

    def building_lvl_redistrbiute(dict, slots):
        import heapq

        # dict = {'apples': 2, 'banannas': 12, 'cats': 5, 'dogs': 7}
        N = slots
        K = len(dict)

        if N < K:
            # print('ERROR. There are less slots provided than there are needed.')
            # print('Provided: ' + str(N))
            # print('Needed: ' + str(K))
            return 'NOTENOUGHSLOTS'

        items = [(-math.ceil(value), math.ceil(value), 1, key) for key, value in dict.items()]
        heapq.heapify(items)
        for i in range(N - K):
            item = heapq.heappop(items)
            div = item[2] + 1
            heapq.heappush(items, (-((item[1] + div - 1) // div), item[1], div, item[3]))

        #print(items)
        output_list = []
        for i in items:
            # print(i)
            output_dict = {}
            output_dict['Building'] = i[3]

            # Gives us a list of the levels that will be made of this main_building.
            if i[1] % i[2] == 0:
                # If the remainder = 0, just run the function
                b = split_levels(i[2], i[1])
            else:
                a = split_levels(i[2], i[1])
                if max(a) == min(a):
                    # If the remainder != but after running the function the max and min values of the main_building
                    # levels are the same, then the output will be fine.
                    b = a
                else:
                    b = []
                    # If the max and min aren't equal, round all the max values up and the min values down.
                    for x in a:
                        if x == max(a):
                            b.append(math.ceil(x))
                        elif x == min(a):
                            b.append(math.floor(x))

            building_cost = encyclopedia_info['producedAt']['cost']  # Lvl 1 cost to construct main_building.

            #print('Cyc info: ' + str(encyclopedia_info))
            #(encyclopedia_info['producedAt']['cost'])
            total_building_cost = 0 + building_cost


            for x in b:
                for y in range(int(x)):
                    if y == 0:
                        y = 1
                    #print('Level: ' + str(y))
                    #print('Adding: ' + str((y)*building_cost))
                    total_building_cost = total_building_cost + ((y) * building_cost)
                    #print(total_building_cost)

            # print("")
            output_dict['Levels'] = b.copy()
            output_dict['Cost_To_build'] = total_building_cost
            output_list.append(output_dict)

        return output_list

    # print('Buildings needed = ' + str(buildings_needed_dict))
    shared_buildings = building_lvl_redistrbiute(buildings_needed_dict, slots)
    # print('Shared buildings = ' + str(shared_buildings))

    total_of_building_levels = 0
    total_of_building_costs = 0

    if shared_buildings == 'NOTENOUGHSLOTS':
        return {'Admin_overhead': 0}, 'NOTENOUGHSLOTS'
    #print(shared_buildings)
    for x in shared_buildings:
        #print(x)
        total_of_building_levels = total_of_building_levels + sum(x['Levels'])
        total_of_building_costs = total_of_building_costs + x['Cost_To_build']
    # print('Total number of buildings: ' + str(total_of_building_levels))

    # Admin % = (total main_building lvls - 1) / 170
    admin_overhead = (total_of_building_levels - 1) / 170
    # print(total_of_building_levels)
    #print('Admin overhead: ' + str(admin_overhead))
    #print('Cost to build: ' + str(total_of_building_costs))
    general_info = {}
    general_info['Admin_overhead'] = admin_overhead
    general_info['Investment'] = total_of_building_costs
    return general_info, shared_buildings


def potential_profit(db_number, target_quality, steps, override_sale_price):


    file_name = db_number
    with open(
            os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\Encyclopedia', str(file_name)) + '.txt',
            "r") as file1:
        encyclopedia_data = eval(file1.read())
        file1.close()

    quantity_produced_per_hour = encyclopedia_data['producedAnHour']
    ####

    file_name = db_number
    try:
        method = 'ExchangeData'
        with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\TargetCalulations',
                               str(file_name)) + '.txt', "r") as file1:
            sale_prices = eval(file1.read())
            file1.close()

        unit_sale_info = 'NULL'

        for x in sale_prices:
            if x['quality'] == target_quality:
                unit_sale_info = x
                break

        # print(unit_sale_info)

        if unit_sale_info == 'NULL':
            #print('Sale info was null so returned "NOMARKETDATA"')
            return 'NOMARKETDATA', 0  # The 0 here for the number of loops is there because I assume if we have no market data, it is pointless knowing how many loops we've done. This might be wrong.
    except:
        method = 'ManualData'

    time_d = time.time()
    timings_e = []
    timings_f = []
    timings_g = []
    timings_h = []
    timings_i = []
    # This is what takes all the time up rn. If I could find a quick way to maybe do every 50th and then narrow it
    # down to between the top 2 highest. Even better if I narrow it down further. The most efficent way to narrow it
    # down (I think) is to go half, then half again, then half again ect.


    # Instead of going through EVERY loop (A loop is actually the number of lvls of the topmost building), we go through these loop numbers. We the filter down to the top 3 profits (by estimated), that way we can be 100% certain that the max profit loop is within those 3 (The curve is not bell shaped so we can't be certain that it is between the top 2). Then we just go through every single loop between the 2 loop numbers that are futherest from eachother.

    initial_loops = [0,5,15,30,50,75,105,140,195,245,300,360,425,495,570,650,735,825,920,1000]

    """if method == 'ManualData':
        print('Using override price: ' + str(override_sale_price) + 'for a Q' + str(target_quality) + ' ' + str(
        number_name_dict[db_number]))"""


    loop_list= []
    try:
        estimated_daily_profit = 0
        max_daily_profit = 0
        min_daily_profit = 0
        for loop in initial_loops:
            loop = loop + 1
            new_quantity_produced_per_hour = quantity_produced_per_hour * loop
            old_daily_profit = estimated_daily_profit
            old_max_daily_profit = max_daily_profit
            old_min_daily_profit = min_daily_profit

            #print('Loop ' + str(loop))
            time_e = time.time()
            base_data = Any_Step_Production(db_number, target_quality, steps, loop)
            # print(base_data)
            # print(base_data)
            time_f = time.time()
            admin_overhead = buildings_needed(db_number, steps, slots, loop, encyclopedia_data)[0]['Admin_overhead']
            #print('Admin overhead: ' + str(admin_overhead))
            time_g = time.time()
            ingredient_costs = Ingredient_Costs(base_data)
            time_h = time.time()
            worker_costs = Worker_Costs(db_number, loop) * (1 + admin_overhead)
            time_i = time.time()
            #print('Ingredient costs: '+ str(ingredient_costs))
            #print('Worker costs: ' + str(worker_costs))
            if ingredient_costs == 'NOMARKETDATA':
                # print('Returned no market data in potential profit')
                return 'NOMARKETDATA', 0
            meh_costs = (ingredient_costs['meh_price'] + worker_costs ) / loop
            best_costs = (ingredient_costs['best_price'] + worker_costs) / loop
            #print('Best costs ' + str(best_costs / loop))
            #print('Unit sale info: ' + str(unit_sale_info))

            if method == 'ExchangeData':

                profit1 = unit_sale_info['best_sell_price'] - meh_costs
                profit2 = unit_sale_info['best_sell_price'] - best_costs
                profit3 = unit_sale_info['average_market_price'] - meh_costs
                profit4 = unit_sale_info['average_market_price'] - best_costs

                max_unit_profit = max(profit4, profit3, profit2, profit1)
                min_unit_profit = min(profit4, profit3, profit2, profit1)
                estimated_unit_profit = sum([profit4, profit3, profit2, profit1]) / 4
            elif method == 'ManualData':
                #print('Using override price: ' + str(override_sale_price) + 'for a Q' +str(target_quality) + ' ' +str(number_name_dict[db_number]) )
                profit1 = (override_sale_price) - (meh_costs)
                profit2 = (override_sale_price) - (best_costs)

                max_unit_profit = max(profit2, profit1)
                min_unit_profit = min(profit2, profit1)
                # print(profit2)
                # print(profit1)
                estimated_unit_profit = (profit2 + profit1) / 2
                # print(estimated_unit_profit)

            max_daily_profit = new_quantity_produced_per_hour * 24 * max_unit_profit
            min_daily_profit = new_quantity_produced_per_hour * 24 * min_unit_profit
            estimated_daily_profit = new_quantity_produced_per_hour * 24 * estimated_unit_profit
            #print('Unit profit: ' + str(estimated_unit_profit))
            # print('Daily produced: ' + str(new_quantity_produced_per_hour))
            # print('Daily profit: ' + str(estimated_daily_profit))

            time_j = time.time()

            timings_e.append(time_e - time_d)
            timings_f.append(time_f - time_e)
            timings_g.append(time_g - time_f)
            timings_h.append(time_h - time_g)
            timings_i.append(time_i - time_h)
            # print('Estimated unit profit: ' + str(estimated_unit_profit)

            if old_daily_profit > estimated_daily_profit:
                #print('Initially broke on loop ' + str(loop))
                # print('Timings report...')
                # print(sum(timings_e) / len(timings_e))
                # print(sum(timings_f) / len(timings_f))
                # print(sum(timings_g) / len(timings_g))
                # print(sum(timings_h) / len(timings_h))
                # print(sum(timings_i) / len(timings_i))
                class ProfitOverflow(Exception): pass
                raise ProfitOverflow

            if loop == 1001:
                print('We hit 1000 loops in the initial loop')  # . Here is the timings report...')
                # print(sum(timings_e) / len(timings_e))
                # print(sum(timings_f) / len(timings_f))
                # print(sum(timings_g) / len(timings_g))
                # print(sum(timings_h) / len(timings_h))
                # print(sum(timings_i) / len(timings_i))
                return [old_max_daily_profit, old_min_daily_profit, old_daily_profit] , loop
    except ProfitOverflow:
        #print('Overflow on loop ' + str(loop))
        if loop == 1:
            return [old_max_daily_profit, old_min_daily_profit, old_daily_profit], loop
        elif loop == 1001:
            return [old_max_daily_profit, old_min_daily_profit, old_daily_profit], loop
        elif loop == 6:
            initial_loop_index = initial_loops.index(loop-1)
            min_range = initial_loops[initial_loop_index - 1]
            max_range = initial_loops[initial_loop_index]

        else:
            initial_loop_index = initial_loops.index(loop-1)
            min_range = initial_loops[initial_loop_index-2]
            max_range = initial_loops[initial_loop_index]

    estimated_daily_profit = 0
    max_daily_profit = 0
    min_daily_profit = 0
    for loop in range(min_range,max_range):
        loop = loop + 1
        new_quantity_produced_per_hour = quantity_produced_per_hour * loop
        old_daily_profit = estimated_daily_profit
        old_max_daily_profit = max_daily_profit
        old_min_daily_profit = min_daily_profit

        #print('Loop ' + str(loop))
        time_e = time.time()
        base_data = Any_Step_Production(db_number, target_quality, steps, loop)
        # print(base_data)
        # print(base_data)
        time_f = time.time()
        admin_overhead = buildings_needed(db_number, steps, slots, loop, encyclopedia_data)[0]['Admin_overhead']
        #print('Admin overhead: ' + str(admin_overhead))
        time_g = time.time()
        ingredient_costs = Ingredient_Costs(base_data)
        time_h = time.time()
        worker_costs = Worker_Costs(db_number, loop) * (1 + admin_overhead)
        time_i = time.time()
        # print('Ingredient costs: '+ str(ingredient_costs))
        # print('Worker costs: ' + str(worker_costs))
        if ingredient_costs == 'NOMARKETDATA':
            # print('Returned no market data in potential profit')
            return 'NOMARKETDATA', 0
        meh_costs = ingredient_costs['meh_price'] + worker_costs
        best_costs = ingredient_costs['best_price'] + worker_costs
        #print('Best costs ' + str(best_costs / loop))

        if method == 'ExchangeData':

            profit1 = (unit_sale_info['best_sell_price']) - (meh_costs / loop)
            profit2 = (unit_sale_info['best_sell_price']) - (best_costs / loop)
            profit3 = (unit_sale_info['average_market_price']) - (meh_costs / loop)
            profit4 = (unit_sale_info['average_market_price']) - (best_costs / loop)

            max_unit_profit = max(profit4, profit3, profit2, profit1)
            min_unit_profit = min(profit4, profit3, profit2, profit1)
            estimated_unit_profit = sum([profit4, profit3, profit2, profit1]) / 4
        elif method == 'ManualData':
            #print('Using override price')
            # print('Override sale price: ' + str(override_sale_price))
            profit1 = (override_sale_price) - (meh_costs / loop)
            profit2 = (override_sale_price) - (best_costs / loop)

            max_unit_profit = max(profit2, profit1)
            min_unit_profit = min(profit2, profit1)
            # print(profit2)
            # print(profit1)
            estimated_unit_profit = (profit2 + profit1) / 2
            # print(estimated_unit_profit)

        max_daily_profit = new_quantity_produced_per_hour * 24 * max_unit_profit
        min_daily_profit = new_quantity_produced_per_hour * 24 * min_unit_profit
        estimated_daily_profit = new_quantity_produced_per_hour * 24 * estimated_unit_profit
        #print('Unit profit: ' + str(estimated_unit_profit))
        #print('Daily produced: ' + str(new_quantity_produced_per_hour))
        #print('Daily profit: ' + str(estimated_daily_profit))

        time_j = time.time()

        timings_e.append(time_e - time_d)
        timings_f.append(time_f - time_e)
        timings_g.append(time_g - time_f)
        timings_h.append(time_h - time_g)
        timings_i.append(time_i - time_h)
        # print('Estimated unit profit: ' + str(estimated_unit_profit)

        if old_daily_profit > estimated_daily_profit:
            #print('Broke on loop ' + str(loop))
            # print('Timings report...')
            # print(sum(timings_e) / len(timings_e))
            # print(sum(timings_f) / len(timings_f))
            # print(sum(timings_g) / len(timings_g))
            # print(sum(timings_h) / len(timings_h))
            # print(sum(timings_i) / len(timings_i))
            return [old_max_daily_profit, old_min_daily_profit, old_daily_profit], loop

        if loop == 1001:
            print('We hit 1000 loops in the latter loop')  # . Here is the timings report...')
            # print(sum(timings_e) / len(timings_e))
            # print(sum(timings_f) / len(timings_f))
            # print(sum(timings_g) / len(timings_g))
            # print(sum(timings_h) / len(timings_h))
            # print(sum(timings_i) / len(timings_i))
            return [old_max_daily_profit, old_min_daily_profit, old_daily_profit], loop


def DailyProfitCalculation(db_number, target_quality, steps, slots, override_sale_price, start_time):
    # print('Starting Daily profit calc')
    time_a = time.time()
    output4, loops = potential_profit(db_number, target_quality, steps, override_sale_price)
    time_b = time.time()
    # print('Marker B: ' + str(time_b-time_a))
    #print('Output 4: '+ str(output4))
    # print('Starting buldings')
    # print('Got potential profit')
    try:
        file_name = db_number
        with open(
                os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\Encyclopedia', str(file_name)) + '.txt',
                "r") as file1:
            encyclopedia_data = eval(file1.read())
            file1.close()
    except FileNotFoundError:
        print('Error file not found:' + str(file_name))

    output5 = buildings_needed(db_number, steps, slots, loops, encyclopedia_data)
    time_c = time.time()
    # print('Marker C: ' + str(time_c-time_b))
    # print('Got buildings needed')
    if output4 == 'NOMARKETDATA':
        #print('No Market Data')
        output4 = [0, 0, 0]
    result = [output4, output5]
    return result


slots = 13

# DailyProfitCalculation(db_number, target_quality, steps, slots,override_sale_price)

# Things still to add:
# Worker cost to make stuff.
# I currently output unit price from potential_profit(),this needs to be multiplied by the produced per hour of the top building to output a profit per hour.
# I may need some consideration in the above statement for number of slots used.
# Tie it all together.
# Iterate through every possible cobination of steps, slots, qualities. Output a single value, profit per day.
# Chart the highest profit per days, work out what is missing to filter out all the false positives.
#

file_name = 'ManualPrices.txt'
with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', file_name),
          "r") as file1:
    manualprices = eval(file1.read())
    file1.close()


# print(type(manualprices))

# manualprices = [{'Market Phase': 'Normal', 'Data Source': 'STH Ventures', 'Products': [{'Product Name': 'Lux Jet', 'Quality': 4, 'Price': 88000}, {'Product Name': 'SEP', 'Quality': 3, 'Price': 35000}, {'Product Name': 'Jumbo Jet', 'Quality': 4, 'Price': 245000}, {'Product Name': 'SEP', 'Quality': 7, 'Price': 39000}, {'Product Name': 'SOR', 'Quality': 4, 'Price': 121000}]}, {'Market Phase': 'Normal', 'Data Source': 'Fridule', 'Products': [{'Product Name': 'Satellite', 'Quality': 6, 'Price': 62000},{'Product Name': 'Gold bars', 'Quality': 4, 'Price': 6300}]}, {'Market Phase': 'Recession', 'Data Source': 'planet Express', 'Products': [{'Product Name': 'Gold bars', 'Quality': 4, 'Price':6300}, {'Product Name': 'Gold bars', 'Quality': 5, 'Price':6400}, {'Product Name': 'Gold bars', 'Quality': 6, 'Price':6500}, {'Product Name': 'Gold bars', 'Quality': 7, 'Price':6600}, {'Product Name': 'Gold bars', 'Quality': 8, 'Price':6700}, {'Product Name': 'Gold bars', 'Quality': 9, 'Price':6800}]}, {'Market Phase': 'Normal', 'Data Source': '323 Enterprises', 'Products': [{'Product Name': 'BFR', 'Quality': 4, 'Price':880000}, {'Product Name': 'BFR', 'Quality': 5, 'Price':960000}, {'Product Name': 'BFR', 'Quality': 6, 'Price':1040000}, {'Product Name': 'BFR', 'Quality': 7, 'Price':1120000}, {'Product Name': 'BFR', 'Quality': 8, 'Price':1200000}, {'Product Name': 'BFR', 'Quality': 9, 'Price':1280000}]}, {'Market Phase': 'Normal', 'Data Source': 'Giga Corporation', 'Products': [{'Product Name': 'Starship', 'Quality': 0, 'Price':90000}, {'Product Name': 'Starship', 'Quality': 1, 'Price':100000}, {'Product Name': 'Starship', 'Quality': 2, 'Price':110000}, {'Product Name': 'Starship', 'Quality': 3, 'Price':120000}, {'Product Name': 'Starship', 'Quality': 4, 'Price':130000}, {'Product Name': 'Starship', 'Quality': 5, 'Price':140000}, {'Product Name': 'Starship', 'Quality': 6, 'Price':150000}, {'Product Name': 'Starship', 'Quality': 7, 'Price':160000}, {'Product Name': 'Starship', 'Quality': 8, 'Price':170000}, {'Product Name': 'Starship', 'Quality': 9, 'Price':180000}]}, {'Market Phase': 'Normal', 'Data Source': 'JCA Motors', 'Products': [{'Product Name': 'Satellite', 'Quality': 2, 'Price':56000}, {'Product Name': 'Satellite', 'Quality': 3, 'Price':57000}, {'Product Name': 'Satellite', 'Quality': 4, 'Price':58000}, {'Product Name': 'Satellite', 'Quality': 5, 'Price':59000}, {'Product Name': 'Satellite', 'Quality': 6, 'Price':60000}, {'Product Name': 'Satellite', 'Quality': 7, 'Price':61000}, {'Product Name': 'Satellite', 'Quality': 8, 'Price':62000}, {'Product Name': 'Satellite', 'Quality': 9, 'Price':63000}]}, {'Market Phase': 'Normal', 'Data Source': 'Whitehawk', 'Products': [{'Product Name': 'Lux Jet', 'Quality': 3, 'Price':86000}, {'Product Name': 'Lux Jet', 'Quality': 4, 'Price':87500}, {'Product Name': 'Lux Jet', 'Quality': 5, 'Price':89000}, {'Product Name': 'Lux Jet', 'Quality': 6, 'Price':90500}, {'Product Name': 'Lux Jet', 'Quality': 7, 'Price':92000}, {'Product Name': 'Lux Jet', 'Quality': 8, 'Price':93500}, {'Product Name': 'Lux Jet', 'Quality': 9, 'Price':95000}, ]}, {'Market Phase': 'Normal', 'Data Source': 'chaos production', 'Products': [{'Product Name': 'Economy E-car', 'Quality': 3, 'Price':3330}, {'Product Name': 'Economy E-car', 'Quality': 4, 'Price':3356}, {'Product Name': 'Economy E-car', 'Quality': 5, 'Price':3382}, {'Product Name': 'Economy E-car', 'Quality': 6, 'Price':3408}, {'Product Name': 'Economy E-car', 'Quality': 7, 'Price':3434}, {'Product Name': 'Economy E-car', 'Quality': 8, 'Price':3460}, {'Product Name': 'Economy E-car', 'Quality': 9, 'Price':3486},   ]}, {'Market Phase': 'Normal', 'Data Source': 'Holy moly', 'Products': [{'Product Name': 'SEP', 'Quality': 4, 'Price':37000}, {'Product Name': 'SEP', 'Quality': 5, 'Price':38500}, {'Product Name': 'SEP', 'Quality': 6, 'Price':40000}, {'Product Name': 'SEP', 'Quality': 7, 'Price':41500}, {'Product Name': 'SEP', 'Quality': 8, 'Price':43000}, {'Product Name': 'SEP', 'Quality': 9, 'Price':44500}]}, {'Market Phase': 'These prices arent linked to a market phase.', 'Data Source': 'FL SETUSA SA', 'Products': [{'Product Name': 'Solid Fuel Booster', 'Quality': 2, 'Price':8200}, {'Product Name': 'Solid Fuel Booster', 'Quality': 3, 'Price':8400}, {'Product Name': 'Solid Fuel Booster', 'Quality': 4, 'Price':8600}, {'Product Name': 'Solid Fuel Booster', 'Quality': 5, 'Price':8800}, {'Product Name': 'Solid Fuel Booster', 'Quality': 6, 'Price':9000}, {'Product Name': 'Solid Fuel Booster', 'Quality': 7, 'Price':9200}, {'Product Name': 'Solid Fuel Booster', 'Quality': 8, 'Price':9400}, {'Product Name': 'Solid Fuel Booster', 'Quality': 9, 'Price':9600}]}, {'Market Phase': 'Normal', 'Data Source': 'Levanter Trading Co', 'Products': [{'Product Name': 'Satellite', 'Quality': 2, 'Price': 58000}]}, {'Market Phase': 'Normal', 'Data Source': 'STONKA LLC', 'Products': [{'Product Name': 'BFR', 'Quality': 5, 'Price':911000}, {'Product Name': 'BFR', 'Quality': 6, 'Price':929000}, {'Product Name': 'BFR', 'Quality': 7, 'Price':947000}, {'Product Name': 'BFR', 'Quality': 8, 'Price':965000}, {'Product Name': 'BFR', 'Quality': 9, 'Price':983000}]}, {'Market Phase': 'Normal', 'Data Source': 'Tia Corp', 'Products': [{'Product Name': 'SOR', 'Quality': 4, 'Price':120000}, {'Product Name': 'SOR', 'Quality': 5, 'Price':122000}, {'Product Name': 'SOR', 'Quality': 6, 'Price':124000}, {'Product Name': 'SOR', 'Quality': 7, 'Price':126000}, {'Product Name': 'SOR', 'Quality': 8, 'Price':128000}, {'Product Name': 'SOR', 'Quality': 9, 'Price':130000}, ]}, {'Market Phase': 'Normal', 'Data Source': 'Coss Enterprises', 'Products': [{'Product Name': 'SEP', 'Quality': 5, 'Price':38000}, {'Product Name': 'SEP', 'Quality': 6, 'Price':39000}, {'Product Name': 'SEP', 'Quality': 7, 'Price':40000}, {'Product Name': 'SEP', 'Quality': 8, 'Price':41000}, {'Product Name': 'SEP', 'Quality': 9, 'Price':42000}]}, {'Market Phase': 'Normal', 'Data Source': 'WestCounce Corp', 'Products': [{'Product Name': 'BFR', 'Quality': 5, 'Price': 910000}, {'Product Name': 'Jumbo Jet', 'Quality': 3, 'Price': 240000}, {'Product Name': 'Lux Jet', 'Quality': 3, 'Price': 85000},  {'Product Name': 'SEP', 'Quality': 5, 'Price': 37000}]}, {'Market Phase': 'Normal', 'Data Source': 'NIKOLA SPACE MOTORS ', 'Products': [{'Product Name': 'Satellite', 'Quality': 2, 'Price':55000}, {'Product Name': 'Satellite', 'Quality': 3, 'Price':56500}, {'Product Name': 'Satellite', 'Quality': 4, 'Price':58000}, {'Product Name': 'Satellite', 'Quality': 5, 'Price':59500}, {'Product Name': 'Satellite', 'Quality': 6, 'Price':61000}, {'Product Name': 'Satellite', 'Quality': 7, 'Price':62500}, {'Product Name': 'Satellite', 'Quality': 8, 'Price':64000}, {'Product Name': 'Satellite', 'Quality': 9, 'Price':65500}]}, {'Market Phase': 'Normal', 'Data Source': 'TreeCo', 'Products': [{'Product Name': 'Gold bars', 'Quality': 0, 'Price':6250}, {'Product Name': 'Gold bars', 'Quality': 1, 'Price':6325}, {'Product Name': 'Gold bars', 'Quality': 2, 'Price':6400}, {'Product Name': 'Gold bars', 'Quality': 3, 'Price':6475}, {'Product Name': 'Gold bars', 'Quality': 4, 'Price':6550}, {'Product Name': 'Gold bars', 'Quality': 5, 'Price':6625}, {'Product Name': 'Gold bars', 'Quality': 6, 'Price':6700}, {'Product Name': 'Gold bars', 'Quality': 7, 'Price':6775}, {'Product Name': 'Gold bars', 'Quality': 8, 'Price':6850}, {'Product Name': 'Gold bars', 'Quality': 9, 'Price':6925}, ]}, {'Market Phase': 'Recession', 'Data Source': 'KIMZE ENTERPRISE', 'Products': [{'Product Name': 'Lux Jet', 'Quality': 4, 'Price': 85000}, {'Product Name': 'Jumbo Jet', 'Quality': 3, 'Price': 240000}, {'Product Name': 'Gold bars', 'Quality': 3, 'Price': 6100},  {'Product Name': 'SEP', 'Quality': 3, 'Price': 34000}]}, {'Market Phase': 'Normal', 'Data Source': 'Global Vision Group', 'Products': [{'Product Name': 'Jumbo Jet', 'Quality': 5, 'Price':246000}, {'Product Name': 'Jumbo Jet', 'Quality': 6, 'Price':249000}, {'Product Name': 'Jumbo Jet', 'Quality': 7, 'Price':252000}, {'Product Name': 'Jumbo Jet', 'Quality': 8, 'Price':255000}, {'Product Name': 'Jumbo Jet', 'Quality': 9, 'Price':258000},   ]}, {'Market Phase': 'Normal', 'Data Source': 'KIMZE ENTERPRISE', 'Products': [{'Product Name': 'Lux Jet', 'Quality': 4, 'Price': 87000}, {'Product Name': 'Jumbo Jet', 'Quality': 3, 'Price': 250000}, {'Product Name': 'Gold bars', 'Quality': 3, 'Price': 6400},  {'Product Name': 'SEP', 'Quality': 3, 'Price': 36000}]}, {'Market Phase': 'Normal', 'Data Source': 'S.M', 'Products': [{'Product Name': 'BFR', 'Quality': 3, 'Price':865000}, {'Product Name': 'BFR', 'Quality': 4, 'Price':875000}, {'Product Name': 'BFR', 'Quality': 5, 'Price':885000}, {'Product Name': 'BFR', 'Quality': 6, 'Price':895000}, {'Product Name': 'BFR', 'Quality': 7, 'Price':905000}, {'Product Name': 'BFR', 'Quality': 8, 'Price':915000}, {'Product Name': 'BFR', 'Quality': 9, 'Price':925000}, ]}, {'Market Phase': 'Normal', 'Data Source': 'Lokque Basic Inc', 'Products': [{'Product Name': 'SOR', 'Quality': 3, 'Price':119000}, {'Product Name': 'SOR', 'Quality': 4, 'Price':121000}, {'Product Name': 'SOR', 'Quality': 5, 'Price':123000}, {'Product Name': 'SOR', 'Quality': 6, 'Price':125000}, {'Product Name': 'SOR', 'Quality': 7, 'Price':127000}, {'Product Name': 'SOR', 'Quality': 8, 'Price':129000}, {'Product Name': 'SOR', 'Quality': 9, 'Price':131000}]}, {'Market Phase': 'Normal', 'Data Source': 'CamCor', 'Products': [{'Product Name': 'Jumbo Jet', 'Quality': 3, 'Price':240000}, {'Product Name': 'Jumbo Jet', 'Quality': 4, 'Price':242000}, {'Product Name': 'Jumbo Jet', 'Quality': 5, 'Price':244000}, {'Product Name': 'Jumbo Jet', 'Quality': 6, 'Price':246000}, {'Product Name': 'Jumbo Jet', 'Quality': 7, 'Price':248000}, {'Product Name': 'Jumbo Jet', 'Quality': 8, 'Price':250000}, {'Product Name': 'Jumbo Jet', 'Quality': 9, 'Price':252000}]}, {'Market Phase': 'Normal', 'Data Source': 'Interstellar Tax Evaders', 'Products': [{'Product Name': 'BFR', 'Quality': 3, 'Price': 870000}, {'Product Name': 'Solid Fuel Booster', 'Quality': 3, 'Price': 9250}, {'Product Name': 'Satellite', 'Quality': 2, 'Price': 54000}, {'Product Name': 'Propellant Tank', 'Quality': 2, 'Price': 9400}, {'Product Name': 'SOR', 'Quality': 4, 'Price': 121000}]}, {'Market Phase': 'Normal', 'Data Source': 'Goods Inc', 'Products': [{'Product Name': 'Jumbo Jet', 'Quality': 2, 'Price': 231800}, {'Product Name': 'Gold bars', 'Quality': 2, 'Price': 6050},  {'Product Name': 'Satellite', 'Quality': 3, 'Price': 56500}]}, {'Market Phase': 'Normal', 'Data Source': 'KNRI', 'Products': [{'Product Name': 'Jumbo Jet', 'Quality': 3, 'Price': 241}, {'Product Name': 'Satellite', 'Quality': 3, 'Price': 58}]}, {'Market Phase': 'Normal', 'Data Source': 'Clarky Ltd', 'Products': [{'Product Name': 'Satellite', 'Quality': 2, 'Price':54000}, {'Product Name': 'Satellite', 'Quality': 3, 'Price':55000}, {'Product Name': 'Satellite', 'Quality': 4, 'Price':56000}, {'Product Name': 'Satellite', 'Quality': 5, 'Price':57000}, {'Product Name': 'Satellite', 'Quality': 6, 'Price':58000}, {'Product Name': 'Satellite', 'Quality': 7, 'Price':59000}, {'Product Name': 'Satellite', 'Quality': 8, 'Price':60000}, {'Product Name': 'Satellite', 'Quality': 9, 'Price':61000}]}, {'Market Phase': 'Normal', 'Data Source': 'Eurito', 'Products': [{'Product Name': 'SEP', 'Quality': 5, 'Price':37000}, {'Product Name': 'SEP', 'Quality': 6, 'Price':38000}, {'Product Name': 'SEP', 'Quality': 7, 'Price':39000}, {'Product Name': 'SEP', 'Quality': 8, 'Price':40000}, {'Product Name': 'SEP', 'Quality': 9, 'Price':41000}]}]


# print(type(manualprices))
def Test_Everything():
    All_Profits = []
    # print('Going around ' + str(len(all_db_numbers)) + ' times')
    for db_number in all_db_numbers:
        print(str(round(100 * all_db_numbers.index(db_number) / len(all_db_numbers))) + '%')
        # override_sale_price = 0
        print(number_name_dict[db_number])
        for target_quality in range(0, 6):
            override_sale_price = 0
            for x in manualprices:
                for a in x['Products']:
                    if target_quality == a['Quality']:
                        # print(number_name_dict[db_number],a['Product Name'])
                        if number_name_dict[db_number] == a['Product Name']:
                            # print('Match')
                            # print(db_number)
                            # print(a['Price'])
                            override_sale_price = a['Price']  #

            print('DB Number: ' + str(db_number) + ', Target Quality: ' + str(target_quality) + ', Overide sale price: ' + str(override_sale_price))
            for steps in range(0, 7):
                start_time = time.time()
                #print('Step ' + str(steps))
                Result = DailyProfitCalculation(db_number, target_quality, steps, 14, override_sale_price, start_time)
                # print('Got the result, now to append and go onto the next step.')
                Output = [db_number, target_quality, steps, Result]
                # print(Output)
                All_Profits.append(Output)

    file_name = 'All profits'

    with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', str(file_name)) + '.txt', "w") as file1:
        file1.write(str(All_Profits))
        file1.close()


Test_Everything()
