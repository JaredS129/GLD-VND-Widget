import requests

response = requests.get('https://sjc.com.vn/GoldPrice/Services/PriceService.ashx')
print(response.status_code)
print(response.json())