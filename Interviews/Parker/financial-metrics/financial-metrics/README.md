## Goal
Design a system for calculating financial business metrics for e-commerce businesses, from data obtained via third-party API integration.  

## Requirements
#### Documentation
Write a design document with enough details that someone other than yourself can follow and implement

Example areas of focus:
- Storage design, schema, type of storage, etc.
- System design, storage, pipeline, method of integration with third-party API, interface for retrieving metrics, etc.

We understand your time is valuable, so feel free to omit low-level details that you think are trivial, but the high level design shall be clear.  List assumptions you make.  Also there is no need to re-invent; feel free to use any actually available technology you think fits, with a quick description on why and how the technology helps.
#### Implementation
Implement the system that processes and loads the example payloads to the next system

You should focus on the design first and then work on this section last; we don't want this requirement to influence your design decision.  
We are only looking for the implementation of the immediate system that processes and loads the example JSON payloads; everything before and after that is not required.
We expect you to be able to set up a simple but testable environment for this. 
Depending on the complexity of your design, this, entirely or partially, could be optional but shall be reasonably justified.  Feel free to contact us to discuss this.

## Contexts
#### Third-party APIs
You are given API access to fetch data from the 2 following unrelated SaaS platforms.  One platform provides service to businesses for storing their "profit and loss" data, while the other platform is used for storing "balance sheet" data.  For simplicity, you can assume:
- all businesses use both platforms, 
- each business has a globally-unique "business identifier"
- the unique ID identifies the same businesses on both platforms. 

_SaaS API for Profit and Loss_
- /business/{businessId}/profit_Loss
  - example payload: profit_loss.json
  - returns all monthly data for the business, "updatedAt" field in each monthly payload changes only if the data has been updated for that month in third-party system

_SaaS API for Balance Sheet_
- /business/{businessId}/monthly_balance_sheet?date={yyyy-mm}
  - example payload: balance_sheet.json
  - returns data for the business for the month specified in the query param, "updatedAt" changes only if the data has been updated in third-party system

#### Business Requirements
- The system shall be able to calculate metrics for 10K, and increasing, businesses
- Metrics shall not be stale longer than 24 hours for all businesses, if new/updated data is available, i.e. if we look at the metrics for a business now, the metrics shall be based on the latest data made available by the third-party API within the last 24 hours
- Be able to see break-down of all secondary category of things, e.g. for balance_sheet assets, we need to be able to see and filter "Fixed Assets" and "Current Assets", same for profit_loss expenses, "Advertising & Marketing", "General Expenses", etc.
- For profit_loss, we need the following financial metrics for any given business for high-read use case:
  - income, costOfSales, expenses, gross_profit (income-costOfSales), net_profit (gross_profit-expenses), and profit_margin (net_profit/income) for below conditions
    - current month
    - last 3 month avg (not counting current month)
    - last 3 month avg change year-over-year (e.g. `(last 3 month avg of income)/(last 3 month avg of income from a year ago)`)
- For another high-read use case we need for a given business:
  - `Current month liabilities("Current Liabilities" only, ignore "Other Liabilities") / sum of income of last 12 months`

## Implementation
### High-Level Design
#### Data Storage
**Amazon DynamoDB** is chosen as the primary database for storing financial metrics due to its scalability, cost-effectiveness, and fully managed nature, which aligns well with the requirement of handling a large volume of data that is frequently updated. 
The metrics will be stored with the primary key as **business_id** and a sort key as **month_key** (i.e., *'2022_02'*). This design allows us to efficiently query data by business and time frame and easily replace outdated records with new data.
All the data could be stored in the same table (**financial_metrics**) due to following reasons:
- Balance sheet and Profit/Loss data contains the same PK and Sort Key.
- The process to get that data is going to be, presumable, run at the same time. 
- A No-SQL DB is being used, so to join the data is a very expensive operation.

**Justification**: Its high scalability, built-in redundancy, and cost-efficiency make it suitable for the data storage needs of this system. It allows us to leverage the benefits of NoSQL databases for quick reads and writes, which is essential for handling financial data that updates frequently.
#### Data Processing and Ingestion
**AWS Lambda** is selected for data processing and ingestion. Lambda functions are ideal for this scenario due to their ability to scale automatically in response to the invocation rate and execute code in response to HTTP requests using Amazon API Gateway or API calls made using AWS SDKs.
Since the computation required to process the financial data is not continuous but is triggered on a daily basis, the serverless model of AWS Lambda fits perfectly, reducing costs by running code only when needed.
Furthermore, the integration with **DynamoDB** is very straightforward.
**Justification**: Provides a serverless execution environment, which is cost-effective for tasks that need to run periodically. It also integrates well with other AWS services, which can simplify the system's architecture.

