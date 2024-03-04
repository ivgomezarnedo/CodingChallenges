# Coding Assessment - Iván Gómez Arnedo

## 1. How to run the code
In order to run the code, you need:
- **Python 3.9** installed in your computer (or with a virtual environment). You can download it from [here](https://www.python.org/downloads/release/python-3917/).
- **user_agents** library.
    ```bash
    pip install user_agents
    ``` 
- A multi-line JSON file with name `sample_orders_transformed.json.gz` in 'files/'
  
Once you have satisfied the previous requirements, you can run the code that is going to download and process the data. To do so, you need to execute the following command in the root folder of the project:
```bash
python3 src/coding_assesment.py
```

This will run the code and print the logging to the console. Once the process is finished, you will see the following message:
```
INFO:root:Successfully completed!
```

And a new file with name `sample_orders_transformed.json.gz` will be created under `files/`.

## 2. How to run the tests
In order to run the code, you need:
- **pytests** library:
```bash
pip install pytest
```
Once you have satisfied the previous requirements, you can run the tests:
  ```bash
  pytest src/tests
  ```

And you should see something like:
```
collected 2 items                                                                      

src/tests/test_coding_assesment.py ..                                            [100%]

================================== 2 passed in 0.12s ===================================
``` 

## 3. How it could have been improved
Due to time constraints, there are some things that could have been improved:
- Adding tests for Reading/writing with gzipped JSON Lines.
- Adding tests for Handling data quality issues
- Passing parameters as `input_file_path`and `output_file_path` as command arguments.
- Better exception handling of cases like when the file to process is not found or is not in the expected format.