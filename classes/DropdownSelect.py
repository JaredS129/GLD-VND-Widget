from typing import Literal

import matplotlib
from PIL.ImageOps import expand

matplotlib.use("TkAgg")
from ttkbootstrap.constants import *
import ttkbootstrap as ttk

class DropdownSelect:
    def __init__(self, app, options: list[str], colors):
        self.app = app
        self.options = options
        self.colors = colors

        self.combo_box = ttk.Combobox(self.app, style=LIGHT, width=50)
        self.combo_box['values'] = self.options
        self.combo_box.current(0)

    def build(self):
        self.combo_box.pack(side='left', fill='x', expand=True, padx=10, pady=5)