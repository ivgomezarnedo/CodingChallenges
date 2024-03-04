from services.profit_loss_service import ProfitLossService
from services.balance_sheet_service import BalanceSheetService
from adapters.input_adapters.json_input_adapter import JSONInputAdapter
from adapters.output_adapters.console_output_adapter import ConsoleOutputAdapter

# Initialize parameters
business_id = 'TEST_ID'
year_month = "2022-02"

# Initialize adapters
json_profit_loss_adapter = JSONInputAdapter('files/profit_loss.json')
json_balance_sheet_adapter = JSONInputAdapter('files/balance_sheet.json')
console_output_adapter = ConsoleOutputAdapter()

# Initialize services with the corresponding adapters
profit_loss_service = ProfitLossService(json_profit_loss_adapter, console_output_adapter)
balance_sheet_service = BalanceSheetService(json_balance_sheet_adapter, console_output_adapter, year_month)

# Use the services
profit_loss_data = profit_loss_service.get_profit_loss_data(business_id)
balance_sheet_data = balance_sheet_service.get_balance_sheet_data(business_id)

# Output the data
console_output_adapter.output_data(profit_loss_data)
console_output_adapter.output_data(balance_sheet_data)
