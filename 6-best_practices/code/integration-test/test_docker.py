import requests 
import json
from deepdiff import DeepDiff


event = {
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49665655494408468328133797929966048802353963189214904322",
                "data": "eyJzYWxlc19pbnB1dCI6IHsiZGF0ZSI6ICIyMDIyLTEyLTI1IiwgInN0b3JlIjogMiwgInByb21vIjogMSwgImhvbGlkYXkiOiAwfSwgInNhbGVzX2lkIjogNTEyfQ==",
                "approximateArrivalTimestamp": 1753871077.078
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49665655494408468328133797929966048802353963189214904322",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::259959202267:role/lambda-kinesis-role",
            "awsRegion": "ap-south-1",
            "eventSourceARN": "arn:aws:kinesis:ap-south-1:259959202267:stream/sales_events"
        }
    ]
}


url = 'http://localhost:8080/2015-03-31/functions/function/invocations'
actual_response = requests.post(url, json=event).json()
print("actual response: ")

print(json.dumps(actual_response, indent=2))

expected_response = {'predictions': 
    [{'model': 'sales_prediction_model',
        'version': 'Test123', 
        'prediction': {'sales_prediction': 222.69, 
                    'sales_id': 512
                    }
        }]}

diff = DeepDiff(actual_response, expected_response , significant_digits=1)
print(diff)

assert 'type_changes' not in diff
assert 'values_changed' not in diff