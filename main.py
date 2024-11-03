import re

from classes.PriceApi import PriceApi, ApiResponseError, AllCurrentGoldPricesResponse, GoldPriceHistoryResponse
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from datetime import datetime, timedelta

app = ttk.Window()
colors = app.style.colors

col_data = [
    'Date',
    "Buy",
    "Sell",
]

row_data = []

all_current_gold_prices = PriceApi.get_all_current_gold_prices()

to_date = datetime.now()
from_date = datetime.now() - timedelta(days=89)
gold_price_id = 81

gold_price_history = PriceApi.get_gold_price_history(gold_price_id, from_date, to_date)

if isinstance(all_current_gold_prices, AllCurrentGoldPricesResponse):
    print('Fetched current gold prices successfully')

if isinstance(all_current_gold_prices, ApiResponseError):
    print(all_current_gold_prices.error)

if isinstance(gold_price_history, GoldPriceHistoryResponse):
    print('Fetched gold price history successfully')
    for data in gold_price_history.data:
        row_data.append([data.date, data.buy_value, data.sell_value])

if isinstance(gold_price_history, ApiResponseError):
    print(gold_price_history.error)

table = Tableview(
    master=app,
    coldata=col_data,
    rowdata=row_data,
    bootstyle=PRIMARY,
    stripecolor=(colors.light, None),
)

table.pack(fill=BOTH, expand=YES, padx=10, pady=10)

app.mainloop()