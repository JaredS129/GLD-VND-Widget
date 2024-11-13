from datetime import datetime
from typing import List
import json
from classes.GoldPriceData import GoldPriceData
import requests

from classes.ProductTree import ProductTree, Branch, Product


class ApiEndpoints:
    SJC_GOLD_PRICE_SERVICE = 'https://sjc.com.vn/GoldPrice/Services/PriceService.ashx'

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
        data = [GoldPriceData.from_json(item) for item in json_data['data']]
        response = AllCurrentGoldPricesResponse(success=json_data['success'], latest_date=json_data['latestDate'], data=data)
        return response

class GoldPriceHistoryResponse:
    def __init__(self, success: bool, data: List[GoldPriceData]):
        self.success = success
        self.data = data

    @staticmethod
    def from_json(json_data: dict) -> 'GoldPriceHistoryResponse':
        data = [GoldPriceData.from_json(item) for item in json_data['data']]
        return GoldPriceHistoryResponse(success=json_data['success'], data=data)

class PriceApi:
    def __init__(self, endpoints: ApiEndpoints, get_all_current_gold_prices: AllCurrentGoldPricesResponse | ApiResponseError):
        self.endpoints = endpoints
        self.get_all_current_gold_prices = get_all_current_gold_prices

    @staticmethod
    def get_all_current_gold_prices() -> AllCurrentGoldPricesResponse | ApiResponseError:
        response = requests.post(ApiEndpoints.SJC_GOLD_PRICE_SERVICE)
        try:
            parsed_response = response.json()
        except json.decoder.JSONDecodeError:
            return ApiResponseError(status_code=500, error='There was an error connecting to the API')

        if response.status_code == 200 and parsed_response['success']:
            json_data = parsed_response
            return AllCurrentGoldPricesResponse.from_json(json_data)
        else:
            return ApiResponseError(status_code=500, error='There was an error connecting to the API')

    @staticmethod
    def get_gold_price_history(gold_price_id: int, from_date: datetime, to_date: datetime) -> GoldPriceHistoryResponse | ApiResponseError:
        form_data = {
            'method': 'GetGoldPriceHistory',
            'goldPriceId': gold_price_id,
            'fromDate': from_date.strftime('%d/%m/%Y'),
            'toDate': to_date.strftime('%d/%m/%Y')
        }
        response = requests.post(ApiEndpoints.SJC_GOLD_PRICE_SERVICE, data=form_data)
        try:
            parsed_response = response.json()
        except json.decoder.JSONDecodeError:
            return ApiResponseError(status_code=500, error='There was an error connecting to the API')

        if response.status_code == 200 and parsed_response['success']:
            json_data = parsed_response
            return GoldPriceHistoryResponse.from_json(json_data)
        else:
            return ApiResponseError(status_code=500, error='There was an error connecting to the API')