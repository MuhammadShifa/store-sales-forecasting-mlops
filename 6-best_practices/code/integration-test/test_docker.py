import os
import json

import requests
from deepdiff import DeepDiff

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))


with open("event.json", "rt", encoding="utf-8") as f_in:
    event = json.load(f_in)


URL = "http://localhost:8080/2015-03-31/functions/function/invocations"
actual_response = requests.post(URL, json=event, timeout=int(REQUEST_TIMEOUT))

print("actual response: ")

print(json.dumps(actual_response, indent=2))

expected_response = {
    "predictions": [
        {
            "model": "sales_prediction_model",
            "version": "Test123",
            "prediction": {"sales_prediction": 222.69, "sales_id": 512},
        }
    ]
}

diff = DeepDiff(actual_response, expected_response, significant_digits=1)
print(diff)

assert "type_changes" not in diff
assert "values_changed" not in diff
