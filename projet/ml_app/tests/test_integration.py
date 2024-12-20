import unittest
from app import app

class TestAppIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_predict_integration(self):
        response = self.client.post('/predict', data={'bedrooms': 3, 'bathrooms': 2, 'sqft_living': 1400, 'sqft_lot': 5000, 'waterfront': 0, 'condition': 3, 'grade': 8, 'yr_built': 2000})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Le prix prédit de la maison est:', response.data.decode())
