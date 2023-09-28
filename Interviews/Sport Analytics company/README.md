# Sport Assessment - Iván Gómez Arnedo
## 1. Introduction
This repository contains the code for the Sport Analytics company assessment. The code is written in Python 3.9 and it is divided in two main folders: `src` and `files`. The first one contains the code for the assessment and the second one contains the SQL files with the answers to the questions (It's also used as the default folder to store the files to download). The code is structured as follows:
- `src`:
    - `main.py`: Main file of the assessment. It contains the code for the `main` function, which is the one that is executed when the program is run.
    - `data_process.py`: Contains the methods to process each file and to store it into the DB.
    - `utils`: 
      - `db_methods.py`: Contains the methods to interact with the DB.
      - `file_methods.py`: Contains the methods to download the files and to unzip them.

### Data Model
![image](https://i.imgur.com/KHsW0NM.png)

ADD MORE COMMENTS TO THE ANSWERS.

## 2. How to run the code
In order to run the code, you need:
- Python 3.9 installed in your computer (or with a virtual environment). You can download it from [here](https://www.python.org/downloads/release/python-3917/). 
- SQLITE3. You can download it from [here](https://www.sqlite.org/download.html). If you are using Ubuntu (as me :D), you can install it by running the following command in a terminal: `sudo apt install sqlite3`.
    - To create the DB you can run in a terminal the following command:
    ```bash
    sqlite3 files/db/cricsheet.db ".quit"
    ```
    - Once you have created the DB, to create the Data Model to be used, you can run the following command in the root folder of the repository:
    ```bash
    sqlite3 files/db/cricsheet.db < files/db/sql/data_model.sql
    ```
  
Once you have satisfied the previous requirements, you can run the code that is going to download and process the data. To do so, you need to execute the following command in the root folder of the repository:
```bash
python3 src/main.py
```

This will run the code and print the logging to the console. You can check the status of the process and check how many files have been processed. Once the process is finished, you will see the following message:
```
INFO:root:Process finished successfully
```

PD : Some arguments can be passed to the command (although it's recommended to run it with the default parameters). To see the list of arguments, you can run the following command:
```bash
python3 src/main.py --help
```

## 3. Answers to the questions
### Question 1. 
#### We don’t expect you to have any cricket knowledge and that is not a requirement to ace this assessment. But we understand that familiarity with cricket may vary from one candidate to the next so we would like to know how you would rate your knowledge of cricket from 1 to 5, where 1 is basically no knowledge (like you had never seen or read anything about the sport until the days before this assessment) and 5 is highly knowledgeable (you watch matches regularly and have a jersey for the Rajasthan Royals in your closet, for example).
I would say a number between 1 and 2. I have never watched a cricket match and I didn't even know the rules of the game. I have to say that I have enjoyed watching the [Netflix’s Explained: Cricket](https://www.youtube.com/watch?v=NZGLHdcw2RM).
### Question 2.
#### a) The win records (percentage win and total wins) for each team by year and gender, excluding ties, matches with no result, and matches decided by the DLS method in the event that, for whatever reason, the planned innings can’t be completed.
To get the win records and after running all the previous code, you can run the following command in the root folder of the repository:
```bash
sqlite3 -header  files/db/cricsheet.db < files/db/sql/question_2_a.sql
```
##### Expected result (first row as header):
![image1](https://i.imgur.com/ERkfbQN.png)

#### b) Which male and female teams had the highest win percentages in 2019?
To get the highest win percentages and after running the previous SQL script, you can run the following command in the root folder of the repository:
```bash
sqlite3 -header  files/db/cricsheet.db < files/db/sql/question_2_b.sql
```
##### Expected result (first row as header):
![image2](https://i.imgur.com/yCBL7jd.png)

#### c) Which players had the highest strike rate as batsmen in 2019? (Note to receive full credit, you need to account for handling extras properly.)
To get the highest strike rates, you can run the following command in the root folder of the repository:
```bash
sqlite3 -header  files/db/cricsheet.db < files/db/sql/question_2_c.sql
```
Only the top10 players are shown in the result. If you want to see all the players, you can remove the `LIMIT 10` from the SQL script. Strike rate is calculated as the number of runs (`batter_runs` because doesn't contain the extras) divided by the number of balls faced.
##### Expected result (first row as header):
![image3](https://i.imgur.com/w2WY7nF.png)

### Question 3.
#### Please provide a brief written answer to the following question. The coding assessment focused on a batch backfilling use case. If the use case was extended to required incrementally loading new match data on a go-forward basis, how would your solution change?
-  **Delta execution**: The solution needs to be able to identify the new files that need to be processed. This can be done by querying the DB to get the latest matches that have been processed, then the date of these matches will be compared with the current date to get the files from the [cricsheet](https://cricsheet.org/) website (as, for example, the matches added in the latest 2 days can be downloaded from the following [URL](https://cricsheet.org/downloads/recently_added_2_json.zip)).
   - As it's not clear the exact point in time in which they update the matches, it could be a good practice to download more matches than the ones that are going to be processed. For example, if the process is going to be executed every day, it could be a good practice to download the matches from the last 3 days.
   - The process is structured in that way, because the methods to process the files could be used to process the files in a batch or in a delta execution.
- **Schedule the process**: The process needs to be scheduled to run with a certain frequency. This can be done by using a CRON job or by using a scheduler like [Airflow](https://airflow.apache.org/).
   - [AWS Lambda](https://aws.amazon.com/lambda/) could be used to run and schedule the process. The SQLITE DB will be downloaded from S3 on every Lambda run and it will be uploaded again to S3 when the process finishes.
- **Clarify match updates**: It's not clear how the matches are updated in the [cricsheet](https://cricsheet.org/) website. If the matches are updated, the solution needs to be able to identify the matches that have been updated and update the data in the DB. 

## 4. How it could have been improved
Due to time constraints (`"This assessment is expected to take approximately 3-6 hours"`), there are some things that could have been improved:
- **Containerize the application using Docker**. This would make it easier to run the code in different environments.
- **Add unit tests**. Due to time constraints, I have not structured and persisted the tests that I have used. Adding properly structured unit tests would make the code more robust.
  -  I have prioritized the code and documentation over the tests, as I think that is going to be more useful for the assessment.
- **Use [AIOSQLite](https://aiosqlite.omnilib.dev/en/latest/?badge=latest) to make the code asynchronous**. This would make the code faster, as it would be able to run multiple queries at the same time.
- **Create dataclasses for the [cricsheet](https://cricsheet.org/) data used**. This would make the code more readable and easier to maintain.

## 5. Decisions made
- **Innings Table**: Whether to include an Innings table in the database schema was considered. The decision hinges on the specific use case and the queries to be supported. For the current requirements, including team win records by year and gender, highest win percentages, and highest strike rates, innings-level data isn't strictly necessary. However, to support more detailed queries or to preserve the original data's granularity, an Innings table was included.
- **Match Player Table**: A Match Player table was included in the schema. This decision was made to ensure the flexibility and future-proofing of the database schema, enabling it to handle potential future requirements or use cases
- **Player IDs**: The players were not assigned internal IDs in the database, as the dataset already provided unique identifiers for each player.
- **Unique Team IDs**: The teams were assigned unique IDs in the database, created based on each team's name and gender. This decision was made due to the lack of unique identifiers for teams in the dataset.


