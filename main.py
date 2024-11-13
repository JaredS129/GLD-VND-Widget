import matplotlib
from classes.PriceHistoryChart import PriceHistoryChart
from classes.PriceLabels import PriceLabels
matplotlib.use("TkAgg")
from datetime import datetime, timedelta
import ttkbootstrap as ttk
from classes.PriceApi import PriceApi, ApiResponseError, AllCurrentGoldPricesResponse

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

price_history_chart = PriceHistoryChart(app, gold_price_history, colors)
price_history_chart.build()

price_labels = PriceLabels(app, gold_price_history, colors)
price_labels.build()

app.mainloop()