# SimCompaniesAnalysis

__Info for Devs:__

This colllection of python program files:
• Collects data from the Simcompanies API.
• Uses a weighted distribution of activity on different endpoints to avoid sending the servers uneccasry traffic.
• Scans for changes in the data and transforms this into stock-like OHLC data.
• Filters & cleans data.
• Visualises the OHLC data.
• Automattically generates graphs + reports using plotly which allows players to evuluate price trends. 
• There is also a sub-program which calculates which products are best to produce given product price trends.

Outputs can be found at: https://github.com/ThechnicallyAnIdiot/SimCompaniesAnalysis/tree/master/Files/Charts GitHub doesn't like these .html files, but here is an example: ![Automatiically generated chart of Bricks price history, seperated by quality](https://i.imgur.com/ObxGjuA.png)

For transparancy: This was my first large project. Inside it are huge quantities of poorly & inefficently written code, bad ideas and bad practices. I'm leaving it up publicly since I want to show my development as a programmer and my ability to improve my skills.

__Info for players:__

I am The Pollution Co. ingame, feel free to send me a DM.

Once I had it running a bit of analysis and you basically had won the game. That was never really the appeal to me, but it may be for you.

IMPORTANT:
1. THIS IS NOT A BOT. IT DOES NOT PLAY THE GAME FOR YOU, ONLY DOES THE MATH AND TELLS YOU HOW BEST TO PROFIT.
2. THIS IS ALLOWED TO RUN __ONLY__ IF YOU DO NOT INCREASE THE API THROTTLE.

The difference between this and the google sheets? This is more efficent, captures more detail of the market including volume, faster.

Run different .py files. They do what they say on the tin. Have an experiment with what does what.

main-online.py or main.py is what you need running on a server. It watches the exchange.

Some API connection may be out of date. I am not supporting them and neither is Patrick (Game Dev)

I have added API throttling. Please don't disable this. Decreasing the throttle or removing it may lead to a permaban.
