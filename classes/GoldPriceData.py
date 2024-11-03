from datetime import datetime
from typing import Optional
from utils.get_datetime_from_group_date_string import get_datetime_from_group_date_string

class GoldPriceData:
    def __init__(self, price_data_id: int, type_name: str, branch_name: str, buy: str, buy_value: float, sell: str, sell_value: float, buy_differ: Optional[str], buy_differ_value: float, sell_differ: Optional[str], sell_differ_value: float, date: datetime):
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
        self.date = date

    @staticmethod
    def from_json(json_data: dict) -> 'GoldPriceData':
        return GoldPriceData(
            price_data_id=json_data['Id'],
            type_name=json_data['TypeName'],
            branch_name=json_data['BranchName'],
            buy=json_data['Buy'],
            buy_value=json_data['BuyValue'],
            sell=json_data['Sell'],
            sell_value=json_data['SellValue'],
            buy_differ=json_data['BuyDiffer'],
            buy_differ_value=json_data['BuyDifferValue'],
            sell_differ=json_data['SellDiffer'],
            sell_differ_value=json_data['SellDifferValue'],
            date=get_datetime_from_group_date_string(json_data['GroupDate'])
        )

    def __iter__(self):
        return iter([self.price_data_id, self.type_name, self.branch_name, self.buy, self.buy_value, self.sell, self.sell_value, self.buy_differ, self.buy_differ_value, self.sell_differ, self.sell_differ_value, self.date])