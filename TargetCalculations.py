import os
import datetime
import numpy as np
import pandas as pd
import math

#Shout at this to get all the targets to update.
def calculate_targets():

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

    for db_number in  db_numbers_that_can_be_sold:
        #print(db_number)
        all_data = []
        for x in range(9):
            file_name = str(db_number['id']) + '- Q' + str(x) + '.txt'

            try:
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales', file_name),
                          "r") as file1:
                    data = eval(file1.read())
                    file1.close()
                    all_data = all_data + [data]
            except FileNotFoundError:
                data = []

        # print(all_data)
        output_list = []
        #print('here')

        for Q in range(len(all_data)):
            quality = all_data[Q][0]['quality']
            temp_prices = []
            temp_quantity = []
            for a in all_data[Q]:
                temp_prices.append(a['price'])
                temp_quantity.append(a['quantity_sold'])

            # These need to be assigned to each Q!
            percentile95 = list_weighted_quartile_hunter(temp_prices, temp_quantity, 95)
            percentile5 = list_weighted_quartile_hunter(temp_prices, temp_quantity, 5)
            percentile50 = list_weighted_quartile_hunter(temp_prices, temp_quantity, 50)
            #print(percentile95,percentile50,percentile5)
            output = {}
            output['quality'] = quality
            output['best_sell_price'] = percentile95
            output['best_market_buy_price'] = percentile5
            output['average_market_price'] = percentile50
            output_list.append(output)

        #print(output_list)

        file_name = str(db_number['id']) + '.txt'
        with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\TargetCalulations', file_name),
                    "w") as file1:
            file1.write(str(output_list))


        # print(all_data)



            # Value is currently equal to each price multiplied by it's quantity. By dividing by total quantity,
            # we can find a weighted average price. What I want however is a top and bottom n% value, rounded to the
            # nearest number seen in the price list. These will give us our target buy and sale price. The firs tto
            # calculate is the target sale price, the target buy price is the calculated from that.


def dict_weighted_quartile_hunter(dict1, targetquart):
    keys = list(dict1.keys())
    values = list(dict1.values())
    total_sold = sum(values)
    subtotal = total_sold
    keys_sorted = keys.copy()
    keys_sorted.sort(reverse=True)
    target = (targetquart / 100) * total_sold
    for x in keys_sorted:
        this_value = dict1.get(x)
        subtotal = subtotal - this_value
        if target >= subtotal:
            quartile_price = x
            break
    return quartile_price


def list_weighted_quartile_hunter(prices, weights, targetquart):
    keys = prices
    values = weights
    total_sold = sum(values)
    subtotal = total_sold
    keys_sorted = keys.copy()
    keys_sorted.sort(reverse=True)
    target = (targetquart / 100) * total_sold
    #print(keys)
    #print(values)
    #print(keys_sorted)
    #print('Target:' + str(target))
    for x in keys_sorted:
        #print('Price = ' + str(x))
        #print(keys.index(x))
        this_value = weights[keys.index(x)]
        #print('Sold at this price = ' + str(this_value))
        subtotal = subtotal - this_value
        #print('Subtotal = ' + str(subtotal))
        if target >= subtotal:
            quartile_price = x
            break
        else:
            quartile_price = min(keys)
    #print(quartile_price)
    return quartile_price


def VWAP_calculations(timestamps,prices,quantity):
    #print("")
    #print('Timestamps: ' + str(timestamps))
    #print('prices: ' + str(prices))
    #print('quantity: ' + str(quantity))
    num_of_recorded_sales = len(timestamps)
    time_length = (max(timestamps) - min(timestamps))
    mins_recorded = time_length.total_seconds() / 60
    num_of_new_datapoints = num_of_recorded_sales / 50 # 1 new datapoint for every 10 original
    #print('We have ' + str(num_of_new_datapoints) + ' datapoints over ' +str(mins_recorded) + ' mins.')
    frequency = round(mins_recorded / num_of_new_datapoints)
    if frequency == 0:
        frequency = 1
        # It is possible for the result of frequency to be 0. This causes issues. A solution is to make all results of 0 into 1.
    #print('Frequency: ' + str(frequency))



    df = pd.DataFrame(
        dict(Dates=timestamps, P=prices, Q= quantity))

    #print(df.index.dtype)
    df = df.set_index(pd.DatetimeIndex(df['Dates']))


    df = df.drop(['Dates'], axis=1)
    #print(df.head())
    #print(df.index.dtype)

    def vwap(data):
        try:
            price = data.P
            quantity = data.Q
            top = sum(price * quantity)
            bottom = sum(quantity)
            return top / bottom
        except ZeroDivisionError:
            return np.nan
    #   return (data.P * data.Q).sum() / data.Q.sum()


    df2 = df.groupby(pd.Grouper(freq=str(frequency) + 'min')).apply(vwap).reset_index(name="vwap")
    #print(df2)
    return df2


#calculate_targets()