import matplotlib
from classes.PriceHistoryChart import PriceHistoryChart
matplotlib.use("TkAgg")
from datetime import datetime, timedelta
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from classes.PriceApi import PriceApi, ApiResponseError, AllCurrentGoldPricesResponse
from utils.format_num_to_vnd_str import format_num_to_vnd_str

app = ttk.Window(themename='darkly')
colors = app.style.colors

all_current_gold_prices = PriceApi.get_all_current_gold_prices()

to_date = datetime.now()
from_date = datetime.now() - timedelta(days=89)
gold_price_id = 81

gold_price_history = PriceApi.get_gold_price_history(gold_price_id, from_date, to_date)

if isinstance(all_current_gold_prices, AllCurrentGoldPricesResponse):
    print('Fetched current gold prices successfully')

if isinstance(all_current_gold_prices, ApiResponseError):
    print(all_current_gold_prices.error)

if isinstance(gold_price_history, ApiResponseError):
    print(gold_price_history.error)

# Extract dates and prices for the line chart
dates: list[datetime] = [data.date for data in gold_price_history.data]
buy_values: list = [data.buy_value for data in gold_price_history.data]
sell_values: list = [data.sell_value for data in gold_price_history.data]

price_history_chart = PriceHistoryChart(app, gold_price_history, colors)
price_history_chart.build()

difference = sell_values[-1] - buy_values[-1]
difference_label = ttk.Label(app, text=f"{format_num_to_vnd_str(difference)}", style=LIGHT, font=("Verdana", 14))
buy_price_label = ttk.Label(app, text=f"{format_num_to_vnd_str(buy_values[-1])}", style=DANGER, font=("Verdana", 28, 'bold'))
sell_price_label = ttk.Label(app, text=f"{format_num_to_vnd_str(sell_values[-1])}", style=SUCCESS, font=("Verdana", 28, 'bold'))
buy_price_label.pack(side=LEFT, padx=55, pady=25)
sell_price_label.pack(side=RIGHT, padx=55, pady=25)
difference_label.place(relx=0.5, rely=0.91, anchor='center')

app.mainloop()