#### System Architecture
##### Hexagonal Architecture
The codebase is structured using [hexagonal architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) to promote clean code separation and to facilitate dependency injection.
This architecture choice simplifies the future expansion of the system, such as integrating direct API fetching methods instead of using static JSON files. 
The adapters in place can be easily replaced or extended to include new functionalities. If the source of the data change (e.g., an API is no longer being used and the data is being fetched from a SQL DB), we would only have to develop a new input adapter and to modify the injected dependency in the application main.

In an example of the usage of the [KISS principle](https://en.wikipedia.org/wiki/KISS_principle), no repositories (hexagonal) have been used and services interact directly with adapters as the data manipulation is straightforward and doesn't require additional layers of logic or abstraction.

**Justification**: Enhances maintainability and testability of the code by decoupling core logic from external concerns. This flexibility will be crucial for future integrations with third-party APIs and changing business requirements.
#### Interfaces and Services
- Input Interfaces (InputInterface): Define contracts for fetching data from different sources (e.g., APIs or static files).
- Output Interfaces (OutputInterface): Define contracts for writing processed data to various destinations (e.g., databases, console...).
- Services (ProfitLossService, BalanceSheetService): Contain business logic to process and calculate financial metrics.

#### Error Handling and Retries
Robust error handling will be implemented to manage potential downtime or inconsistencies from third-party APIs. 
The system will include retry mechanisms to handle transient errors, ensuring that data fetching and processing can recover from interruptions.

### Assumptions
- Business identifiers are stable and do not change frequently.
- The third-party APIs are reliable, but the system will be designed to handle occasional failures gracefully.
- The simplicity of the current workflow does not necessitate an orchestrator like AWS Step Functions or Apache Airflow. However, should the need arise, AWS Step Functions can be integrated without overhauling the system architecture.
- 

### Data Flow
- Data Fetching: Lambda functions are triggered on a schedule (every 24 hours) to fetch data from third-party APIs using the business identifiers.
- Data Processing: Lambda functions process the fetched data to calculate the required financial metrics.
- Data Ingestion: The processed metrics are stored in DynamoDB, with outdated records being replaced by new ones based on the business ID and year_month.


### Future Considerations
- Should the complexity of data processing increase or the number of integrated platforms grow, introducing a workflow orchestrator like AWS Step Functions or managed Apache Airflow could provide better management of the data pipeline and processing steps.
- In order to better understand the architecture it could have been drawn a diagram with the components used. Due to time constraints and the simplicity of the current approach, it has not been done but if the complexity increases, it could be done in order to improve the documentation.

### Conclusion
The proposed FMS design meets the requirements by providing a robust, scalable, and cost-effective solution for calculating and storing financial metrics for e-commerce businesses. The system's architecture ensures that it is maintainable and extensible, with the capacity to evolve in line with future demands and integration needs.

## Code
### Considerations
- Due to time constraints, only basic unit testing has been included in the `tests` folder. Some comments have been added describing how more robust tests could be developed.
- Some methods have not been implemented as there is not enough data in the provided files.
- As deploying a DynamoDB instance will be out of the scope of the current assignment, it has been created a not implement DynamoDB adapter (`src/adapters/output_adapters/dynamodb_output_adapter.py`).
  - A Console Adapter has been developed otherwise to print the results of the process on the screen.  
- As no SaaS API from which to retrieve the data is available, it has been created a not implement API adapter (`src/adapters/input_adapters/api_input_adapter.py`).
  - A JSON Adapter has been developed otherwise to get the data directly from a file.
### Environment
- Python >=3.8

### Run the project
- Go to the root folder of the project
- Run the following command
```bash
python3 src/main.py
```
- It will output something like:
```
{
  "income": 6960.09,
  "costOfSales": 700,
  "expenses": 1392.06,
  "gross_profit": 6260.09,
  "net_profit": 4868.030000000001,
  "profit_margin": 0.6994205534698547,
  "year": 2022,
  "month": 2,
  "month_key": "2022-02",
  "updated_at": "2022-02-13T00:00:00",
  "detailed_expenses": {
    "Advertising & Marketing": 1083.33,
    "Entertainment-100% business": 18.33,
    "General Expenses": 186.97,
    "Light, Power, Heating": 103.43
  },
  "type": "Profit and Loss Metrics",
  "business_id": "TEST_ID"
}
{
  "assets_breakdown": {
    "Fixed Assets": 4069,
    "Current Assets": 21523.17
  },
  "liabilities_value": 13054.83,
  "liabilities_to_income": 0.10879025,
  "year": 2022,
  "month": 2,
  "month_key": "2022-02",
  "updated_at": "2022-02-05T00:00:00",
  "type": "Balance Sheet Metrics",
  "business_id": "TEST_ID"
}

```
