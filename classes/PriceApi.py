from typing import List
import json
from classes.GoldPriceData import GoldPriceData
import requests

class ApiEndpoints:
    ALL_CURRENT_GOLD_PRICES = 'https://sjc.com.vn/GoldPrice/Services/PriceService.ashx'

class ApiResponseError:
    def __init__(self, status_code: int, error: str):
        self.status_code = status_code
        self.error = error

    @staticmethod
    def from_json(json_data: dict) -> 'ApiResponseError':
        return ApiResponseError(status_code=json_data['status_code'], error=json_data['error'])

class AllCurrentGoldPricesResponse:
    def __init__(self, success: bool, latest_date: str, data: List[GoldPriceData]):
        self.success = success
        self.latest_date = latest_date
        self.data = data

    @staticmethod
    def from_json(json_data: dict) -> 'AllCurrentGoldPricesResponse':
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
        return AllCurrentGoldPricesResponse(success=json_data['success'], latest_date=json_data['latestDate'], data=data)

class PriceApi:
    def __init__(self, endpoints: ApiEndpoints, get_all_current_gold_prices: AllCurrentGoldPricesResponse | ApiResponseError):
        self.endpoints = endpoints
        self.get_all_current_gold_prices = get_all_current_gold_prices

    @staticmethod
    def get_all_current_gold_prices() -> AllCurrentGoldPricesResponse | ApiResponseError:
        response = requests.get(ApiEndpoints.ALL_CURRENT_GOLD_PRICES)
        try:
            parsed_response = response.json()
        except json.decoder.JSONDecodeError:
            return ApiResponseError(status_code=500, error='There was an error connecting to the API')

        if response.status_code == 200 and parsed_response['success']:
            json_data = parsed_response
            return AllCurrentGoldPricesResponse.from_json(json_data)
        else:
            return ApiResponseError(status_code=500, error='There was an error connecting to the API')