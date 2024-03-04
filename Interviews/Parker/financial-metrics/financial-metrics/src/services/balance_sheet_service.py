from interfaces.input_interface import InputInterface
from interfaces.output_interface import OutputInterface
from datetime import datetime

# TODO: Add comments to methods


class BalanceSheetService:
    def __init__(self, input_adapter: InputInterface, output_adapter: OutputInterface, month_key: str):
        self.input_adapter = input_adapter
        self.output_adapter = output_adapter
        self.month_key = month_key  # Format: %Y-%m

    def get_balance_sheet_data(self, identifier: str):
        balance_sheet_data = self.input_adapter.fetch_data(identifier)
        balance_sheet_metrics = self._calculate_balance_sheet_metrics(balance_sheet_data)
        balance_sheet_metrics['type'] = 'Balance Sheet Metrics'
        balance_sheet_metrics['business_id'] = identifier
        return balance_sheet_metrics

    def _calculate_balance_sheet_metrics(self, balance_sheet_data):
        report = balance_sheet_data['report']
        assets_by_category = self._calculate_assets_by_category(report['assets']['items'])
        current_liabilities_value = self._calculate_current_liabilities(report['liabilities']['items'])
        sum_of_income_last_12_months = self._get_sum_of_income_last_12_months()

        date_object = datetime.strptime(self.month_key, '%Y-%m')
        return {
            'assets_breakdown': assets_by_category,
            'liabilities_value': current_liabilities_value,
            'liabilities_to_income': current_liabilities_value / sum_of_income_last_12_months if sum_of_income_last_12_months else 0,
            'year': date_object.year,
            'month': date_object.month,
            'month_key': self.month_key,
            'updated_at': report['updatedAt'],
        }

    def _calculate_assets_by_category(self, asset_items):
        return {
            item['name']: sum(sub_item['value'] for sub_item in item['items'])
            for item in asset_items
        }

    def _calculate_current_liabilities(self, liability_items):
        return next(
            (item['value'] for item in liability_items if item['name'] == 'Current Liabilities'),
            0
        )

    def _get_sum_of_income_last_12_months(self):
        # TODO: Replace this with actual logic to calculate the sum of income over the last 12 months.
        # Query to the system in which the profit_loss metrics are
        return 120000  # Placeholder value
