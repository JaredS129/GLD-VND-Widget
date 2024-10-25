from classes.PriceApi import PriceApi, ApiResponseError, AllCurrentGoldPricesResponse

all_current_gold_prices = PriceApi.get_all_current_gold_prices()

if isinstance(all_current_gold_prices, AllCurrentGoldPricesResponse):
    print(all_current_gold_prices.latest_date)
    for data in all_current_gold_prices.data:
        branch_name = data.branch_name
        type_name = data.type_name
        buy = data.buy
        sell = data.sell
        print(f'{branch_name} - {type_name} - Buy: {buy} - Sell: {sell}')

if isinstance(all_current_gold_prices, ApiResponseError):
    print(f'{all_current_gold_prices.status_code} Status Error: {all_current_gold_prices.error}')