import requests
from classes.GoldPriceResponse import GoldPriceResponse

response = requests.get('https://sjc.com.vn/GoldPrice/Services/PriceService.ashx')
if response.status_code == 200:
    json_data = response.json()
    gold_price_response = GoldPriceResponse.from_json(json_data)

    print(gold_price_response.latest_date)
    for data in gold_price_response.data:
        branch_name = data.branch_name
        type_name = data.type_name
        buy = data.buy
        sell = data.sell
        print(f'{branch_name} - {type_name} - Buy: {buy} - Sell: {sell}')
else:
    json_data = response.json()
    print(response.status_code, json_data['message'])