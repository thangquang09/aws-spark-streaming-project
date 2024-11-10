from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DateType
from pyspark.sql.functions import udf
import os
from dotenv import load_dotenv

from udf_utils import *

def define_udfs():
    return {
        'extract_job_title_udf': udf(extract_job_title, StringType()),
        'extract_salary_start_udf': udf(extract_salary_start, StringType()),
        'extract_salary_end_udf': udf(extract_salary_end, StringType()),
        'extract_experience_udf': udf(extract_experience, StringType()),
        'extract_submission_deadline_udf': udf(extract_submission_deadline, DateType()),
        'extract_job_description_udf': udf(extract_job_description, StringType()),
        'extract_job_requirements_udf': udf(extract_job_requirements, StringType()),
        'extract_benefits_udf': udf(extract_benefits, StringType()),
        'extract_company_address_udf': udf(extract_company_address, StringType()),
    }

if __name__ == "__main__":
    load_dotenv()
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    spark = (SparkSession.builder.appName("AWS_Spark_Streaming")
        .config('spark.jars.packages',
                'org.apache.hadoop:hadoop-aws:3.3.1,'
                'com.amazonaws:aws-java-sdk:1.11.469')
        # .config('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
        # .config('spark.hadoop.fs.s3a.access.key', AWS_ACCESS_KEY_ID)
        # .config('spark.hadoop.fs.s3a.secret.key', AWS_SECRET_ACCESS_KEY)
        # .config('spark.hadoop.fs.s3a.aws.credentials.provider',
        #         'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
        .getOrCreate()
    )

    text_dir = 'file:///home/thangquang/Documents/CODE/aws-spark-streaming-project/data/text'
    csv_dir = 'file:///home/thangquang/Documents/CODE/aws-spark-streaming-project/data/csv'
    json_dir = 'file:///home/thangquang/Documents/CODE/aws-spark-streaming-project/data/json'

    data_schema = StructType([
        StructField("job_title", StringType(), True),
        StructField("salary_start", StringType(), True),
        StructField("salary_end", StringType(), True),
        StructField("years_of_experience", StringType(), True),
        StructField("submission_deadline", DateType(), True),
        StructField("job_description", StringType(), True),
        StructField("job_requirements", StringType(), True),
        StructField("benefits", StringType(), True),
        StructField("company_address", StringType(), True),
    ])

    udfs = define_udfs()

    text_df = spark.readStream\
    .format("text")\
    .option("wholetext", True)\
    .load(text_dir)

    json_df = spark.readStream.json(json_dir, schema=data_schema, multiLine=True)

    text_df = text_df.withColumn("job_title", udfs["extract_job_title_udf"]('value'))
    text_df = text_df.withColumn("salary_start", udfs["extract_salary_start_udf"]('value'))
    text_df = text_df.withColumn("salary_end", udfs["extract_salary_end_udf"]('value'))
    text_df = text_df.withColumn("years_of_experience", udfs["extract_experience_udf"]('value'))
    text_df = text_df.withColumn("submission_deadline", udfs["extract_submission_deadline_udf"]('value'))
    text_df = text_df.withColumn("job_description", udfs["extract_job_description_udf"]('value'))
    text_df = text_df.withColumn("job_requirements", udfs["extract_job_requirements_udf"]('value'))
    text_df = text_df.withColumn("benefits", udfs["extract_benefits_udf"]('value'))
    text_df = text_df.withColumn("company_address", udfs["extract_company_address_udf"]('value'))
    
    final_text_df = text_df.select("job_title",
                                    "salary_start",
                                    "salary_end",
                                    # "years_of_experience",
                                    # "submission_deadline",
                                    # "job_description",
                                    # "job_requirements",
                                    # "benefits",
                                    # "company_address",
                                )

    final_json_df = json_df.select("job_title",
                                    "salary_start",
                                    "salary_end",
                                    # "years_of_experience",
                                    # "submission_deadline",
                                    # "job_description",
                                    # "job_requirements",
                                    # "benefits",
                                    # "company_address",
                                )

    query = (
        final_json_df.writeStream
        .outputMode('append')
        .format('console')
        .option('truncate', False)
        .start()
    )

    query.awaitTermination()