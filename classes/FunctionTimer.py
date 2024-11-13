import time
import ttkbootstrap as ttk
from ttkbootstrap import LIGHT


class FunctionTimer:
    def __init__(self, app, callback):
        self.app = app
        self.initial_time = 600  # 10 minutes
        self.callback = callback
        self.remaining_seconds = self.initial_time
        self.progress_bar = ttk.Progressbar(app, mode='determinate', style=LIGHT, maximum=100, length=150)
        self.refresh_button = ttk.Button(app, text=f'Làm Mới ({self.remaining_seconds})', style='light-outline')

    def refresh_data(self):
        while True:
            while self.remaining_seconds > 0:
                time.sleep(1)
                self.remaining_seconds -= 1
                progress_value = (self.remaining_seconds / self.initial_time) * 100
                self.progress_bar['value'] = progress_value
                self.refresh_button['text'] = f'Làm Mới ({self.remaining_seconds} giây)'
            self.refresh_button.configure(state='disabled', text='Đang làm mới...')
            self.callback()
            self.remaining_seconds = self.initial_time
            self.refresh_button.configure(state='normal', text=f'Làm Mới ({self.remaining_seconds})')