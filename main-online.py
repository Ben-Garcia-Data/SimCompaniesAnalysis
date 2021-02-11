import requests
import os
import time
import collections
import datetime
import sched


s = sched.scheduler(time.time, time.sleep)


def update_latest_market(db_number, data_sourced_from,main_loop, archive_data):
    # Fetches the latest market data
    market_url = "https://www.simcompanies.com/api/v2/market/"
    time_to_test_against2 = time.time()

    now = datetime.datetime.now()
    clean_response = {}
    response = []
    sold_dict = {}
    dupes = []
    only_in_1 = []
    sold_list = []

    print(str(numbers_dict[db_number]) +' (' + str(db_number)+ ") @ " + str(now) +', had been waiting for ' + str(int(time_differential)) + ' seconds')
    url = market_url + str(db_number)

    if data_sourced_from == 'live':

        def market_fetch(url):
            try:
                market_response = requests.get(url)
                market_response.close()
                market_response = market_response.json()
            except:
                print("Error, could not get API data")
                print('Errortime was:' +str(time.time()))
                time.sleep(5)
                market_response = market_fetch(url)
            return market_response

        # print('Pre-request time elapsed: ' + str(time.time()-time_to_test_against))
        time_neg1 = time.time()
        market_response = market_fetch(url)
        time_0 = time.time()
        # print('API found')
        # time.sleep(1)

        # Write the API result to a history of API results
        def record_whole_market(data_to_store):
            file_name = 'All Market Responses for ' + str(db_number)

            # Timestamp this market.
            current_market = {'time': now, 'data': data_to_store}
            #print('Pre-Saving time elapsed: ' + str(time.time() - time_to_test_against))
            try:
                time_1 = time.time()
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\MarketResults',
                                       str(file_name)) + '.txt', "r") as file1:
                    all_market_responses = eval(file1.read())
                time_2 = time.time()
                all_market_responses.append(current_market)
                time_3 = time.time()
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\MarketResults',
                                       str(file_name)) + '.txt', "w") as file1:
                    file1.write(str(all_market_responses))
                    file1.close()
                time_4 = time.time()

            except FileNotFoundError:
                print('Error no file to read: ' + str(file_name) + '.txt')
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\MarketResults',
                                       str(file_name)) + '.txt', "w") as file1:
                    file1.write(str([current_market]))
                    file1.close()

            except SyntaxError:
                print('Syntax Error')
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\MarketResults',
                                       str(file_name)) + '.txt', "w") as file1:
                    file1.write(str([current_market]))
                    file1.close()

            #times_list.append([time_neg1,time_0,time_1,time_2,time_3,time_4])
           # timings_list[0].append(time_0 - time_neg1)
           # timings_list[1].append(time_1 - time_0)
           # timings_list[2].append(time_2 - time_1)
           # timings_list[3].append(time_3 - time_2)
           # timings_list[4].append(time_4 - time_3)

        # Entire market history saving has been disabled bcus maybe it hurts my hard drive but also it's really slow
        # and recorded sales is all the data I need. Perhaps knowing the quantity of the unit on the exchange or the
        # density at perticular price points but that's a bit more advanced than what I'm doing rn.

        #record_whole_market(market_response)

        # print('Post Market History Saving time elapsed: ' + str(time.time() - time_to_test_against))

    if data_sourced_from == 'archive':

        all_market_responses = archive_data.copy()

        # Allow the program to continue running using estimated times if the archive doesn't have a timestamp (D'oh!)
        if isinstance(all_market_responses[main_loop], list):
            this_loops_data = all_market_responses[main_loop]
            print('Using posted time')
        elif isinstance(all_market_responses[main_loop], dict):
            this_loops_data = all_market_responses[main_loop]['data']
            archived_time = all_market_responses[main_loop]['time']
            print('using archived time of ' + str(archived_time))
        else:
            "Error archive data type"

        try:
            market_response = this_loops_data

            # time.sleep(1)
        except:
            print("Error, could not use file data")
            print(this_loops_data)
            print("")
            print(main_loop)
            print("")
            print(all_market_responses)
            time.sleep(5)
    # print('After Data fetching ' + str(time.time()- time_to_test_against))

    try:
        # Reads the previous data for this item
        file_name = 'Market for ' + str(db_number) + '.txt'
        with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\MarketResults',
                               file_name), "r") as file1:
            old_data = eval(file1.read())
            file1.close()
    except:
        old_data = []
        print("ERROR File not found, continuing:" + str(file_name))

    # Makes a new dict and adds only the items we care about to it, then adds it to a list.
    # print('Market response: ' + str(market_response))
    for y in market_response:
        # Checks to work out if the listing was cancelled rather than sold.
        # print(y)

        # Writes the data we want to the clean response dict
        clean_response.clear()
        clean_response['id'] = y['id']
        clean_response['quantity'] = y['quantity']
        clean_response['quality'] = y['quality']
        clean_response['price'] = y['price']
        clean_response['posted'] = y['posted']
        clean_response['seller_name'] = y['seller']['company']
        clean_response['seller_is_NPC'] = y['seller']['npc']
        # Using .copy() here stops it from updating all the dict's in the list.
        response.append(clean_response.copy())

    # Compares the 2 sets of data and returns the dicts that have changed.
    list_dicts_difference = []
    list_dicts_overlapping = []
    list_1 = old_data
    list_2 = response

    set_list1 = set(tuple(sorted((d).items())) for d in list_1)
    set_list2 = set(tuple(sorted(d.items())) for d in list_2)

    set_overlapping = set_list1.intersection(set_list2)

    set_difference = set_list1.symmetric_difference(set_list2)

    for tuple_element in set_difference:
        list_dicts_difference.append(dict((x, y) for x, y in tuple_element))
    for tuple_element in set_overlapping:
        list_dicts_overlapping.append(dict((x, y) for x, y in tuple_element))

    id_list = []
    for x in list_dicts_difference:
        id_list.append(x['id'])

    dupes = ([item for item, count in collections.Counter(id_list).items() if count > 1])

    # Returns a list of lists of dicts paired by ID.
    paired_id = {}
    paired_ids = []
    all_pairs = []
    # print('dupes = ' + str(dupes))
    # print("")
    # print(list_dicts_difference)
    # print("")
    for x in dupes:
        count = 0
        paired_ids.clear()
        for y in list_dicts_difference:
            # print('loop = ' + str(count))
            paired_id.clear()
            id = y['id']
            # print('y= ' + str(y))
            # print('y_ID= ' + str(id))
            # print("")

            if x == id:
                paired_id = dict(list_dicts_difference[count].copy())
                # print('Pair Popped = ' + str(paired_id))
                # print("")
                paired_ids.append(paired_id.copy())
                # print('Pairs Popped = ' + str(paired_ids))

            count = count + 1

        # print('paired ids = ' + str(paired_ids))
        all_pairs.append(paired_ids.copy())

    # Make a dict which has all the details of what has been sold, ONLY including where I can see the id in both results.
    for i in all_pairs:
        price = i[0]['price']
        quality = i[0]['quality']
        date_posted = i[0]['posted']
        seller_name = i[0]['seller_name']
        seller_was_NPC = i[0]['seller_is_NPC']
        quantity_1 = i[0]['quantity']
        quantity_2 = i[1]['quantity']

        higher_quantity = max([quantity_1, quantity_2])
        lower_quantity = min([quantity_1, quantity_2])
        products_sold = higher_quantity - lower_quantity

        # Fills our preperation dict with data
        sold_dict['quality'] = quality
        sold_dict['price'] = price
        sold_dict['quantity_sold'] = products_sold
        sold_dict['posted'] = date_posted
        sold_dict['seller_name'] = seller_name
        sold_dict['seller_is_NPC'] = seller_was_NPC
        sold_dict['Listings_sold'] = 1
        sold_list.append(sold_dict.copy())

    partial_sold_list = sold_list.copy()
    # print('Parital sold: ' + str(partial_sold_list))

    # I now need to find all dicts which were in the old data but are not in the new data.
    # print('Moving on from partially sold entires to 100% sold entries')
    # This gives us 2 lists of all the ID's in the old and new data.
    new_ids = []
    old_ids = []
    for x in list_dicts_overlapping:
        new_ids.append(x['id'])
    for x in old_data:
        old_ids.append(x['id'])

    # Filters down to just the ID's that were only in the old set
    only_old_ids = set(old_ids.copy())
    for x in new_ids:
        only_old_ids.discard(x)

    for x in only_old_ids:
        for y in old_data:
            if y['id'] == x:
                price = y['price']
                quality = y['quality']
                quantity = y['quantity']
                date_posted = y['posted']
                seller_name = y['seller_name']
                seller_was_NPC = y['seller_is_NPC']

                sold_dict['quality'] = quality
                sold_dict['price'] = price
                sold_dict['quantity_sold'] = quantity
                sold_dict['posted'] = date_posted
                sold_dict['seller_name'] = seller_name
                sold_dict['seller_is_NPC'] = seller_was_NPC
                sold_dict['Listings_sold'] = 1
                sold_list.append(sold_dict.copy())

    # print('Sold list = ' + str(sold_list))

    def remove_false_sales(sold_list, partial_sold_list):
        # print('Full sold list: ' + str(sold_list))

        output = []

        partial_sold_q0 = []
        partial_sold_q1 = []
        partial_sold_q2 = []
        partial_sold_q3 = []
        partial_sold_q4 = []
        partial_sold_q5 = []
        partial_sold_q6 = []
        partial_sold_q7 = []
        partial_sold_q8 = []
        partial_sold_q9 = []

        # Get us a load of lists with ONLY partial sale prices.
        # The only time there will be more than 1 price in the list is when there is a listing removed
        for x in partial_sold_list:
            if x['quality'] == 0:
                partial_sold_q0.append(x['price'])
            if x['quality'] == 1:
                partial_sold_q1.append(x['price'])
            if x['quality'] == 2:
                partial_sold_q2.append(x['price'])
            if x['quality'] == 3:
                partial_sold_q3.append(x['price'])
            if x['quality'] == 4:
                partial_sold_q4.append(x['price'])
            if x['quality'] == 5:
                partial_sold_q5.append(x['price'])
            if x['quality'] == 6:
                partial_sold_q6.append(x['price'])
            if x['quality'] == 7:
                partial_sold_q7.append(x['price'])
            if x['quality'] == 8:
                partial_sold_q8.append(x['price'])
            if x['quality'] == 9:
                partial_sold_q9.append(x['price'])

        # print('Partial sold prices:')
        # print(partial_sold_q0)
        # print(partial_sold_q1)
        # print(partial_sold_q2)
        # print(partial_sold_q3)
        # print(partial_sold_q4)

        # If the item has been partially or completely sold,but there is a non completely sold item in both
        # market responses of the same Q,then that is an invalid sale as the seller has removed it the market.
        for i in sold_list:
            # print('Listing sold: ' + str(i))

            latest_prices = []

            # This is a slightly dangerous if statement. If we get into a situation where people are buying from
            # the NPC's, we will miss ALL NPC sales. However, this statement skips a whole bunch of checks AND
            # will be regularly used AND in the situation where people are buying from NPC's, there would likely
            # be some NPC's removing their sales like normal, very possibly as they are the lowest price item on
            # the exchange.
            if i['seller_is_NPC'] == True:
                """print('Invalid sale, seller is an NPC: ' + str(i['seller_name']))"""


            else:  # x['seller_is_NPC'] == False: =
                quality = i['quality']
                # We have to use a list here for partial_sold_qx because if an item is removed and then relisted at
                # the same price but in a lower quantity, we will have 2 listings of the same Q which have been
                # partially sold.
                """if quality == 0:
                    partial_sold_len = len(partial_sold_q0)
                if quality == 1:
                    partial_sold_len = len(partial_sold_q1)
                if quality == 2:
                    partial_sold_len = len(partial_sold_q2)
                if quality == 3:
                    partial_sold_len = len(partial_sold_q3)
                if quality == 4:
                    partial_sold_len = len(partial_sold_q4)
                if quality == 5:
                    partial_sold_len = len(partial_sold_q5)
                if quality == 6:
                    partial_sold_len = len(partial_sold_q6)
                if quality == 7:
                    partial_sold_len = len(partial_sold_q7)
                if quality == 8:
                    partial_sold_len = len(partial_sold_q8)
                if quality == 9:
                    partial_sold_len = len(partial_sold_q9)

                #Set the target_sale_price based on the Q
                if partial_sold_len > 0:
                    print('Using partial sold target price')
                    if quality == 0:
                        target_sale_price = min(partial_sold_q0)
                    if quality == 1:
                        target_sale_price = min(partial_sold_q1)
                    if quality == 2:
                        target_sale_price = min(partial_sold_q2)
                    if quality == 3:
                        target_sale_price = min(partial_sold_q3)
                    if quality == 4:
                        target_sale_price = min(partial_sold_q4)
                    if quality == 5:
			target_sale_price = min(partial_sold_q5)
                    if quality == 6:
                        target_sale_price = min(partial_sold_q6)
                    if quality == 7:
                        target_sale_price = min(partial_sold_q7)
                    if quality == 8:
                        target_sale_price = min(partial_sold_q8)
                    if quality == 9:
                        target_sale_price = min(partial_sold_q9)"""  # I am leaving this here as it is a lot of code, but I think it is redundant.

                # If there is only full sales or removals and as such the partial sale price
                # list is empty, we can check the price of the listing we have iterated to against the lowest
                # priced listing of the same Q in the latest market results.
                if 0 == 0:
                    # print('Using overlapping dict list min price')
                    for x in list_dicts_overlapping:
                        if x['quality'] == quality:
                            latest_prices.append(x['price'])

                    # If there are NO common Q listings between the 2, just assume it's valid as we have nothing to compare against.                        if len(latest_prices) > 0:
                    if len(latest_prices) > 0:
                        target_sale_price = min(latest_prices)
                    if len(latest_prices) == 0:
                        target_sale_price = 999999999

                # If this listing has been completely OR partially removed AND has a price larger than the target
                # sale price, it must have been manually removed.
                if i['price'] > target_sale_price:
                    """print('Price more than target: Price = ' + str(i) + ' vs Target = ' + str(target_sale_price))"""
                else:
                    output.append(i)

        return output

    sold_list = remove_false_sales(sold_list, partial_sold_list)

    q0 = []
    q1 = []
    q2 = []
    q3 = []
    q4 = []
    q5 = []
    q6 = []
    q7 = []
    q8 = []
    q9 = []

    # Seperates the sold list into different Q's
    for x in sold_list:
        if x['quality'] == 0:
            q0.append(x)
        if x['quality'] == 1:
            q1.append(x)
        if x['quality'] == 2:
            q2.append(x)
        if x['quality'] == 3:
            q3.append(x)
        if x['quality'] == 4:
            q4.append(x)
        if x['quality'] == 5:
            q5.append(x)
        if x['quality'] == 6:
            q6.append(x)
        if x['quality'] == 7:
            q7.append(x)
        if x['quality'] == 8:
            q8.append(x)
        if x['quality'] == 9:
            q9.append(x)

    # Combines any entires with matching prices
    def combine_matching_prices(list_of_dicts):
        # This function inputs a list of dicts formatted like...
        # [{'quality': 0, 'price': 0.254, 'quantity_sold': 356592}, {'quality': 0, 'price': 0.374, 'quantity_sold': 634}, {'quality': 0, 'price': 0.254, 'quantity_sold': 50000}]
        # Notes especially that 2 of these dicts have the same price. At the output these 2 will be combined into 1 dict.
        # This function is not currently setup to make sure the quality is matching.

        # print('Input =' + str(list_of_dicts))
        prices = []
        output = []

        for x in list_of_dicts:
            prices.append(x['price'])

        # print('prices = ' + str(prices))
        # This gives us a list of unique prices
        unique_prices = prices.copy()
        unique_prices = list(dict.fromkeys(unique_prices))
        # print('unique prices = ' + str(unique_prices))
        # This gives us a dict with each price as key and amount of times in list as value.
        counter = collections.Counter(prices)
        # print('counter = ' + str(counter))

        for x in unique_prices:
            matched_price = []
            quantity = 0
            dates_posted = []
            seller_names = []
            sellers_were_NPC = []
            Listings_sold = 0

            sold_dict.clear()
            # If there is only 1 on the counter, then we can still run it through this code, it will just build a
            # new dict which is identical to itself.
            if counter[x] > 0:
                # We make a list of the dicts where we have a matching price
                for y in list_of_dicts:
                    if x == y['price']:
                        # print('Looking at: ' + str(y))
                        matched_price.append(y)

                # We work out the total sold
                # print(matched_price)
                for z in matched_price:
                    # print(z)
                    try:
                        quantity = quantity + z['quantity']
                    except:
                        quantity = quantity + z['quantity_sold']

                    try:
                        dates_posted.append(z['posted'])
                        sold_dict['posted'] = dates_posted

                        seller_names.append(z['seller_name'])
                        sold_dict['seller_name'] = seller_names

                        sellers_were_NPC.append(z['seller_is_NPC'])
                        sold_dict['seller_is_NPC'] = sellers_were_NPC

                        Listings_sold = Listings_sold + z['Listings_sold']
                        sold_dict['Listings_sold'] = Listings_sold
                    except:
                        print("Unable include old data")

                # Get the non changing values from the matching price dict
                price = matched_price[0]['price']
                quality = matched_price[0]['quality']

                # Build the new dict. Some of this happens above in the 'trys' to compensate for old data without the values in them.
                sold_dict['quality'] = quality  # This data is used later, even  though it's mplied by the file.
                sold_dict['price'] = price
                sold_dict['quantity_sold'] = quantity
                if data_sourced_from == 'live':
                    sold_dict['datetime'] = now
                if data_sourced_from == 'archive':
                    try:
                        sold_dict['datetime'] = archived_time
                    except:
                        sold_dict['datetime'] = matched_price[0]['posted']

                # print('Added to output:' + str(sold_dict))

                output.append(sold_dict.copy())

        # print('Output =' + str(output))
        # print("")
        return output

    # Formats the items that have been sold read for nice and easy writing to file
    condensed_q0 = combine_matching_prices(q0.copy())
    condensed_q1 = combine_matching_prices(q1.copy())
    condensed_q2 = combine_matching_prices(q2.copy())
    condensed_q3 = combine_matching_prices(q3.copy())
    condensed_q4 = combine_matching_prices(q4.copy())
    condensed_q5 = combine_matching_prices(q5.copy())
    condensed_q6 = combine_matching_prices(q6.copy())
    condensed_q7 = combine_matching_prices(q7.copy())
    condensed_q8 = combine_matching_prices(q8.copy())
    condensed_q9 = combine_matching_prices(q9.copy())

    """condensed_q0 = {'quality': 0, 'datetime': now, 'data': combine_matching_prices(q0.copy())}
    condensed_q1 = {'quality': 1, 'datetime': now, 'data': combine_matching_prices(q1.copy())}
    condensed_q2 = {'quality': 2, 'datetime': now, 'data': combine_matching_prices(q2.copy())}
    condensed_q3 = {'quality': 3, 'datetime': now, 'data': combine_matching_prices(q3.copy())}
    condensed_q4 = {'quality': 4, 'datetime': now, 'data': combine_matching_prices(q4.copy())}
    condensed_q5 = {'quality': 5, 'datetime': now, 'data': combine_matching_prices(q5.copy())}
    condensed_q6 = {'quality': 6, 'datetime': now, 'data': combine_matching_prices(q6.copy())}
    condensed_q7 = {'quality': 7, 'datetime': now, 'data': combine_matching_prices(q7.copy())}
    condensed_q8 = {'quality': 8, 'datetime': now, 'data': combine_matching_prices(q8.copy())}
    condensed_q9 = {'quality': 9, 'datetime': now, 'data': combine_matching_prices(q9.copy())}"""

    formatted_sell_list = []
    formatted_sell_list.extend(
        [condensed_q0, condensed_q1, condensed_q2, condensed_q3, condensed_q4, condensed_q5, condensed_q6,
         condensed_q7, condensed_q8, condensed_q9])
    print('Final output')
    for x in range(len(formatted_sell_list)):

        if len(formatted_sell_list[x]) > 0:
            print('Q' + str(x))
            for a in formatted_sell_list[x]:
                print(a)

    print("")

    # Writes every Q to it's own file
    loop = 0
    #print(formatted_sell_list)
    for x in formatted_sell_list:
        # print('loop = ' + str(loop))
        content = x.copy()
        file_name = str(db_number) + '- Q' + str(loop)
        # print('Writing to ' + str(db_file_name) + ", " + str(content))

        if len(x) > 0:

            # Open the file in append & read mode ('a+')
            with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales',
                                   str(file_name)) + '.txt', "a+") as file_object:
                for x in content:
                    file_object.write('\n')
                    file_object.write(str(x))

                file_object.close()




    # Writes the latest api response to file.
    content = response

    with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\MarketResults',
                               'Market for ' + str(db_number)) + '.txt', "w") as file_object:

        file_object.write(str(response))
        file1.close()
    #print("End of " + str(numbers_dict[db_number]) + ' (' + str(db_number) + '). It took ' +str(time.time() - time_to_test_against2) + ' seconds')
    #print("")




