import os
import datetime

cash_to_invest = 6000000

file_name = 'numbers_dict'
with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files',
                       str(file_name)) + '.txt', "r") as file1:
    number_name_dict = eval(file1.read())
    file1.close()

file_name = 'All profits.txt'
with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', file_name),
          "r") as file1:
    profits = eval(file1.read())
    file1.close()

file_name = 'db_numbers_that_cannot_be_sold'
with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', str(file_name)) + '.txt', "r") as file1:
    db_numbers_that_cannot_be_sold = eval(file1.read())
    file1.close()

print('Begin filtering')
latest_product = 'blank'
#print(number_name_dict)

filtered_profits = []
for x in profits:

    if number_name_dict[x[0]] != latest_product:

        print(number_name_dict[x[0]])
    latest_product = number_name_dict[x[0]]
    #print(x)
    if x[3][0][2] > 0:
        #print('Profits Targets: ' + str())
        try:
            if x[3][1][0]['Investment'] < cash_to_invest:
                #print(x[3][1][0])
                try:
                    #print(number_name_dict[x[0]])
                    # We attempt to check the amount of sales on the exchange. If we can't, it's certain that this is
                    # because the product isn't sold on the exchange and hence it doesn't matter if the exchange cannot
                    # hit this target.
                    file_name = str(x[0]) + '- Q' + str(x[1]) + '.txt'
                    with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales', file_name),
                              "r") as file1:
                        recorded_sales = eval(file1.read())
                        file1.close()
                    volume_total = 0
                    for a in recorded_sales:
                        volume_total = volume_total + a['quantity_sold']
                    estimated_price = recorded_sales[0]['price']
                    total_value_goods_sold = estimated_price * volume_total
                    if (total_value_goods_sold / 8) > x[3][0][2]: # Divided by the number of days that data capture has been happening for.
                        #print('Added ' + str())
                        filtered_profits.append(x)
                except:
                    filtered_profits.append(x)
            else:
                # Everything in this else is used to decrease the Profit and investment costs until they are at an
                # acceptable level. It's not done in the most accurate or the most efficent way but it's good enough.
                # It's worth noting that the expected profit for something that has been popped will actually be
                # higher than listed as admin fees will still be at the highest leve.
                position = profits.index(x)
                profits.pop(position)
                #print('Popped: ' + str(x))
                old_profits = [x[3][0][0], x[3][0][1], x[3][0][2]]
                old_investment = x[3][1][0]['Investment']

                division_level = old_investment / cash_to_invest

                old_profits0 = old_profits[0]
                old_profits1 = old_profits[1]
                old_profits2 = old_profits[2]

                new_profits0 = old_profits0 / division_level
                new_profits1 = old_profits1 / division_level
                new_profits2 = old_profits2 / division_level

                new_profits = [new_profits0,new_profits1,new_profits2]
                #print(new_profits)

                new_investment = old_investment / division_level


                x[3][0] = new_profits
                x[3][1][0]['Investment'] = new_investment

                profits.append(x)



        except KeyError:
            print('Could make a profit here but not enough slots')
#print(filtered_profits)

print('Done filtering')

def sortingorder(x):
    return x[3][0][2]

filtered_profits.sort(reverse=True,key=sortingorder)

#print(filtered_profits)

#Prints the top 20 results
for x in filtered_profits[:20]:
    print(str(number_name_dict[x[0]]) + ' at Q' + str(x[1]) + ', estimated daily profit is: $' + str(int(x[3][0][2])) + '. Up to ' +str(sum(x[3][1][1][0]['Levels'])) + ' building levels.')

print("")
for x in filtered_profits[:20]:
    print(x)
print("")



profits = []
all_names = []
all_qualities = []
all_steps = []
all_maxprofits = []
all_minprofits = []
all_avgprofits = []
all_investments = []
all_IDs = []
for x in filtered_profits:
    new_dict = {}
    new_dict['name'] =  number_name_dict[x[0]]
    new_dict['quality'] = x[1]
    new_dict['steps'] = x[2]
    new_dict['maxprofit'] = x[3][0][0]
    new_dict['minprofit'] = x[3][0][1]
    new_dict['avgprofit'] = x[3][0][2]
    new_dict['Investment'] = x[3][1][0]['Investment']
    #new_dict['Buildings'] = x[3][1][1]
    profits.append(new_dict)

    all_names.append(number_name_dict[x[0]])
    all_qualities.append(x[1])
    all_steps.append(x[2])
    all_maxprofits.append(x[3][0][0]-x[3][0][2])
    all_minprofits.append(x[3][0][2]-x[3][0][1])
    all_avgprofits.append(int(x[3][0][2]))
    all_investments.append(x[3][1][0]['Investment'])
    all_IDs.append(str(number_name_dict[x[0]]) +', Q:' + str(x[1]) + ', ' + str(x[2])+ ' steps')


#print(all_names)
#print("")
#print(all_avgprofits)



import plotly.graph_objects as go

fig = go.Figure([go.Bar(x=all_IDs,
                        y=all_avgprofits,
                        
                        error_y=dict(
                                    type='data',
                                    symmetric=False,
                                    array=all_maxprofits,
                                    arrayminus=all_minprofits)
                        )
])
#fig.write_html('Profits' + '.html', auto_open=True)
fig.write_html(r'C:\Users\PC\PycharmProjects\SimCompanies\Files\Profits'+ '.html', auto_open=True)