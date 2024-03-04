from interfaces.input_interface import InputInterface
from interfaces.output_interface import OutputInterface
from datetime import datetime

# Aux methods could be static.
# It allows the methods to use the instance's state, which could be beneficial if the logic for calculating metrics becomes more complex and requires accessing other instance variables or methods.
# TODO: Add comments to methods
class ProfitLossService:
        def __init__(self, input_adapter: InputInterface, output_adapter: OutputInterface):
            self.input_adapter = input_adapter
            self.output_adapter = output_adapter

        def get_profit_loss_data(self, identifier: str):
            profit_loss_data = self.input_adapter.fetch_data(identifier)
            profit_loss_metrics = self._calculate_profit_loss_metrics(profit_loss_data)
            profit_loss_metrics['type'] = 'Profit and Loss Metrics'
            profit_loss_metrics['business_id'] = identifier
            return profit_loss_metrics

        def _calculate_profit_loss_metrics(self, profit_loss_data):
            reports = profit_loss_data['reports']
            reports.sort(key=lambda x: x['toDate'], reverse=True)
            latest_report = reports[0]
            metrics = self._get_metrics(latest_report)
            metrics['detailed_expenses'] = self._get_detailed_expenses(latest_report['expenses']['items'])

            if len(reports) > 3:
                past_three_months_reports = reports[1:4]
                metrics['last_3_months_avg'] = self._get_last_3_months_avg(past_three_months_reports)
                metrics['avg_income_year_ago'] = self._get_avg_income_year_ago()
                year_over_year_income = metrics['avg_income_year_ago']
                metrics['avg_income_change_y_over_y'] = (
                    (metrics['last_3_months_avg']['income'] - year_over_year_income) / year_over_year_income * 100
                    if year_over_year_income != 0 else 0
                )

            return metrics

        def _get_metrics(self, latest_report):
            income = latest_report['income']['value']
            cost_of_sales = latest_report['costOfSales']['value']
            expenses = latest_report['expenses']['value']
            gross_profit = income - cost_of_sales
            net_profit = gross_profit - expenses
            profit_margin = net_profit / income if income != 0 else 0
            date_object = datetime.strptime(latest_report['toDate'], '%Y-%m-%dT%H:%M:%S')
            month_key = f"{date_object.year}-{date_object.month:02d}"
            return {
                'income': income,
                'costOfSales': cost_of_sales,
                'expenses': expenses,
                'gross_profit': gross_profit,
                'net_profit': net_profit,
                'profit_margin': profit_margin,
                'year': date_object.year,
                'month': date_object.month,
                'month_key': month_key,
                'updated_at': latest_report['updatedAt']
            }

        def _get_detailed_expenses(self, expenses_details):
            return {expense['name']: expense['value'] for expense in expenses_details}

        def _get_last_3_months_avg(self, past_three_months_reports):
            return {
                metric: sum(report[metric]['value'] for report in past_three_months_reports) / 3
                for metric in ['income', 'costOfSales', 'expenses']
            }

        def _get_avg_income_year_ago(self):
            # TODO: Replace this with actual logic to calculate the last 3 month avg of income from a year ago.
            return 120000  # Placeholder value
