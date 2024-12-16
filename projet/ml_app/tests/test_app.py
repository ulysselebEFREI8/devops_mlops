import unittest
from app import app

class TestAppRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_predict_route(self):
        response = self.client.post('/predict', data={'bedrooms': 3, 'bathrooms': 2, 'sqft_living': 1400, 'sqft_lot': 5000, 'waterfront': 0, 'condition': 3, 'grade': 8, 'yr_built': 2000})
        self.assertEqual(response.status_code, 200)
