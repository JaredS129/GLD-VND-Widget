import matplotlib
import threading

from ttkbootstrap import LIGHT

from classes.PriceHistoryChart import PriceHistoryChart
from classes.PriceLabels import PriceLabels
from utils.get_product_id_by_branch_and_product_name import get_product_id_by_branch_and_product_name

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
product_id = 1

gold_price_history = PriceApi.get_gold_price_history(product_id, from_date, to_date)

price_history_chart = PriceHistoryChart(app, gold_price_history, colors)
price_labels = PriceLabels(app, gold_price_history, colors)

def refresh_state():
    updated_gold_price_history = PriceApi.get_gold_price_history(product_id, from_date, to_date)
    price_labels.gold_price_history = updated_gold_price_history
    price_history_chart.gold_price_history = updated_gold_price_history
    price_labels.rebuild()
    price_history_chart.rebuild()

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
branches_options = [branch.name for branch in product_tree.branches]
products_options = [product.name for product in product_tree.branches[0].products]

def on_branch_select(event):
    global product_id
    selected_branch = event.widget.get()
    new_products_options = [product.name for branch in product_tree.branches if branch.name == selected_branch for product in branch.products]
    product_select['values'] = new_products_options
    product_select.current(0)
    product_id = get_product_id_by_branch_and_product_name(product_tree, selected_branch, new_products_options[0])
    on_refresh()

def on_product_select(event):
    global product_id
    selected_product = event.widget.get()
    product_id = get_product_id_by_branch_and_product_name(product_tree, branch_select.get(), selected_product)
    on_refresh()

branch_select = ttk.Combobox(dropdown_frame, style=LIGHT, width=50)
branch_select['values'] = branches_options
branch_select.current(0)

branch_select.bind("<<ComboboxSelected>>", on_branch_select)

product_select = ttk.Combobox(dropdown_frame, style=LIGHT, width=50)
product_select['values'] = products_options
product_select.current(0)

product_select.bind("<<ComboboxSelected>>", on_product_select)

branch_select.pack(side='left', fill='x', expand=True, padx=10, pady=5)
product_select.pack(side='left', fill='x', expand=True, padx=10, pady=5)

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