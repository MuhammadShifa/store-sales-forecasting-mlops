import requests

sample_input = {
    "date": "2022-12-25",
    "store": 2,
    "promo": 1,
    "holiday": 0
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=sample_input)
print(response.json())