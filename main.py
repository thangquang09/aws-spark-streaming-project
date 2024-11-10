from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    spark = SparkSession.builder.appName("AWS_Spark_Streaming")\
        .config('spark.jars.packages',
                'org.apache.hadoop:hadoop-aws:3.3.1,'
                'com.amazonaws:aws-java-sdk:1.11.469')\
        .config('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')\
        .config('spark.hadoop.fs.s3a.access.key', AWS_ACCESS_KEY_ID)\
        .config('spark.hadoop.fs.s3a.secret.key', AWS_SECRET_ACCESS_KEY)\
        .config('spark.hadoop.fs.s3a.aws.credentials.provider',
                'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')\
        .getOrCreate()

    text_dir = 'file:///home/thangquang/Documents/CODE/aws-spark-streaming-project/data/text'
    csv_dir = 'file:///home/thangquang/Documents/CODE/aws-spark-streaming-project/data/csv'

    data_schema = StructType([
        StructField("job_title", StringType(), True),
        StructField("salary", StringType(), True),
        StructField("job_title", StringType(), True),
        StructField("job_title", StringType(), True),
        StructField("job_title", StringType(), True),
    ])
    
        