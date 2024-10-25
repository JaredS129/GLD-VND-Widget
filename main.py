from classes.PriceApi import PriceApi, ApiResponseError, GoldPriceResponse

gold_price_response = PriceApi.get_all_current_gold_prices()

if isinstance(gold_price_response, GoldPriceResponse):
    print(gold_price_response.latest_date)
    for data in gold_price_response.data:
        branch_name = data.branch_name
        type_name = data.type_name
        buy = data.buy
        sell = data.sell
        print(f'{branch_name} - {type_name} - Buy: {buy} - Sell: {sell}')

if isinstance(gold_price_response, ApiResponseError):
    print(f'{gold_price_response.status_code} Status Error: {gold_price_response.error}')