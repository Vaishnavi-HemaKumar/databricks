from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import DoubleType

# Initialize Spark session
spark = SparkSession.builder.appName("CarDataETL").getOrCreate()

# S3 paths
input_path = "s3://tiger-devops-dac-aws/data/auto-data.csv"
output_path = "s3://tiger-devops-dac-aws/output/filtered_cars"

# Read the data from the S3 bucket
car_data_df = spark.read.csv(input_path, header=True, inferSchema=True)

# Ensure PRICE is in correct numeric format
car_data_df = car_data_df.withColumn("PRICE", col("PRICE").cast(DoubleType()))

# Filter cars with a price greater than $10,000

filtered_df = car_data_df.filter(col("PRICE") > 10000).persist()

# Aggregate results: Count the number of cars per MAKE
aggregated_df = filtered_df.groupBy("MAKE").count()

# Show the results
aggregated_df.show()

# Write the processed data back to S3
aggregated_df.write.csv(output_path, header=True, mode="overwrite")

print(f"✅ Processed data written to {output_path}")
# Stop Spark after processing
if spark:
    spark.stop()
