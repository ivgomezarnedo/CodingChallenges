from interfaces.input_interface import InputInterface
# /business/{businessId}/monthly_balance_sheet?date={yyyy-mm}
# /business/{businessId}/profit_Loss

class APIInputAdapter(InputInterface):
    # To be implemented

    def fetch_data(self, id: str):
        raise NotImplementedError()