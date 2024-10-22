from typing import List
from classes.GoldPriceData import GoldPriceData

class GoldPriceResponse:
    def __init__(self, success: bool, latest_date: str, data: List[GoldPriceData]):
        self.success = success
        self.latest_date = latest_date
        self.data = data

    @staticmethod
    def from_json(json_data: dict) -> 'GoldPriceResponse':
        data = [GoldPriceData(
            price_data_id=item['Id'],
            type_name=item['TypeName'],
            branch_name=item['BranchName'],
            buy=item['Buy'],
            buy_value=item['BuyValue'],
            sell=item['Sell'],
            sell_value=item['SellValue'],
            buy_differ=item['BuyDiffer'],
            buy_differ_value=item['BuyDifferValue'],
            sell_differ=item['SellDiffer'],
            sell_differ_value=item['SellDifferValue'],
            group_date=item['GroupDate']
        ) for item in json_data['data']]
        return GoldPriceResponse(success=json_data['success'], latest_date=json_data['latestDate'], data=data)