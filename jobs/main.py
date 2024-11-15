from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DateType
from pyspark.sql.functions import udf
from functools import reduce
import os

from dotenv import load_dotenv

from udf_utils import *
      

def define_udfs():
    # return all udf to extract every single field in the whole text file
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
    # load ENVIRONMENT VARIABLES
    load_dotenv()
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET = os.getenv("S3_BUCKET")
    # create SparkSession and Config
    spark = (SparkSession.builder.appName("AWS_Spark_Streaming_Project")
        .master("spark://spark-master:7077")
        .config('spark.jars.packages',
                'org.apache.hadoop:hadoop-aws:3.3.1,'
                'com.amazonaws:aws-java-sdk:1.11.469')
        .config('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
        .config('spark.hadoop.fs.s3a.access.key', AWS_ACCESS_KEY_ID)
        .config('spark.hadoop.fs.s3a.secret.key', AWS_SECRET_ACCESS_KEY)
        .config('spark.hadoop.fs.s3a.aws.credentials.provider',
                'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
        .getOrCreate()
    )

    # Directory to raw data with different types
    text_dir = 'data/txt'
    csv_dir = 'data/csv'
    json_dir = 'data/json'

    # Define Data Schema For Consistency
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

    # Load all udfs
    udfs = define_udfs()
    
    # Read Stream with TEXT FILE
    text_df = (spark.readStream
        .format("text")
        .option("wholetext", True)
        .option("pathGlobFilter", "*.txt")
        .load(text_dir)
    )

    # Read Stream with JSON FILE
    json_df = (spark.readStream
        .format("json")
        .option("pathGlobFilter", "*.json")
        .schema(data_schema)
        .option("multiLine", True)
        .load(json_dir)
    )


    # Read Stream with CSV FILE
    csv_df = (spark.readStream
        .format("csv")
        .option("pathGlobFilter", "*.csv")
        .schema(data_schema)
        .option("header", "true")
        .load(csv_dir)
    )



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
                                    "years_of_experience",
                                    "submission_deadline",
                                    "job_description",
                                    "job_requirements",
                                    "benefits",
                                    "company_address",
                                )

    final_json_df = json_df.select("job_title",
                                    "salary_start",
                                    "salary_end",
                                    "years_of_experience",
                                    "submission_deadline",
                                    "job_description",
                                    "job_requirements",
                                    "benefits",
                                    "company_address",
                                )

    final_csv_df = csv_df.select("job_title",
                                    "salary_start",
                                    "salary_end",
                                    "years_of_experience",
                                    "submission_deadline",
                                    "job_description",
                                    "job_requirements",
                                    "benefits",
                                    "company_address",
                                )

    # --------- concatenate all data sources -------------
    dfs = [final_text_df, final_json_df, final_csv_df]
    final_data_stream = reduce(lambda df1, df2: df1.union(df2), dfs)

    # Write Streaming Data
    def streamWriter(input, checkpointFolder, output):
        return (
            input.writeStream.
            format('parquet')
            .option('checkpointLocation', checkpointFolder)
            .option('path', output)
            .outputMode('append')
            .trigger(processingTime='5 seconds')
            .start()
        )

    query = streamWriter(
        input=final_data_stream, 
        checkpointFolder=f's3a://{S3_BUCKET}/checkpoints/', 
        output=f's3a://{S3_BUCKET}/data/spark_stream'
    )

    query.awaitTermination()

    spark.stop()