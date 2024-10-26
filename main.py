from widget import Widget
import tkinter as tk
from datetime import datetime


class date_time(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(percent=20, time=10, *args, **kwargs)

        self.time = tk.StringVar()
        self.time.set(datetime.now().strftime("%H:%M:%S"))
        self.time_label = tk.Label(self, textvariable=self.time, font=("Helvetica", 48))
        self.time_label.pack(expand=True, fill="both", padx=25, pady=(25, 0))
        self.time_label.bind("<Button-1>", self.get_pos)

        self.date = tk.StringVar()
        self.date.set(datetime.now().strftime("%A %d %B %Y").title())
        self.date_label = tk.Label(self, textvariable=self.date, font=("Helvetica", 24))
        self.date_label.pack(expand=True, fill="both", padx=25, pady=(0, 25))
        self.date_label.bind("<Button-1>", self.get_pos)

        self.update_time()

    def update_time(self):
        self.time.set(datetime.now().strftime("%H:%M:%S"))
        self.app.after(1000, self.update_time)


if __name__ == "__main__":
    date_time().app.mainloop()

# from classes.PriceApi import PriceApi, ApiResponseError, AllCurrentGoldPricesResponse
# import tkinter as tk
# import ttkbootstrap as ttk
# from ttkbootstrap.tableview import Tableview
# from ttkbootstrap.constants import *
#
# app = ttk.Window()
# colors = app.style.colors
#
# col_data = [
#     'Branch Name',
#     'Type Name',
#     {"text": "Buy", "stretch": False},
#     {"text": "Sell", "stretch": False}
# ]
#
# row_data = []
#
# all_current_gold_prices = PriceApi.get_all_current_gold_prices()
#
# if isinstance(all_current_gold_prices, AllCurrentGoldPricesResponse):
#     print(all_current_gold_prices.latest_date)
#     for data in all_current_gold_prices.data:
#         branch_name = data.branch_name
#         type_name = data.type_name
#         buy = data.buy
#         sell = data.sell
#         row_data.append([branch_name, type_name, buy, sell])
#         print(f'{branch_name} - {type_name} - Buy: {buy} - Sell: {sell}')
#
# if isinstance(all_current_gold_prices, ApiResponseError):
#     print(f'{all_current_gold_prices.status_code} Status Error: {all_current_gold_prices.error}')
#
# table = Tableview(
#     master=app,
#     coldata=col_data,
#     rowdata=row_data,
#     paginated=True,
#     searchable=True,
#     bootstyle=PRIMARY,
#     stripecolor=(colors.light, None),
# )
#
# table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
#
# app.mainloop()