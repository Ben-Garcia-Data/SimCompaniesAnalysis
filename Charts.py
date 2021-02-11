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

datapoints_dict_list = []


# This is a rounding calculation used later
def round_sig(x, sig=2):
    import math
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)


def build_chart(db_number, chart_type, autoopen, qualities=range(9), position_column=1, position_row=1):
    # chart_type: Options are 'hloc', 'scatter' or 'scatter3d' or 'line'
    #print('Chart type is ' + str(chart_type) + ' for: ' + str(number_name_dict[db_number]))

    import plotly.graph_objects as go
    from TargetCalculations import list_weighted_quartile_hunter, VWAP_calculations
    import numpy as np

    import datetime
    import os
    import pandas as pd
    import math

    if chart_type == 'hloc':
        qualities = range(1)

    #print('Pre setup Qualities: ' + str(qualities))

    original_db_number = db_number
    #print('Original DB Number: ' + str(original_db_number))


    def Setup_for_Charts(db_number, Setup_for_Charts_qualities):

        # BEGIN the simple numpy dataframe building.
        #print('Seting up for: ' + str(db_number))
        all_data = []
        db_name = number_name_dict[db_number]
        save_location = r"C:\\Users\\PC\\PycharmProjects\\Simcompanies\\Files\\Charts\\" + chart_type + '\\'
        host_name = str(db_name) +'-' + str(chart_type)
        #print(save_location)

        quality_loops = Setup_for_Charts_qualities

        #print("Setup charts Q's: " + str(quality_loops))

        now = datetime.datetime.utcnow()
        #print('Quality loops:' + str(quality_loops))
        for x in quality_loops:
            file_name = str(db_number) + '- Q' + str(x) + '.txt'
            #print(file_name)

            try:
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\RecordedSales', file_name),
                          "r") as file1:
                    data = file1.readlines()
                    file1.close()
                    #print('DATA: ' + str(data))
                    #print("")


                    all_data = all_data + [data]
            except FileNotFoundError:
                data = []
                #print(str(file_name) + ' not found')



        #print('All data: ' + str(all_data))
        all_dates = []
        all_prices = []
        all_quantity = []
        all_quality = []
        time_to_sell_list = []
        all_text = []
        all_colors = []

        which_qualities = []
        datapoints = 0

        special_list = []
        failurecount = 0
        #print('length of all data: ' + str(all_data))
        def Check_if_error():
            if isinstance(all_data[Q][0], int):
                Remove_if_error()

        def Remove_if_error():
            all_data[Q].remove(Q[0])
            Check_if_error()
        for Q in range(len(all_data)):
            #print('Q Loop: ' + str(Q))

            try:
                if isinstance(all_data[Q][0], str):
                    all_data[Q][0] = eval(all_data[Q][0])
            except:
                print('Error sanitizing data:')
                print(str(all_data[Q][0]))

            #Check_if_error()


            quality = all_data[Q][0]['quality']
            # print(quality)
            which_qualities.append(quality)
            temp_prices = []
            temp_quantity = []
            temp_timestamps = []
            for a in all_data[Q]:
                try:
                    if isinstance(a,str):
                        #print('hi')
                        a = eval(a)
                except:
                    continue
                all_dates.append(a['datetime'])
                all_prices.append(a['price'])
                temp_prices.append(a['price'])
                temp_quantity.append(a['quantity_sold'])
                temp_timestamps.append(a['datetime'])
                all_quantity.append(a['quantity_sold'])
                if chart_type == 'scatter':
                    all_quality.append(str(a['quality']))
                elif chart_type == 'scatter3d':
                    all_quality.append(str(a['quality']))
                else:
                    all_quality.append(a['quality'])

                # This segment is currently unused.
                if quality == 0:
                    all_colors.append('#876A8A')
                elif quality == 1:
                    all_colors.append('#6E3935')
                elif quality == 2:
                    all_colors.append('#D8973C')
                elif quality == 3:
                    all_colors.append('#H1994C')
                elif quality == 4:
                    all_colors.append('#8FFF5C')
                elif quality == 5:
                    all_colors.append('#8DFFCD')
                elif quality == 6:
                    all_colors.append('#5CCEFF')
                elif quality == 7:
                    all_colors.append('#1D4E89')
                elif quality == 8:
                    all_colors.append('#735CDD')
                elif quality == 9:
                    all_colors.append('#991D1D')

                # all_quality.append(str(a['quality'])) This was replaced by the line below to enable VWAP calcs. If this
                # breaks something else, probably easier to change the VWAP checks to be == '0' instead of == 0.

                posted = datetime.datetime.strptime(a['posted'][0], '%Y-%m-%dT%H:%M:%S.%f+00:00')
                time_to_sell = a['datetime'] - posted
                datapoints = datapoints + 1
                # print(time_to_sell)
                time_to_sell_list.append(time_to_sell.total_seconds() / 2400)
                try:
                    text_to_add = ', Seller(s): ' + str(a['seller_name']) + ', Listings: ' + str(
                        a['Listings_sold'])
                except KeyError:
                    text_to_add = 'No name recorded'
                all_text.append(text_to_add)

            # print('VWAP: ' + str(VWAP))
            # print('VWAP dates: ' + str(vwap_dates))

            try:
                file_name = str(db_number) + '.txt'
                with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\Encyclopedia', file_name),
                          "r") as file1:
                    encyclopedia_info = eval(file1.read())
                    file1.close()
            except FileNotFoundError:
                print('File not found for: ' + str(number_name_dict[db_number]))

            transport_quantity = encyclopedia_info['transportation']
            transport_price = 0.35

            transport_cost = transport_price * transport_quantity

            from math import log10, floor

            def round_to_n(x, sig=3):
                return round(x, sig - int(floor(log10(abs(x)))) - 1)

            # Begin the calculation of special values (basically anything that might be called an indicator)

            percentile95 = list_weighted_quartile_hunter(temp_prices, temp_quantity, 95)
            df_vwap = VWAP_calculations(temp_timestamps, temp_prices, temp_quantity)
            VWAP = list(df_vwap['vwap'])
            vwap_dates = list(df_vwap['Dates'])
            # print(vwap_dates)
            # print(VWAP)

            special_dict = {}

            special_dict['Quality'] = quality
            special_dict['price_target'] = round_to_n((percentile95 * 0.97) - transport_cost)
            special_dict['VWAP'] = VWAP
            special_dict['vwap_dates'] = vwap_dates
            special_list.append(special_dict)
            # print('Special dict: ' + str(special_dict))

        if len(all_dates) == 0:
            raise ArithmeticError
        #print('All dates: ' + str(all_dates))
        sorted_prices = sorted(all_prices)
        # Used for general horizontal lines
        first_timestamp = min(all_dates)
        mid_timestamp = all_dates[0]
        last_timestamp = max(all_dates)

        df1 = pd.DataFrame(
            dict(Date=all_dates, Price=all_prices, Quantity=all_quantity, Quality=all_quality,
                 Waittime=time_to_sell_list,
                 Text=all_text, color=all_colors))
        # End building the Numpy Dataframe

        # print(df1)

        # Different market states: Recession, Normal, Boom

        market_state_colours = []
        market_states = []
        market_dates = []

        file_name = 'market_states.txt'
        with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', file_name),
                  "r") as file1:
            market_info = eval(file1.read())
            file1.close()

        #print('Market info: ' + str(market_info))

        for x in market_info:
            market_dates.append(x['Start_Date'])
            try:
                market_states.append(x['state'])
            except KeyError:
                """print('Reached the end of the market states')"""

        for x in market_states:
            if x == 'Recession':
                market_state_colours.append("#9bffe9")  # Turquoise
            elif x == 'Normal':
                market_state_colours.append('#c6d5ff')  # Light blue
            elif x == 'Boom':
                market_state_colours.append('#6b93ff')  # Darker blue
            else:
                market_state_colours.append('#000000')  # Black (Error)

        #print('Finished the setup. Qualities is now: ' + str())

        return db_name, save_location, all_quality, host_name, datapoints, which_qualities, first_timestamp, mid_timestamp, last_timestamp, all_quantity, df1, all_data, special_list, all_dates, market_states, market_dates, market_state_colours, all_prices, sorted_prices, original_db_number

    db_name, save_location, all_quality, host_name, datapoints, which_qualities, first_timestamp, mid_timestamp, last_timestamp, all_quantity, df1, all_data, special_list, all_dates, market_states, market_dates, market_state_colours, all_prices, sorted_prices, original_db_number = Setup_for_Charts(
        db_number, qualities)

    def Build_1_chart(db_number, db_name, save_location, all_quality, host_name, datapoints, which_qualities, chart_type,
                      first_timestamp, mid_timestamp, last_timestamp, all_quantity, df1, all_data, special_list,
                      all_dates, market_states, market_dates, market_state_colours, all_prices, sorted_prices, original_db_number):

        import plotly.graph_objects as go
        import plotly.express as px
        import datetime
        import os

        #print('Begining to build a chart')

        def Add_Market_States(market_states, market_dates, market_state_colours,positions=[99,99]):
            states_list = []
            for x in range(len(market_states)):
                #print('Between ' + str(market_dates[x])+ ' and ' + str(market_dates[x+ 1]) + ' is ' + str(market_states[x]) + ', coloured as '  + str(market_state_colours[x]))
                states_list.append(
                    dict(
                        type="rect",
                        xref="x",
                        yref="paper",
                        x0=market_dates[x],
                        y0=0,
                        x1=market_dates[x + 1],
                        y1=1,
                        fillcolor=market_state_colours[x],
                        opacity=0.5,
                        layer="below",
                        line_width=0,
                    ))

            fig.update_layout(
                shapes=states_list)

            # market_switch_times = ["2020-09-07 01:00, 2020-09-11 15:00"]

        def Add_Price_Targets(all_data, special_list, all_dates,show_legend,positions=[99,99]):
            import pandas as pd
            for Q in range(len(all_data)):

                if isinstance(all_data[Q][0], str):
                    all_data[Q][0] = eval(all_data[Q][0])

                quality = all_data[Q][0]['quality']
                # print('For Q' + str(quality))

                indicators = special_list[Q]
                # print(special_list)
                # print("")
                VWAP = indicators['VWAP']
                price_target = indicators['price_target']
                vwap_dates = indicators['vwap_dates']
                quality2 = indicators['Quality']
                # print('Fake quality: ' + str(quality2))

                if quality != quality2:
                    print('HASHAGFHSAHGIOSDBKGOES')

                df4 = pd.DataFrame(
                    dict(Date=vwap_dates, Price=VWAP))

                df3 = pd.DataFrame(
                    dict(Date=all_dates, Price=price_target))

                # print(df3.dtypes)
                # print(type(df3))
                # print(df1.dtypes)
                # print(type(df1))

                # Adds a Master Lines layer so we can enable and disable all the lines as one

                """fig.add_trace(go.Scatter(
                    x=df3['Date'],
                    y=df3['Price'],
                    name='Q' + str(quality) + ' BUY',
                    legendgroup='Lines',
                    showlegend=False

                ))"""
                position_row = positions[1]
                position_column = positions[0]
                #print(str(position_row) + ', ' + str(position_column))
                if position_column != 99:
                    if all_data[0][0]['quality'] == quality:
                        fig.add_trace(go.Scatter(
                            x=df4['Date'],
                            y=df4['Price'],
                            name='Q' + str(quality) + ' VWAP',
                            legendgroup='Lines',
                            showlegend=show_legend

                        ),row=position_row,col=position_column)
                    else:
                        fig.add_trace(go.Scatter(
                            x=df4['Date'],
                            y=df4['Price'],
                            name='Q' + str(quality) + ' VWAP',
                            legendgroup='Lines',
                            showlegend=show_legend

                        ),row=position_row,col=position_column)
                else:
                    if all_data[0][0]['quality'] == quality:
                        fig.add_trace(go.Scatter(
                            x=df4['Date'],
                            y=df4['Price'],
                            name='Q' + str(quality) + ' VWAP',
                            legendgroup='Lines',
                            showlegend=show_legend

                        ))
                    else:
                        fig.add_trace(go.Scatter(
                            x=df4['Date'],
                            y=df4['Price'],
                            name='Q' + str(quality) + ' VWAP',
                            legendgroup='Lines',
                            showlegend=show_legend

                        ))

        def Add_3D_Price_Targets(all_data, special_list, first_timestamp, mid_timestamp, last_timestamp):
            #print('Indicators list length: ' + str(len(special_list)))
            #print('All data length: ' + str(len(all_data)))
            for Q in range(len(all_data)):
                #print('Q Loop: ' + str(Q))
                try:
                    if isinstance(all_data[Q][0], str):
                        all_data[Q][0] = eval(all_data[Q][0])
                except SyntaxError:
                    print('Syntax Error on the end of the file. New lines not appending correctly')
                    continue
                quality = all_data[Q][0]['quality']
                #print('Quality: ' +str(quality))
                #print('special_list: ' + str(special_list))
                indicators = special_list[Q]
                VWAP = indicators['VWAP']
                price_target = indicators['price_target']
                vwap_dates = indicators['vwap_dates']
                quality2 = indicators['Quality']

                fig.add_trace(go.Scatter3d(
                    x=[first_timestamp, mid_timestamp, last_timestamp],
                    z=[price_target, price_target, price_target],
                    y=[quality, quality, quality],
                    mode="lines",
                    name="Q" + str(Q) + " buy trigger: $" + str(round_sig(price_target, 4)),
                    line=dict(width=4),
                ))

        def Setup_Y_Axis(all_prices, sorted_prices,positions=[99,99]):
            length = len(all_prices)
            #print('Setup of Y axis: ' + str(db_name))
            # print('Sorted prices: ' + str(sorted_prices))
            # print('Length: ' + str(length))
            # print(round(length*0.99))
            #print(sorted_prices[0])
            upper_limit = sorted_prices[math.floor(length * 0.99)] + sorted_prices[0] * 0.01
            lower_limit = sorted_prices[math.ceil(length * 0.01)] - sorted_prices[0] * 0.01
            #print(upper_limit,lower_limit)

            position_row = positions[1]
            position_column = positions[0]
            # print(str(position_row) + ', ' + str(position_column))
            if position_column != 99:

                fig.update_layout(
                    yaxis=dict(range=[lower_limit, upper_limit]))
            else:
                fig.update_layout(
                    yaxis=dict(range=[lower_limit, upper_limit]))


        if chart_type == 'scatter':

            fig = px.scatter(df1,
                             x='Date',
                             y='Price',
                             color='Quality',
                             opacity=0.3,
                             size='Quantity',
                             size_max=70,
                             text='Text',
                             # legendgroup=df1['Quality']
                             )
            # Set options common to all traces with fig.update_traces
            fig.update_traces(mode='markers', marker_line_width=2)

            Add_Price_Targets(all_data, special_list, all_dates, True)

            Add_Market_States(market_states, market_dates, market_state_colours)

            Setup_Y_Axis(all_prices, sorted_prices)

            fig.update_layout(title='Price History for ' + str(db_name) + ' (' + str(db_number) + ')',
                              xaxis_title="Time",
                              yaxis_title="Price",
                              yaxis_zeroline=False, xaxis_zeroline=False,

                              legend=dict(
                                  font_size=15,
                                  yanchor='middle',
                                  xanchor='right')
                              )
            fig.write_html(save_location + str(host_name) + '.html', auto_open=autoopen)

        if chart_type == 'scatter3d':
            import plotly.express as px
            import pandas as pd
            import os
            import datetime

            # print(y_list)
            # print(color_list)

            # print(df1)
            fig = px.scatter_3d(df1, x='Date', y='Quality', z='Price', color='Quality', size='Quantity', size_max=100,
                                opacity=0.7)

            Add_3D_Price_Targets(all_data, special_list, first_timestamp, mid_timestamp, last_timestamp)
            # Setup_Y_Axis()

            fig.update_layout(title=db_name, legend=dict(
                font_size=15,
                yanchor='middle',
                xanchor='right'))
            # fig.add_traces(go.Surface(x=x_list, y=quality_list, z=y_list, name='pred_surface'))
            fig.write_html(save_location + str(host_name) + '.html', auto_open=autoopen)

        if chart_type == 'hloc':
            import plotly.express as px
            import pandas as pd
            import os
            import plotly.graph_objects as go
            import datetime as dt

            # def convert_DF_to_OHLC # Maybe add this later?

            df2 = pd.DataFrame(
                dict(Time=all_dates, Symbol=str('Power'), Price=all_prices, Volume=all_quantity, Quality=all_quality)
            )

            df2['Time'] = pd.to_datetime(df2['Time'])

            df2 = df2.set_index(pd.DatetimeIndex(df2['Time']))

            num_of_recorded_sales = len(all_dates)
            time_length = (max(all_dates) - min(all_dates))
            mins_recorded = time_length.total_seconds() / 60
            num_of_new_datapoints = num_of_recorded_sales / 12  # 1 new datapoint for every 10 original
            # print('We have ' + str(num_of_new_datapoints) + ' datapoints over ' +str(mins_recorded) + ' mins.')
            frequency = round(mins_recorded / num_of_new_datapoints)

            df3 = df2['Price'].resample(str(frequency) + 'Min').ohlc()

            fig = go.Figure(data=go.Ohlc(x=df3.index,
                                         open=df3['open'],
                                         high=df3['high'],
                                         low=df3['low'],
                                         close=df3['close']))

            Setup_Y_Axis(all_prices, sorted_prices)
            Add_Market_States(market_states, market_dates, market_state_colours)

            # fig.update(layout_xaxis_rangeslider_visible=False)
            fig.write_html(save_location + str(host_name) + '.html', auto_open=autoopen)

        if chart_type == 'line':
            df = pd.DataFrame(
                dict(Time=all_dates, Prices=all_prices, Quantity=all_quantity, Quality=all_quality)
            )

            fig = go.Figure()

            Add_Price_Targets(all_data, special_list, all_dates, True)

            Add_Market_States(market_states, market_dates, market_state_colours)

            Setup_Y_Axis(all_prices, sorted_prices)

            fig.update_layout(title='Price History for ' + str(db_name) + ' (' + str(db_number) + ')',
                              xaxis_title="Time",
                              yaxis_title="Price",
                              yaxis_zeroline=False, xaxis_zeroline=False,

                              legend=dict(
                                  font_size=15,
                                  yanchor='middle',
                                  xanchor='right')
                              )

        if chart_type == 'overview':
            from plotly.subplots import make_subplots
            import plotly.graph_objects as go
            if len(qualities) > 1:
                print("We are entering more that 1 quality for the overview. While this does work, it probably won't look the best.")
            # This will be a page where we have 1 main item and all the ingredients, plus some pi charts that show how
            # much each ingredient contributes to the overall price and a few handy cute looking graphics that display
            # profit or something.
            #
            #       Title like Overview for Chemicals(17)
            #
            #   Ingredient 1 Q(n-1) VWAP chart
            #   Ingredient 2 Q(n-1) VWAP chart
            #   Ingredient 3 Q(n-1) VWAP chart
            #   Ingredient 4 Q(n-1) VWAP chart
            #   Ingredient 5 Q(n-1) VWAP chart
            #
            #

            # Get a list of ingredients and their quantities
            file_name = db_number
            with open(
                    os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files\Encyclopedia',
                                 str(file_name)) + '.txt',
                    "r") as file1:
                encyclopedia_data = eval(file1.read())
                file1.close()

            ingredients_db_list = []
            ingredients_quantity_list = []
            db_numbers_that_can_be_sold_ID_ONLY = []
            for x in db_numbers_that_can_be_sold:
                db_numbers_that_can_be_sold_ID_ONLY.append(x['id'])
            #print('Can be sold: ' + str(db_numbers_that_can_be_sold_ID_ONLY))
            for x in encyclopedia_data['producedFrom']:
                #print('Produced from: ' + str(x))
                if x['resource']['db_letter'] in db_numbers_that_can_be_sold_ID_ONLY:
                    #print('Added this to the ingredients list')
                    # Only adds to the ingredients list if we can actually source it from the exchange
                    ingredients_db_list.append(x['resource']['db_letter'])
                    ingredients_quantity_list.append(x['amount'])
            #print(ingredients_db_list)
            #print(ingredients_quantity_list)
            first_column = []
            subplot_titles = []
            for i in range(len(ingredients_db_list)):
                first_column.append({})
                subplot_titles.append(str(number_name_dict[ingredients_db_list[i]]))
            subplot_titles.insert(1,db_name)

            specs = []
            columns = 4
            ingredient_specs = []
            num_of_ingredients = len(ingredients_db_list)

            #To avoid a crash for Power bcus it has no ingredients, meaning we have no rows, which leaves no space for the power chart.
            if num_of_ingredients == 0:
                num_of_ingredients = 1
            num_of_ingredients = range(num_of_ingredients)

            #print(num_of_ingredients)
            #print(len(num_of_ingredients))

            for i in num_of_ingredients:
                if i == 0:
                    specs.append([{}, {"rowspan": len(num_of_ingredients), "colspan": 2}, None, None])
                    #Adds the first row of the ingredients, this is a bit different bcus the 'main' chart is here.
                else:
                    specs.append([{}, None, None, None])
                    #Row by roww adds the other charts. Column 1 and 2 need to be left as none so that the main chart can fit there.

            #print(specs)

            fig = make_subplots(
                rows=len(num_of_ingredients), cols=columns,
                specs=specs,
                subplot_titles=(subplot_titles),
                #print_grid = True
            )

            ingredient_qualities = []
            for x in qualities:
                ingredient_qualities.append(x-1)

            #print('Ingredient qualitites: ' + str(ingredient_qualities))

            for db_number in ingredients_db_list:
                #print('Db number ' + str(db_number))
                db_name, save_location, all_quality, host_name, datapoints, which_qualities, first_timestamp, mid_timestamp, last_timestamp, all_quantity, df1, all_data, special_list, all_dates, market_states, market_dates, market_state_colours, all_prices, sorted_prices, original_db_number = Setup_for_Charts(
                    db_number,ingredient_qualities)
                positions = []
                position_column = 1
                position_row = ingredients_db_list.index(db_number) + 1
                positions.append(position_column)
                positions.append(position_row)
                #print('Pre insert positions: ' + str(positions))

                Add_Price_Targets(all_data, special_list, all_dates, False, positions=positions)

                Add_Market_States(market_states, market_dates, market_state_colours,positions=positions)


                Setup_Y_Axis(all_prices, sorted_prices,positions=positions)

                #Not needed bcus we only ever have 1 Q             <<< No longer true, now using all Q's in overview
                # so it auto bounds the range to something sensible.

            #print('Original DB Number: ' + str(original_db_number))
            db_number = original_db_number

            db_name, save_location, all_quality, host_name, datapoints, which_qualities, first_timestamp, mid_timestamp, last_timestamp, all_quantity, df1, all_data, special_list, all_dates, market_states, market_dates, market_state_colours, all_prices, sorted_prices, original_db_number = Setup_for_Charts(
                db_number,qualities)

            positions = []
            position_column = 2
            position_row = 1
            positions.append(position_column)
            positions.append(position_row)
            # print('Pre insert positions: ' + str(positions))

            Add_Price_Targets(all_data, special_list, all_dates, False, positions=positions)

            Add_Market_States(market_states, market_dates, market_state_colours, positions=positions)



            fig.write_html(save_location + str(host_name) + '.html', auto_open=autoopen)
        # Next up, I need to export the data that is made in these if statements (probably just the 3d one tho bcus it's
        # clearly the best) to a file. This will be something which counts how the quantity of items below the buy line
        # and their respective price, to give a 'potential profit from exchange sales' value. Each Q will have it's own
        # value, this way I can sort the element and it will give me the items that likely have the most profit
        # potential. Some quick sales chats saying 'Buying X' later and then PROFIT.

        # While not currently used, these last 3 lines help by generating a list of how many datapoints each db number has had.
        datapoints_dict = {}
        datapoints_dict['db_name'] = db_name
        datapoints_dict['datapoints'] = datapoints
        # This bit ain't ideal but it'll work for 99% of cases
        # print(datapoints_dict)
        if chart_type == 'scatter':
            print('Built ' + db_name + " (" + str(db_number) + ") charts, with Q's " + str(
                which_qualities) + '. There are ' + str(datapoints) + ' datapoints.')
            datapoints_dict_list.append(datapoints_dict.copy())


    Build_1_chart(db_number, db_name, save_location, all_quality, host_name, datapoints, which_qualities, chart_type,
              first_timestamp, mid_timestamp, last_timestamp, all_quantity, df1, all_data, special_list, all_dates,
              market_states, market_dates, market_state_colours, all_prices, sorted_prices, original_db_number)


