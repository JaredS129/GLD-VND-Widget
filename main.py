import re
from xmlrpc.client import DateTime

from classes.PriceApi import PriceApi, ApiResponseError, AllCurrentGoldPricesResponse, GoldPriceHistoryResponse
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from datetime import datetime

app = ttk.Window()
colors = app.style.colors

col_data = [
    'Branch Name',
    'Type Name',
    "Buy",
    "Sell",
]

row_data = []

all_current_gold_prices = PriceApi.get_all_current_gold_prices()

from_date = datetime.strptime('01/10/2024', '%d/%m/%Y')
to_date = datetime.strptime('01/11/2024', '%d/%m/%Y')
gold_price_id = 81

gold_price_history = PriceApi.get_gold_price_history(gold_price_id, from_date, to_date)

if isinstance(all_current_gold_prices, AllCurrentGoldPricesResponse):
    for data in all_current_gold_prices.data:
        branch_name = data.branch_name
        type_name = data.type_name
        buy = data.buy
        sell = data.sell
        row_data.append([branch_name, type_name, buy, sell])

if isinstance(all_current_gold_prices, ApiResponseError):
    print(all_current_gold_prices.error)

if isinstance(gold_price_history, GoldPriceHistoryResponse):
    for data in gold_price_history.data:
        date_string = data.group_date
        timestamp = int(re.search(r'\d+', date_string).group())
        milliseconds = int(timestamp / 1000)
        formatted_date = datetime.fromtimestamp(milliseconds).strftime('%d/%m/%Y')
        print(f"Date: {formatted_date}, Buy: {data.buy_value}, Sell: {data.sell_value}")

if isinstance(all_current_gold_prices, ApiResponseError):
    print(gold_price_history.error)

table = Tableview(
    master=app,
    coldata=col_data,
    rowdata=row_data,
    paginated=True,
    searchable=True,
    bootstyle=PRIMARY,
    stripecolor=(colors.light, None),
)

table.pack(fill=BOTH, expand=YES, padx=10, pady=10)

app.mainloop()