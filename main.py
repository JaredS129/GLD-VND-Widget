import matplotlib
import threading
from classes.PriceHistoryChart import PriceHistoryChart
from classes.PriceLabels import PriceLabels
matplotlib.use("TkAgg")
from datetime import datetime, timedelta
import ttkbootstrap as ttk
from classes.PriceApi import PriceApi, ApiResponseError
from classes.FunctionTimer import FunctionTimer

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

if isinstance(all_current_gold_prices, ApiResponseError):
    print(all_current_gold_prices.error)

if isinstance(gold_price_history, ApiResponseError):
    print(gold_price_history.error)

price_history_chart.build()

refresh_timer = FunctionTimer(app, refresh_state)

refresh_countdown_bar = refresh_timer.progress_bar
refresh_button = refresh_timer.refresh_button
refresh_button.pack(expand=True, padx=20)
refresh_countdown_bar.pack(expand=True, padx=20, pady=10)

thread = threading.Thread(target=refresh_timer.refresh_data)
thread.start()

price_labels.build()

app.mainloop()