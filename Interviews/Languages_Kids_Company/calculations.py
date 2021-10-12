# Author: Iván Gómez
# Last modification: 01-09-2021
""" CALCULATIONS

According to the repository, the things that have to be able to measure are:

-The number of activities played
-The time spent playing
-The most played activities, both in terms of number of times and total duration
-The completion rate of activities

All these things have been calculated in this file using the previously generated output file.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from common_methods import read_properties_file

# GLOBAL PARAMETERS
spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext
config = read_properties_file("config.properties")
output_path = config.get("dev.output", "path_output")

# LOAD DATASET
final_completed = spark.read.format("json").load(output_path)

# CALCULATIONS
print("Number of activities played: {0}".format(final_completed.count()))

print("Total time spent playing: {0}".format(final_completed.agg(F.round(F.sum("duration"), 2)).take(1)[0][0]))

print("TOP 10 activities by number of times played:")
final_completed \
    .select("activity_id", "activity_name", "number_of_times_played") \
    .distinct() \
    .orderBy(F.col("number_of_times_played").desc()) \
    .show(10)

print("TOP 10 activities by duration:")
final_completed \
    .select("activity_id", "activity_name", "time_spent_playing") \
    .distinct() \
    .orderBy(F.col("time_spent_playing").desc()) \
    .show(10)

""" How field 'completion_percentage' its being calculated:
Two rows with same 'activity_id' but with different 'completed' field will have different values for the field
'percentage_by_completion_status' (Rows with value 'true' in that field will contain the percentage of completion
for a certain activity, meanwhile, rows with value 'false' will have the percentage of non-completion for thE activity).
What we are calculating in field 'completion_percentage' is only the percentage of times that a certain activity has 
been completed, so we have to remove the rows that contain information for non-completed activities and, 
if a certain activity has been never completed (100% appearances of the activity with"completed" value ='false'), 
that activity completion percentage is being set to 0.

"""
print("Activities ordered by completion rate:")
final_completion_rate = final_completed \
    .withColumn("completion_percentage", F.when((F.col("completed") == "false") &
                                                (F.col("percentage_by_completion_status") == 100), 0)
                .otherwise(F.col("percentage_by_completion_status"))) \
    .filter("completed='true' or completion_percentage=0") \
    .select("activity_id", "activity_name", "completion_percentage") \
    .distinct() \
    .orderBy(F.col("completion_percentage").desc())

final_completion_rate.show()
