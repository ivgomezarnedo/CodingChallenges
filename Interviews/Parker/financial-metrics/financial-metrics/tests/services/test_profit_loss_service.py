import unittest
from unittest.mock import Mock
from src.services.profit_loss_service import ProfitLossService
from src.interfaces.input_interface import InputInterface
from src.interfaces.output_interface import OutputInterface


# Additional test cases can be added for boundary conditions and error handling, such as:
# - What if `fetch_data` returns an empty list of reports?
# - How should the service behave if there are less than 3 months of reports?
# - How does the service handle a report with missing fields?

class TestProfitLossService(unittest.TestCase):
    def setUp(self):
        self.input_adapter_mock = Mock(spec=InputInterface)
        self.output_adapter_mock = Mock(spec=OutputInterface)
        self.service = ProfitLossService(self.input_adapter_mock, self.output_adapter_mock)
        self.mock_data = {
            "currency": "USD",
            "reports": [
                {
                    "updatedAt": "2022-02-13T00:00:00",
                    "fromDate": "2022-02-01T00:00:00",
                    "toDate": "2022-02-28T00:00:00",
                    "income": {
                        "value": 5000.00
                    },
                    "costOfSales": {
                        "value": 1500.00
                    },
                    "expenses": {
                        "name": "Expenses",
                        "value": 300.00,
                        "items": [
                            {
                                "name": "Light, Power, Heating",
                                "value": 300.00,
                                "items": []
                            }
                        ]
                    }
                },
                {
                    "updatedAt": "2022-01-13T00:00:00",
                    "fromDate": "2022-01-01T00:00:00",
                    "toDate": "2022-01-31T00:00:00",
                    "income": {
                        "value": 4500.00
                    },
                    "costOfSales": {
                        "value": 1200.00
                    },
                    "expenses": {
                        "value": 1800.00
                    }
                }
            ]
        }

    def test_get_profit_loss_data(self):
        identifier = "test_business"
        self.input_adapter_mock.fetch_data.return_value = self.mock_data

        result = self.service.get_profit_loss_data(identifier)

        self.input_adapter_mock.fetch_data.assert_called_once_with(identifier)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['business_id'], identifier)
        # Asserting detailed values like income, costOfSales, expenses
        self.assertEqual(result['income'], 5000.00)
        self.assertEqual(result['costOfSales'], 1500.00)
        self.assertEqual(result['expenses'], 300.00)
        #TODO: Add more assertions


# All the other methods are private so these methods will be tested indirectly by the `get_profit_loss_data` method.

if __name__ == '__main__':
    unittest.main()