data_source = 'live'  # Option are 'archive OR 'live'
db_num = 1  # Only used in the case that we are in archive mode.
print('Mode is ' + str(data_source))

if data_source == 'live':
    file_name = 'db_numbers_that_can_be_sold'
    with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files',
                           str(file_name)) + '.txt', "r") as file1:
        db_numbers_that_can_be_sold = eval(file1.read())

else:
    db_numbers_that_can_be_sold = [db_num]


file_name = 'numbers_dict'
with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files',
                        str(file_name)) + '.txt', "r") as file1:
    numbers_dict = eval(file1.read())
    file1.close()

# loops = 1000 # NO LONGER NEEDED AS LIVE IS CALLED VIA CRONJOB This is, roughly, how many mins to run for. In reality it will be about 6% more than this.

if data_source == 'live':
    print('Start of Market data recording at: ' + str(time.time()))
    time_to_test_against = time.time()
    timings_list = [[], [], [],[],[]]
    hits_this_loop = 0
    times_list = []
    for x in db_numbers_that_can_be_sold:
        time_differential = (time.time() - x['last_run'])


        if time_differential > x['pause_interval']:
            #print(str(numbers_dict[x['id']]) + ' hit, waited for ' + str(int(time_differential)) + ' seconds')
            update_latest_market(x['id'], data_source,'', '')
            x['last_run'] = time.time()
            hits_this_loop = hits_this_loop + 1


        else:
            """print(str(x['id']) + ' still waiting, so far waited for ' + str(int(time_differential)) + ' seconds')"""

    #print(times_list)

    file_name = 'db_numbers_that_can_be_sold'
    with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', str(file_name)) + '.txt',
              "w") as file1:
        file1.write(str(db_numbers_that_can_be_sold))
        file1.close()

    total_time = time.time()-time_to_test_against

    print('Total time taken was: ' + str(total_time) + ' for ' + str(hits_this_loop) + ' products')
    times_report = []
    for x in timings_list:
        try:
            times_report.append(sum(x.copy()) / len(x.copy()))
        except ZeroDivisionError:
            a6jheda = 'cdsfdggb'
    #print('Timings report: ' + str(times_report))
    print("")


if data_source == 'archive':
    file_name = 'All Market Responses for ' + str(db_numbers_that_can_be_sold[0])
    try:
        with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\MarketResults',
                               str(file_name)) + '.txt', "r") as file1:
            all_market_responses = eval(file1.read())
            file1.close()
            loops = len(all_market_responses)
            # print('File found')

    except:
        print('Error no file to read: ' + str(file_name) + '.txt')

    print('Hold on tight! We are going around the roundabout ' + str(
        loops) + ' times! (this is how many loops will happen)')

    for x in range(loops):
        print('loop ' + str(x + 1))
        update_latest_market(db_numbers_that_can_be_sold, data_source, x,all_market_responses)




