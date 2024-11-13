import matplotlib
matplotlib.use("TkAgg")
from ttkbootstrap.constants import *
from utils.format_num_to_vnd_str import format_num_to_vnd_str
import ttkbootstrap as ttk

class PriceLabels:
    def __init__(self, app, gold_price_history, colors):
        self.app = app
        self.gold_price_history = gold_price_history
        self.colors = colors

    def build(self):
        buy_values: list = [data.buy_value for data in self.gold_price_history.data]
        sell_values: list = [data.sell_value for data in self.gold_price_history.data]

        difference = sell_values[-1] - buy_values[-1]
        difference_label = ttk.Label(self.app, text=f"{format_num_to_vnd_str(difference)}", style=LIGHT, font=("Verdana", 14))
        buy_price_label = ttk.Label(self.app, text=f"{format_num_to_vnd_str(buy_values[-1])}", style=DANGER, font=("Verdana", 28, 'bold'))
        sell_price_label = ttk.Label(self.app, text=f"{format_num_to_vnd_str(sell_values[-1])}", style=SUCCESS, font=("Verdana", 28, 'bold'))
        buy_price_label.pack(side=LEFT, padx=55, pady=25)
        sell_price_label.pack(side=RIGHT, padx=55, pady=25)
        difference_label.place(relx=0.5, rely=0.91, anchor='center')