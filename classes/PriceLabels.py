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

        self.buy_values: list = [data.buy_value for data in self.gold_price_history.data]
        self.sell_values: list = [data.sell_value for data in self.gold_price_history.data]

        self.difference = self.sell_values[-1] - self.buy_values[-1]
        self.difference_label = ttk.Label(self.app, text=f"Chênh lệch: {format_num_to_vnd_str(self.difference)}", style=LIGHT, font=("Verdana", 14))
        self.buy_price_label = ttk.Label(self.app, text=f"{format_num_to_vnd_str(self.buy_values[-1])}", style=DANGER, font=("Verdana", 28, 'bold'))
        self.sell_price_label = ttk.Label(self.app, text=f"{format_num_to_vnd_str(self.sell_values[-1])}", style=SUCCESS, font=("Verdana", 28, 'bold'))

    def build(self):
        self.buy_price_label.pack(side=LEFT, padx=55, pady=25)
        self.sell_price_label.pack(side=RIGHT, padx=55, pady=25)
        self.difference_label.place(relx=0.5, rely=0.91, anchor='center')

    def rebuild(self):
        self.buy_values: list = [data.buy_value for data in self.gold_price_history.data]
        self.sell_values: list = [data.sell_value for data in self.gold_price_history.data]

        self.difference = self.sell_values[-1] - self.buy_values[-1]
        self.difference_label.configure(text=f"Chênh lệch: {format_num_to_vnd_str(self.difference)}")
        self.buy_price_label.configure(text=f"{format_num_to_vnd_str(self.buy_values[-1])}")
        self.sell_price_label.configure(text=f"{format_num_to_vnd_str(self.sell_values[-1])}")