def update_datapoints():
    from operator import itemgetter
    # print(datapoints_dict_list)
    sorted_datapoints_list = sorted(datapoints_dict_list, key=itemgetter('datapoints'), reverse=True)
    print(sorted_datapoints_list)

    names_list = []
    datapoints_list = []
    for x in sorted_datapoints_list:
        names_list.append(x['db_name'])
        datapoints_list.append(x['datapoints'])

    fig = go.Figure([go.Bar(x=names_list, y=datapoints_list)])
    fig.write_html('Datapoints' + '.html', auto_open=True)

    file_name = 'datapoints.txt'
    with open(os.path.join(r'C:\Users\PC\PycharmProjects\Simcompanies\Files', file_name),
              "w") as file1:
        file1.write(str(sorted_datapoints_list))
        file1.close()


def update_all_charts():
    print('Starting off by updating our price targets')
    #calculate_targets()
    print('Building all charts')

    # While this is not the most efficent way to update all charts, because we are getting the data for each chart 3
    # times, I really don't care enough to code a fix for it because it's not very intensive to get that data.
    for x in db_numbers_that_can_be_sold:
        # Set these to true if you are a masochist (and like to kill your browser).
        build_chart(x['id'], 'scatter3d', False)
        build_chart(x['id'], 'scatter', False)
        build_chart(x['id'], 'hloc', False)
        build_chart(x['id'], 'overview', False)

update_all_charts()
update_datapoints()

# build_chart(80,'overview',True,qualities=[2])