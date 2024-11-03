from classes.PriceApi import PriceApi, ApiResponseError, AllCurrentGoldPricesResponse, GoldPriceHistoryResponse
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from datetime import datetime, timedelta
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

app = ttk.Window(themename='darkly')
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
)

# Extract dates and prices for the line chart
dates = [data.date for data in gold_price_history.data]
buy_values = [data.buy_value for data in gold_price_history.data]
sell_values = [data.sell_value for data in gold_price_history.data]

# Create a figure for the line chart
graph_frame = Figure(figsize=(5, 5), dpi=100)
line_graph = graph_frame.add_subplot(111)

# Plot the buy and sell values
line_graph.plot(dates, buy_values, label='Buy', color='blue')
line_graph.plot(dates, sell_values, label='Sell', color='red')

# Format the chart
line_graph.set_title('Gold Price History')
line_graph.set_xlabel('Date')
line_graph.set_ylabel('Price')
line_graph.legend()

table.pack(fill=BOTH, expand=YES, padx=10, pady=10)

canvas = FigureCanvasTkAgg(graph_frame, master=app)
canvas.draw()
canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

app.mainloop()