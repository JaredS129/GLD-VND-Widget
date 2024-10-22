from typing import Optional

class GoldPriceData:
    def __init__(self, price_data_id: int, type_name: str, branch_name: str, buy: str, buy_value: float, sell: str, sell_value: float, buy_differ: Optional[str], buy_differ_value: float, sell_differ: Optional[str], sell_differ_value: float, group_date: str):
        self.price_data_id = price_data_id
        self.type_name = type_name
        self.branch_name = branch_name
        self.buy = buy
        self.buy_value = buy_value
        self.buy_differ = buy_differ
        self.sell = sell
        self.sell_value = sell_value
        self.buy_differ = buy_differ
        self.buy_differ_value = buy_differ_value
        self.sell_differ = sell_differ
        self.sell_differ_value = sell_differ_value
        self.group_date = group_date