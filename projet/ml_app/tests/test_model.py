import unittest
import joblib

class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = joblib.load('house_price_model.pkl')

    def test_model_prediction(self):
        test_features = [[3, 2, 1400, 5000, 0, 3, 8, 2000]]
        prediction = self.model.predict(test_features)
        self.assertGreater(prediction[0], 0)
