# Data Engineer coding challenge

## Some data

The Lingokids App generates events that are sent to our API for us to
understand how our users behave. In this exercise we are interested in a
particular type of event called `activity_exit`. This event is triggered when
a user (parent or child) exits one of our activities, either because the
activity is finished or because they decided to leave.

Here is an example of such an event, in JSON:

```json
{
  "event_id": "205f2688-0d60-4afa-9d49-2004af2ee10d",
  "name": "activity_exit",
  "occurred_at": "2021-01-31 23:01:25.295",
  "user_id": "c7b2555c-5a37-46b6-8715-9cc2378f1ee2",
  "child_id": "314874c6-929b-40cb-9ec8-9255fdf78f3a",
  "data": {
    "activity_id": "snow_game",
    "source": "launcher",
    "duration": 232.725,
    "completed": false,
    "collection_id": "lk_collection_winterexplorer",
    "loading_time": 0.887
  },
  "context": {
    "device": {
      "device_id": "129b1f02-644d-4f1d-a99a-89017d588721",
      "brand": "Apple",
      "model": "iPad7,6"
    },
    "os": {
      "name": "iOS",
      "version": "14.2"
    },
    "app": {
      "version": "7.41.0",
      "build": "4457"
    }
  }
}
```
The `data` object in the event contains fields specific to each event type.
Here we can see the following fields:

 * `activity_id`: the id of the activity that the user was playing
 * `source`: the screen in the App from which the user started the activity
 * `duration`: the amount of time the user spent playing the activity
 * `completed`: whether the user finished the activity or left before it was complete
 * `collection_id`: the id of the collection the activity was part of when it was played
 * `loading_time`: the time it took for the activity to load once the user opened it

Our API backend also keeps track of the subscription status of all our users.
For this exercise, we assume that a subscription state moves in one direction
between the following states:

State | Entered when | Description
------|--------------|------------
free  | user registers | The user can play a limited number of activities per day
trial | user starts trial | The user has full access for free for a limited time
subscribed | user doesn't cancel at the end of trial | The user has full access and pays a monthly subscription fee
lapsed | user cancels subscription | The user does not have full access anymore

Based on this, we store for each user a record similar to the following example in JSON:

```json
{
  "user_id": "9097aa48-6be9-453f-9833-9ead1c4adfa9",
  "children_ids": [
    "826d41ee-b99f-4be8-bd7d-f688a7836dd0",
    "8fe0391a-9ca7-4e70-87ea-25ebcc11211a"
  ],
  "country_code": "in",
  "registration_at": "2021-01-12 13:34:37.139000",
  "trial_start_at": "2021-01-12 13:49:37.139000",
  "trial_end_at": "2021-01-19 13:49:37.139000",
  "subscription_start_at": "2021-01-19 13:49:37.139000",
  "subscription_expire_at": "2021-02-18 13:49:37.139000"
}
```

Finally, we also maintain metadata about all the content that has ever been
available in the Lingokids App. An example of activity metadata, in JSON,
looks like the following:

```json
{
  "activity_id": "rainforest_game",
  "name": "Rainforest Game",
  "type": "game",
  "subtype": "hide_and_seek"
}
```

## The challenge

Your task is to process the input raw data and generate an output that can be
used to analyze some engagement metrics. In particular, with the output you will 
generate we want to be able to measure:
 * the number of activities played
 * the time spent playing
 * the most played activities, both in terms of number of times and total duration
 * the completion rate of activities

On top of that:

 * we want to be able to analyze data at daily, weekly, monthly and yearly
   granularity.
 * we want to be able to slice the data by several dimensions:
   - country
   - OS of the device (type and version) and App version
   - subscription status: free, trial, subscribed, lapsed
   - activity type and collection
 * we are not interested in being able to analyze every single event or the
   behaviour of individual users.


