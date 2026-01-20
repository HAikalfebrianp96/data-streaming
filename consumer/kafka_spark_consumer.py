from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("MoviesStreamingPipeline") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "streaming-movies") \
    .option("startingOffsets", "earliest") \
    .load()

schema = StructType([
    StructField("show_id", StringType()),
    StructField("type", StringType()),
    StructField("title", StringType()),
    StructField("director", StringType()),
    StructField("cast", StringType()),
    StructField("country", StringType()),
    StructField("date_added", StringType()),
    StructField("release_year", StringType()),
    StructField("rating", StringType()),
    StructField("duration", StringType()),
    StructField("listed_in", StringType()),
    StructField("description", StringType()),
    StructField("platform", StringType())
])

json_df = df.select(
    from_json(col("value").cast("string"), schema).alias("d")
).select("d.*")

df_clean = json_df.drop("date_added") \
    .withColumn("listed_in", regexp_replace("listed_in", "[&-]", ","))

df_exploded = df_clean \
    .withColumn("category", explode(split("listed_in", ","))) \
    .withColumn("category", trim(col("category")))

df_final = df_exploded \
    .withColumn("duration_value", regexp_extract("duration", r"(\d+)", 1).cast("int")) \
    .withColumn(
        "duration_type",
        when(col("duration").contains("min"), "Minutes")
        .when(col("duration").contains("Season"), "Seasons")
    )

def write_to_sqlserver(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:sqlserver://sqlserver:1433;databaseName=master") \
        .option("dbtable", "moviesproject") \
        .option("user", "sa") \
        .option("password", "YourStrong@Passw0rd") \
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
        .mode("append") \
        .save()

df_final.writeStream \
    .foreachBatch(write_to_sqlserver) \
    .option("checkpointLocation", "/tmp/movies_checkpoint") \
    .start() \
    .awaitTermination()
