# Author: Iván Gómez
# Last modification: 01-09-2021
# TO-DO: Use deequ to implement automatic testing and to ensure data quality.
"""ETL Process

Script that fulfil expectations described in repo:
https://github.com/lingokids/lk-coding-exercise-data-engineer-Ivan-Gomez
- Loads the datasets.
- Transforms them as necessary.
- Produces one or several datasets that can be used to perform further analysis.

"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from common_methods import read_properties_file


# GLOBAL VARIABLES
spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

# READ PARAMETERS
config = read_properties_file("config.properties")
activities_path = config.get("dev.source", "path_activities")
events_path = config.get("dev.source", "path_events")
users_path = config.get("dev.source", "path_users")
output_path = config.get("dev.output", "path_output")


# READ AND TRANSFORM DATASETS
activities = spark.read.format("json").load(activities_path) \
    .select("activity_id", "name") \
    .withColumnRenamed("name", "activity_name")  # Renamed to avoid misunderstandings

# Columns added to allow to analyze the data easier (not having to deal directly with the timestamp).
events = spark.read.format("json").load(events_path) \
    .select(F.col("child_id"), F.col("context.app.version").alias("app_version"),
            F.col("context.os.name").alias("os_name"), F.col("context.os.version").alias("os_version"),
            F.col("data.activity_id"), F.col("data.collection_id"), F.col("data.duration"), F.col("data.completed"),
            F.col("occurred_at")) \
    .withColumn("day_of_year_occurred_at", F.dayofmonth("occurred_at")).withColumn("week_of_year_occurred_at",
                                                                                   F.weekofyear("occurred_at")) \
    .withColumn("month_occurred_at", F.month("occurred_at")) \
    .withColumn("year_occurred_at", F.year("occurred_at"))

# Each row with more than one 'child_id' is exploded to generate as much as new rows as values in 'children_ids' field
users = spark.read.format("json").load(users_path).withColumn("child_id", F.explode("children_ids")) \
    .withColumn("subscription_status", \
                # Status of subscription is calculated using the process described in repo.
                F.when((F.col("subscription_start_at").isNull()) & (F.col("trial_start_at").isNull()),
                       F.lit("FREE")) \
                .otherwise( \
                    F.when((F.col("trial_end_at").isNotNull()) & (F.col("trial_end_at") > F.current_timestamp()),
                           F.lit("TRIAL"))
                        .otherwise(F.when((F.col("subscription_expire_at").isNotNull())
                                          & (F.col("subscription_expire_at") > F.current_timestamp()), "SUBSCRIBED") \
                                   .otherwise("ELAPSED")
                                   )
                )
                ) \
    .select("child_id", "country_code", "subscription_status")

# COMBINE (JOIN) DATASETS
joined_df = events.join(users, events["child_id"] == users["child_id"]) \
    .drop(users["child_id"]) \
    .join(activities, events["activity_id"] == activities["activity_id"]) \
    .drop(activities["activity_id"])

# FINAL TRANSFORMATIONS TO ADD CALCULATED FIELDS
"""
Calculated fields added to simplify dealing with the output data (saving costs and analyst's time):

-time_spent_playing-> Average duration of each activity.

-number_of_times_played-> Number of times that each activity is played.

-number_completed_by_value-> Number of times that each activity is played and completed or played and not completed.

-percentage_by_completion_status -> Previous column is used to calculate the completion percentage by 'completed' field
  ('true' or 'false'). The field contains the number of times a given activity has been completed (or not)
  as a percentage. The value will vary depending on the value of the 'completed' field in each row.
"""

windowSpec_total_activities = Window.partitionBy("activity_id")
windowSpec_total_completed = Window.partitionBy("activity_id", "completed")

final_completed = joined_df \
    .withColumn("time_spent_playing", F.round(F.mean("duration").over(windowSpec_total_activities), 2)) \
    .withColumn("number_of_times_played", F.count("*").over(windowSpec_total_activities)) \
    .withColumn("number_completed_by_value", F.count("*").over(windowSpec_total_completed)) \
    .withColumn("percentage_by_completion_status",
                F.round((F.col("number_completed_by_value") / F.col("number_of_times_played")) * 100, 2)) \
    .drop("number_completed_by_value")  # Not needed anymore

# WRITE OUTPUT DATAFRAME (as volume is not big, all data is being written into one single file)
final_completed.coalesce(1) \
    .write.format("json").save(output_path)