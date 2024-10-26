from classes.PriceApi import PriceApi, ApiResponseError, AllCurrentGoldPricesResponse
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *

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

if isinstance(all_current_gold_prices, AllCurrentGoldPricesResponse):
    print(all_current_gold_prices.latest_date)
    for data in all_current_gold_prices.data:
        branch_name = data.branch_name
        type_name = data.type_name
        buy = data.buy
        sell = data.sell
        row_data.append([branch_name, type_name, buy, sell])
        print(f'{branch_name} - {type_name} - Buy: {buy} - Sell: {sell}')

if isinstance(all_current_gold_prices, ApiResponseError):
    print(f'{all_current_gold_prices.status_code} Status Error: {all_current_gold_prices.error}')

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