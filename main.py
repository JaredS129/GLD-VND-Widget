import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
import matplotlib.dates as mdates
from classes.PriceApi import PriceApi, ApiResponseError, AllCurrentGoldPricesResponse, GoldPriceHistoryResponse

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
graph_frame = Figure(figsize=(7, 4), dpi=100)
line_graph = graph_frame.add_subplot(111)

# Plot the buy and sell values
line_graph.plot(dates, buy_values, label='Buy', color=colors.success)
line_graph.plot(dates, sell_values, label='Sell', color=colors.danger)

# Format the chart
line_graph.set_title(f"{gold_price_history.data[0].branch_name}: {gold_price_history.data[0].type_name} - 90 ngày qua", color=colors.light)
line_graph.set_xlabel('Date', color=colors.light)
line_graph.set_ylabel('Price', color=colors.light)
line_graph.legend()

# Remove the x and y value labels
line_graph.set_xticklabels([])
line_graph.set_yticklabels([])

# Remove the black border
line_graph.spines['top'].set_visible(False)
line_graph.spines['right'].set_visible(False)
line_graph.spines['left'].set_visible(False)
line_graph.spines['bottom'].set_visible(False)

# Remove the ticks
line_graph.tick_params(axis='both', which='both', length=0)

# Create annotations
annotation = line_graph.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=None)
annotation.set_visible(False)

def update_annotation(x_value):
    texts = [f"{x_value}"]
    for line in line_graph.get_lines():
        if line.get_label() in ["Buy", "Sell"]:
            x, y = line.get_data()
            if x_value in x:
                index = list(x).index(x_value)
                texts.append(f"{line.get_label()}: {y[index]}")
    annotation.set_text("\n".join(texts))
    annotation.get_bbox_patch().set_facecolor(colors.light)
    annotation.get_bbox_patch().set_alpha(1)
    for line in line_graph.get_lines():
        if line.get_label().startswith("_"):
            line.remove()
    line_graph.axvline(x=x_value, color=colors.light, linestyle='dotted', linewidth=1, alpha=0.3)

def hover(event):
    vis = annotation.get_visible()
    if event.inaxes == line_graph:
        for line in line_graph.get_lines():
            x, y = line.get_data()
            if len(x) > 0 and event.xdata is not None:
                x_datetime = mdates.num2date(event.xdata).replace(tzinfo=None)  # Convert event.xdata to naive datetime
                x_value = min(x, key=lambda x_val: abs(x_val.replace(tzinfo=None) - x_datetime))
                if abs(x_value - x_datetime).total_seconds() < 86400:  # Adjust the threshold as needed
                    annotation.xy = (mdates.date2num(x_value), event.ydata)
                    update_annotation(x_value)
                    annotation.set_visible(True)
                    graph_frame.canvas.draw_idle()
                    return
    if vis:
        annotation.set_visible(False)
        graph_frame.canvas.draw_idle()

# Set the tick parameters to match the theme
line_graph.tick_params(axis='x', colors=colors.light)
line_graph.tick_params(axis='y', colors=colors.light)

# Set the figure background color to match the theme
graph_frame.patch.set_facecolor(colors.dark)
line_graph.set_facecolor(colors.dark)

# table.pack(fill=BOTH, expand=YES, padx=10, pady=10)

canvas = FigureCanvasTkAgg(graph_frame, master=app)
canvas.draw()
canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

canvas.mpl_connect("motion_notify_event", hover)

app.mainloop()