You will find in this repository 3 files in
[JSON Lines format](https://jsonlines.org/) that are samples of the 3 datasets
described above.

## Expectations

We expect you to write code that: loads the datasets; transforms them as
necessary; produces one or several datasets that can be used to perform further
analysis.

You are free to use the language and libraries/frameworks that you
prefer.

You can generate your output in the format you find most appropriate and can
assume that we have access to modern querying/processing tools for consuming
them (data warehouse, query engine, database , ...).

We expect you to:

 * spend no more than 4 hours
 * write a solution that we can easily execute on a laptop for evaluation
 * include a Readme that describes your approach, and the assumptions you made
   (if any)
 * write code with the same care you would use in your job
 * include some level of automated testing
 * explain in the Readme how you would scale your solution to handle millions
   of daily events, users and activities

We will evaluate all aspects of your submission, in particular code quality, so avoid spending all your time on just the perfect data processing approach. If your submission meets our expectations you will have time to discuss improvements with us in the following interviews.

If you have any doubt regarding any part of this challenge, do no hesitate to
email us with your questions.

## EXPLANATION: how you would scale your solution to handle millions of daily events, users and activities
 I have choosen a distributed processing framework as `Spark` to be able to scale the solution. In case that the expected volume of data would be similar to the sizes of the files used as an example in this exercise, the solution would be implemented in a more lightweight framework like `Pandas`.

`JSON` files won't be used in case of having volumes of millions of rows, instead and, as data wants to be used for analytical purposes (OLAP) and mostly for aggregations, a columnar format will be used for all the files (output and source files); more precisely, `PARQUET` format will be used due to:
* It's a columnar storage format.
* It has native compatibility with Spark.
* It's compatible with a lot of modern querying/processing tools.

Furhtermore and, to simplify the access to the data by different granularity, the output dataset would be partitioned by `year, month and day`. Doing that, the entire dataset wouldn't have to be read every time that a query filtering by one of these values is executed. If other values (EX: Country, Subscription status...) are widely used in other analyst's queries, then different versions of the same output dataset could be created with different partitions.

As the data is being generated in real time (there is a JSON file called `events`), the ETL pipeline could be improved with the addition of `Stream processing`. In the current solution, the data is processed in batch format, the generated job could be triggered every time that new data is detected in a certain path, but if a distributed queue (like `Kafka`) is used, data could be read in real time (instead of generate files, the data would be pushed to a Kafka queue) and the output dataset could also be updated in real time too, so analysts will always have the most updated version of the output dataset. With that approach, no trigger is needed for the job as it will always be running and reading new data from the Kafka queue.


## EXPLANATION: My approach and assumptions made
### Introduction
Specific decissions and more technical comments can be found in the code.
As it's stated in previous section, the framework used has been `Spark` to simplify the usage of the same code in case that the volume of data increases. Python has been chosen as language due to:
* Easy to understand.
* Widely used in Data engineering.
* Integration with Spark (`pyspark`)

In this case, three Python files has been generated:
* `common_methods.py` with methods used in more than one file.
* `ETL_process.py` with the ETL functionality to read the input datasets, transform them and generate the new dataset.
* `calculations.py` with calculations of the metrics described above. 

A config file called `config.properties` has been used to store all the values used as parameters in the files. 

### Approach
As the metrics to be extracted from the output dataset depend on the combination of the three input datasets,a single output dataset has been generated by combining those three input datasets.

For each entry in `users` dataset it can be more than one `child_id`, that's why it is necessary to explode those rows in order to generate one row per each `child_id` so it will be possible to join that dataset with `events` dataset. Furthermore, the subscription status is not explicitly described in the data, so it is necessary to calculate it as described above.

For each entry in `events` dataset it is necessary to take exclusively the columns that could be used in further calculations (to avoid generating a very large dataset), and some calculated fields are added to facilitate the analysis of the data by the fields described above.

Finally, the result of the join between `users` dataset and `events` dataset is joined with `activities` dataset by `activity_id` to get more information about the activities described in the events.

Before persisting the generated dataset, some calculated columns are added to simplify dealing with the output data (saving costs and analyst's time):

* `time_spent_playing` -> Average duration of each activity.
* `number_of_times_played` -> Number of times that each activity is played.
* `number_completed_by_value` -> Number of times that each activity is played and completed or played and not completed.
* `percentage_by_completion_status` -> Previous column is used to calculate the completion percentage by `completed` field ('true' or 'false'). The field contains the number of times a given activity has been completed (or not) as a percentage. The value will vary depending on the value of the 'completed' field in each row.

### Assumptions made
* No outliers has been identified, so no methods to deal with them have been included.
* Data quality is assumed in the input data sets (e.g., a given user cannot be in "test" and "expired" status at the same time).
* No automated testing tool has been included due to lack of time. I would be glad to describe possible solutions in upcoming interviews.