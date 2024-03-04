import unittest
from unittest.mock import Mock
from src.services.balance_sheet_service import BalanceSheetService

#TODO: ADD MORE TESTS

class TestBalanceSheetService(unittest.TestCase):

    def setUp(self):
        # Mock input and output adapters
        self.input_adapter_mock = Mock()
        self.output_adapter_mock = Mock()

        # Define a month_key for testing
        self.month_key = "2022-02"

        # Initialize the BalanceSheetService with mocks and the test month_key
        self.service = BalanceSheetService(
            input_adapter=self.input_adapter_mock,
            output_adapter=self.output_adapter_mock,
            month_key=self.month_key
        )

    def test_get_balance_sheet_data(self):
        # Set up mock return value for the input adapter's fetch_data method
        mock_balance_sheet_data = {
            "report": {
                "updatedAt": "2022-02-13T00:00:00",
                "assets": {
                    "name": "Assets",
                    "items": [
                        {
                            "name": "Fixed Assets",
                            "value": 25000,
                            "items": [{"name": "Equipment", "value": 50000}]
                        },
                        {
                            "name": "Fixed Assets",
                            "value": 25000,
                            "items": [{"name": "Equipment", "value": 50000}]
                        },
                        {
                            "name": "Current Assets",
                            "value": 150000,
                            "items": [{"name": "Cash", "value": 100000}, {"name": "Accounts Receivable", "value": 50000}]
                        }
                    ]
                },
                "liabilities": {
                    "name": "Liabilities",
                    "items": [
                        {
                            "name": "Current Liabilities",
                            "value": 20000,
                            "items": [{"name": "Accounts Payable", "value": 20000}]
                        }
                    ]
                }
            }
        }
        self.input_adapter_mock.fetch_data.return_value = mock_balance_sheet_data

        business_id = "test_business"

        result = self.service.get_balance_sheet_data(business_id)

        self.assertEqual(result['business_id'], business_id)
        self.assertEqual(result['assets_breakdown']['Fixed Assets'], 50000)
        self.assertEqual(result['assets_breakdown']['Current Assets'], 150000)
        self.assertEqual(result['liabilities_value'], 20000)
        self.assertTrue('liabilities_to_income' in result)
        self.assertEqual(result['year'], 2022)
        self.assertEqual(result['month'], 2)
        self.assertEqual(result['month_key'], self.month_key)
        self.assertEqual(result['updated_at'], "2022-02-13T00:00:00")


    # All the other methods are private so these methods will be tested indirectly by the `get_balance_sheet_data` method.
    # TODO: Add more tests if methods are changed to 'static'.


if __name__ == '__main__':
    unittest.main()
