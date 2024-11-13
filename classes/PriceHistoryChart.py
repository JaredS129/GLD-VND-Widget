import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from utils.format_num_to_vnd_str import format_num_to_vnd_str

class PriceHistoryChart:
    def __init__(self, app, gold_price_history, colors):
        self.app = app
        self.gold_price_history = gold_price_history
        self.colors = colors
        self.graph_frame = Figure(figsize=(7, 4), dpi=100)
        self.line_graph = self.graph_frame.add_subplot(111)
        self.annotation = self.line_graph.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                                   bbox=dict(boxstyle="round", fc="w"), arrowprops=None)
        self.annotation.set_visible(False)

    def build(self):
        dates: list[datetime] = [data.date for data in self.gold_price_history.data]
        buy_values: list = [data.buy_value for data in self.gold_price_history.data]
        sell_values: list = [data.sell_value for data in self.gold_price_history.data]
        # Plot the buy and sell values
        self.line_graph.plot(dates, buy_values, label='Mua vào', color=self.colors.danger, linewidth=2)
        self.line_graph.plot(dates, sell_values, label='Bán ra', color=self.colors.success, linewidth=2)

        # Format the chart
        self.line_graph.set_xlabel('Date', color=self.colors.light)
        self.line_graph.set_ylabel('Price', color=self.colors.light)
        self.line_graph.legend()

        # Remove the x and y value labels
        self.line_graph.set_xticklabels([])
        self.line_graph.set_yticklabels([])

        # Remove the black border
        self.line_graph.spines['top'].set_visible(False)
        self.line_graph.spines['right'].set_visible(False)
        self.line_graph.spines['left'].set_visible(False)
        self.line_graph.spines['bottom'].set_visible(False)

        # Remove the ticks
        self.line_graph.tick_params(axis='both', which='both', length=0)

        # Set the tick parameters to match the theme
        self.line_graph.tick_params(axis='x', colors=self.colors.light)
        self.line_graph.tick_params(axis='y', colors=self.colors.light)

        # Set the figure background color to match the theme
        self.graph_frame.patch.set_facecolor(self.colors.bg)
        self.line_graph.set_facecolor(self.colors.bg)

        canvas = FigureCanvasTkAgg(self.graph_frame, master=self.app)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, pady=35)

        canvas.mpl_connect("motion_notify_event", self.hover)

    def update_annotation(self, x_value):
        texts = [f"{x_value.strftime('%d/%m/%Y')}"]
        price_to_compare: float = 0
        diff: float = 0
        for line in self.line_graph.get_lines():
            if line.get_label() in ["Mua vào", "Bán ra"]:
                x, y = line.get_data()
                if x_value in x:
                    index = list(x).index(x_value)
                    price = y[index]
                    texts.append(f"{line.get_label()}: {format_num_to_vnd_str(price)}")
                    diff = abs(price_to_compare - y[index])
                    price_to_compare = y[index]
        texts.append(f"Chênh lệch: {format_num_to_vnd_str(diff)}")
        self.annotation.set_text("\n".join(texts))
        self.annotation.get_bbox_patch().set_facecolor(self.colors.light)
        self.annotation.get_bbox_patch().set_alpha(1)
        for line in self.line_graph.get_lines():
            if line.get_label().startswith("_"):
                line.remove()
        self.line_graph.axvline(x=x_value, color=self.colors.light, linestyle='dotted', linewidth=1, alpha=0.3)

    def hover(self, event):
        vis = self.annotation.get_visible()
        if event.inaxes == self.line_graph:
            for line in self.line_graph.get_lines():
                x, y = line.get_data()
                if len(x) > 0 and event.xdata is not None:
                    x_datetime = mdates.num2date(event.xdata).replace(tzinfo=None)  # Convert event.xdata to naive datetime
                    x_value = min(x, key=lambda x_val: abs(x_val.replace(tzinfo=None) - x_datetime))
                    if abs(x_value - x_datetime).total_seconds() < 86400:  # Adjust the threshold as needed
                        self.annotation.xy = (mdates.date2num(x_value), event.ydata)
                        self.update_annotation(x_value)

                        # Check if the mouse is within the rightmost quarter of the graph
                        if event.x > 0.90 * self.line_graph.get_window_extent().width:
                            self.annotation.set_position((-130, 20))  # Move annotation to the left side
                        else:
                            self.annotation.set_position((20, 20))  # Default position

                        self.annotation.set_visible(True)
                        self.graph_frame.canvas.draw_idle()
                        return
        if vis:
            # check whether the mouse is withing the bounds of the graph
            if event.xdata is None and event.ydata is None:
                self.annotation.set_visible(False)
            self.graph_frame.canvas.draw_idle()

    def refresh_state(self):
        self.line_graph.clear()  # Clear the existing plot

        dates = [data.date for data in self.gold_price_history.data]
        buy_values = [data.buy_value for data in self.gold_price_history.data]
        sell_values = [data.sell_value for data in self.gold_price_history.data]

        # Re-plot the buy and sell values
        self.line_graph.plot(dates, buy_values, label='Mua vào', color=self.colors.danger, linewidth=2)
        self.line_graph.plot(dates, sell_values, label='Bán ra', color=self.colors.success, linewidth=2)

        # Re-format the chart
        self.line_graph.set_title(
            f"{self.gold_price_history.data[0].branch_name}: {self.gold_price_history.data[0].type_name} - 90 ngày qua",
            color=self.colors.light)
        self.line_graph.set_xlabel('Date', color=self.colors.light)
        self.line_graph.set_ylabel('Price', color=self.colors.light)
        self.line_graph.legend()

        # Remove the x and y value labels
        self.line_graph.set_xticklabels([])
        self.line_graph.set_yticklabels([])

        # Remove the black border
        self.line_graph.spines['top'].set_visible(False)
        self.line_graph.spines['right'].set_visible(False)
        self.line_graph.spines['left'].set_visible(False)
        self.line_graph.spines['bottom'].set_visible(False)

        # Remove the ticks
        self.line_graph.tick_params(axis='both', which='both', length=0)

        # Set the tick parameters to match the theme
        self.line_graph.tick_params(axis='x', colors=self.colors.light)
        self.line_graph.tick_params(axis='y', colors=self.colors.light)

        # Set the figure background color to match the theme
        self.graph_frame.patch.set_facecolor(self.colors.bg)
        self.line_graph.set_facecolor(self.colors.bg)

        self.graph_frame.canvas.draw_idle()  # Redraw the canvas