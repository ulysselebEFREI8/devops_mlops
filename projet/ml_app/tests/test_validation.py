import unittest
from app import validate_data

class TestDataValidation(unittest.TestCase):
    def test_invalid_data(self):
        invalid_data = {'bedrooms': -1, 'bathrooms': 2, 'sqft_living': 1400, 'sqft_lot': 5000, 'waterfront': 0, 'condition': 3, 'grade': 8, 'yr_built': 2000}
        self.assertRaises(ValueError, validate_data, invalid_data)
