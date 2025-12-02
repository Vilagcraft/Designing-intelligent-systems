from pyspark.sql import SparkSession
from pyspark.sql.functions import length, col
import pyspark.sql.functions as F
from pyspark.sql.types import StringType

def main(input_path, output_path):
    spark = SparkSession.builder.appName("rureviews_preprocess").getOrCreate()
    df = spark.read.csv(input_path, header=True, multiLine=True, escape="\"")
    df = df.withColumn("char_len", length(col("text")))
    df = df.filter(col("char_len") > 15)
    df = df.dropDuplicates(["text"])
    df.write.mode("overwrite").parquet(output_path)
    spark.stop()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: spark-submit src/preprocessing/spark_preprocess.py <input_csv> <output_parquet>")
    else:
        main(sys.argv[1], sys.argv[2])