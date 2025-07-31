from pathlib import Path

import model


def read_text(file):
    test_directory = Path(__file__).parent

    with open(test_directory / file, 'rt', encoding='utf-8') as f_in:
        return f_in.read().strip()

def test_base64_decode():
    input_base64 = "eyJzYWxlc19pbnB1dCI6IHsiZGF0ZSI6ICIyMDIyLTEyLTI1IiwgInN0b3JlIjogMiwgInByb21vIjogMSwgImhvbGlkYXkiOiAwfSwgInNhbGVzX2lkIjogNTEyfQ=="
    actual_results = model.base64_decode(input_base64)
    
    expected_results ={
        "sales_input": {"date": "2022-12-25", "store": 2, "promo": 1, "holiday": 0}, 
        "sales_id": 512
        }

    assert actual_results == expected_results


def test_prepare_features():
    model_service = model.ModelService(None)
    sales_input = {
        "date": "2022-12-25",
        "store": 2,
        "promo": 1,
        "holiday": 0
    }

    actual_features = model_service.prepare_features(sales_input)

    expected_features = {
        'store': 2, 
        'promo': 1, 
        'holiday': 0, 
        'year': 2022, 
        'month': 12, 
        'dayofweek': 6, 
        'is_weekend': 1
        }

    assert actual_features == expected_features


# Creates a fake (mock) model that always returns the prediction 500.0
# This is useful for testing, so you don’t use a real model instead class ModelMock:

class ModelMock:
    def __init__(self, value):
        self.value = value

    def predict(self, X):
        n = len(X)
        return [self.value] * n


def test_predict():
    model_mock = ModelMock(500.0)
    # Creates a ModelService instance and gives it the fake model (model_mock) to use.
    # Now, any prediction made through model_service will use that mock.
    model_service = model.ModelService(model_mock)
    features = {
        'store': 2, 
        'promo': 1, 
        'holiday': 0, 
        'year': 2022, 
        'month': 12, 
        'dayofweek': 6, 
        'is_weekend': 1
        }

    actual_prediction = model_service.predict(features)
    expected_prediction = 500.0

    assert actual_prediction == expected_prediction


def test_lambda_handler():
    model_mock = ModelMock(500.0)
    model_version = 'Test123'
    input_base64 = "eyJzYWxlc19pbnB1dCI6IHsiZGF0ZSI6ICIyMDIyLTEyLTI1IiwgInN0b3JlIjogMiwgInByb21vIjogMSwgImhvbGlkYXkiOiAwfSwgInNhbGVzX2lkIjogNTEyfQ=="
    event = {
        "Records": [
            {
                "kinesis": {"data": input_base64},
            }
        ]
    }

    model_service = model.ModelService(model=model_mock, model_version=model_version)
    actual_prediction = model_service.lambda_handler(event)
    expected_predictions = {
        'predictions': [
            {
                'model': 'sales_prediction_model',
                'version': model_version,
                'prediction': {
                    'sales_prediction': 500.0,
                    'sales_id': 512
                },
            }
        ]
    }

    assert actual_prediction == expected_predictions