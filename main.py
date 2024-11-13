import matplotlib
import threading

from classes.DropdownSelect import DropdownSelect
from classes.PriceHistoryChart import PriceHistoryChart
from classes.PriceLabels import PriceLabels
matplotlib.use("TkAgg")
from datetime import datetime, timedelta
import ttkbootstrap as ttk
from classes.PriceApi import PriceApi, ApiResponseError
from classes.FunctionTimer import FunctionTimer
from utils.build_product_tree import build_product_tree

app = ttk.Window(themename='darkly')
colors = app.style.colors

all_current_gold_prices = PriceApi.get_all_current_gold_prices()

to_date = datetime.now()
from_date = datetime.now() - timedelta(days=89)
gold_price_id = 81

gold_price_history = PriceApi.get_gold_price_history(gold_price_id, from_date, to_date)

price_history_chart = PriceHistoryChart(app, gold_price_history, colors)
price_labels = PriceLabels(app, gold_price_history, colors)

def refresh_state():
    updated_gold_price_history = PriceApi.get_gold_price_history(gold_price_id, from_date, to_date)
    price_labels.gold_price_history = updated_gold_price_history
    price_history_chart.gold_price_history = updated_gold_price_history
    price_labels.refresh_state()

def on_refresh():
    refresh_state()
    refresh_timer.remaining_seconds = refresh_timer.initial_time
    refresh_timer.refresh_button.configure(state='normal', text=f'Làm Mới ({refresh_timer.remaining_seconds})')

if isinstance(all_current_gold_prices, ApiResponseError):
    print(all_current_gold_prices.error)

if isinstance(gold_price_history, ApiResponseError):
    print(gold_price_history.error)

product_tree = build_product_tree(all_current_gold_prices)

# Create a frame to hold the dropdown menus
dropdown_frame = ttk.Frame(app)
dropdown_frame.pack(fill='x', side='top', padx=10, pady=5)

branch_select = DropdownSelect(dropdown_frame, [branch.name for branch in product_tree.branches], colors)
product_select = DropdownSelect(dropdown_frame, [product.name for product in product_tree.branches[0].products], colors)

branch_select.build()
product_select.build()

price_history_chart.build()

refresh_timer = FunctionTimer(app, refresh_state)

refresh_countdown_bar = refresh_timer.progress_bar
refresh_button = refresh_timer.refresh_button
refresh_button.configure(command=on_refresh)
refresh_button.pack(expand=True, padx=20)
refresh_countdown_bar.pack(expand=True, padx=20, pady=10)

thread = threading.Thread(target=refresh_timer.refresh_data)
thread.start()

price_labels.build()

app.mainloop()