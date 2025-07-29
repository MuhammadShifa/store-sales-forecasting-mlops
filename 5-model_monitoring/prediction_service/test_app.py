import requests

sample_input = {
    "date": "2022-1-28",
    "store": 7,
    "promo": 1,
    "holiday": 1
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=sample_input)
print(response.json())