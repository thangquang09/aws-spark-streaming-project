<h1>AWS SPARK STREAMING PROJECT</h1>

![Background](background.png)

- [1. Project Overview](#1-project-overview)
- [2. Project](#2-project)
  - [2.1. Multi-format Data Ingestion:](#21-multi-format-data-ingestion)
  - [2.2. Unified Data Schema:](#22-unified-data-schema)
  - [2.3. Data Lake Storage with AWS S3:](#23-data-lake-storage-with-aws-s3)
  - [2.4. Optional Data Cataloging and Querying with AWS Glue and Athena:](#24-optional-data-cataloging-and-querying-with-aws-glue-and-athena)
  - [2.5. Dockerized Spark Cluster:](#25-dockerized-spark-cluster)
  - [2.6. Real-time Processing with Spark Streaming:](#26-real-time-processing-with-spark-streaming)
- [3. Technology Stack](#3-technology-stack)
- [5. Architecture](#5-architecture)
- [6. Getting Started](#6-getting-started)
  - [6.1. Prerequisites](#61-prerequisites)
  - [6.2. Instructions](#62-instructions)
  - [6.3. Generating Streaming Data](#63-generating-streaming-data)


## 1. Project Overview

This project is designed to build a data pipeline for collecting, processing, and storing job data from various sources and formats. By leveraging the power of Apache Spark for distributed data processing, this pipeline reads job listings in multiple formats (text, JSON, and CSV), unifies the data schema, and loads it into a data lake on AWS S3. Using AWS Glue and Athena for ETL and querying is optional but recommended for streamlined data querying and management of the data catalog.

The pipeline is packaged and orchestrated in Docker, creating a simulated Spark cluster environment with a master node and two worker nodes. This setup allows for scalable and efficient processing, closely replicating a production environment.

## 2. Project 

### 2.1. Multi-format Data Ingestion:

The pipeline is capable of reading job data from different formats: text files, JSON, and CSV.
Each data source is processed and converted to a unified schema, facilitating downstream aggregation and analysis.

### 2.2. Unified Data Schema:

All ingested job data adheres to a standard schema, ensuring consistency and enabling seamless data transformation and storage. The schema for the job data is as follows:

```python
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
```

### 2.3. Data Lake Storage with AWS S3:

The processed data is stored in a data lake on AWS S3, providing a cost-effective, scalable, and durable storage solution for large datasets.
Using S3 as the data lake is mandatory in this project, as it serves as the primary storage for both raw and processed data, allowing efficient access and future transformations.

### 2.4. Optional Data Cataloging and Querying with AWS Glue and Athena:

While not required, it is recommended to use AWS Glue to catalog the data stored in S3 and enable easy querying and analysis with AWS Athena or other SQL-compatible services. Glue can automate schema detection and data cataloging, which is particularly beneficial for ETL tasks and data analysis. Athena, in turn, allows for SQL-based queries on the cataloged data without the need for additional infrastructure setup.

### 2.5. Dockerized Spark Cluster:

The entire setup is containerized using Docker, enabling easy deployment and replication across different environments.
The Docker configuration creates a Spark cluster with one master node and two worker nodes, simulating a real-world distributed processing environment. This setup allows for horizontal scalability and high-performance processing of large datasets.

### 2.6. Real-time Processing with Spark Streaming:

The pipeline is designed to support Spark Streaming, enabling real-time ingestion and processing of data as new job listings become available.
This feature allows for continuous updates to the data lake and real-time insights into job market trends.

## 3. Technology Stack

- **Apache Spark:** For distributed data processing and streaming.
- **AWS S3:** Data lake storage solution, providing scalability and durability.
- **AWS Glue:** Optional data catalog and ETL service for schema management and query facilitation.
- **AWS Athena:** Optional serverless query service for SQL-based data analysis.
- **Docker:** To package the application into containers and simulate a Spark cluster environment with two worker nodes.
- **Python:** The primary programming language for data processing and pipeline orchestration.

## 5. Architecture

- **Data Ingestion:** Spark reads job data from different sources/formats (text, JSON, CSV) and applies a schema to unify the data structure.

- **Data Processing:** Spark processes and transforms the data according to the specified schema, ensuring consistency across sources. Additional transformations and cleansing operations can be applied as necessary.

- **Data Storage:** The processed data is stored in a data lake on AWS S3, creating a centralized repository for all job-related data.

- **Optional Data Querying and Cataloging:** AWS Glue catalogs the data in S3, enabling efficient querying and analysis using AWS Athena or other compatible tools.

- **Real-time Processing:** Spark Streaming enables real-time ingestion and processing, allowing the pipeline to handle continuous data flows and update the data lake in near real-time.

## 6. Getting Started

### 6.1. Prerequisites

- **Docker:** Ensure Docker is installed on your local machine to run the Spark cluster.
- **AWS Account:** Necessary for setting up S3 and optionally for AWS Glue and Athena.

### 6.2. Instructions

1. Clone the Repository: Clone the project repository to your local machine.
    ```bash
    git clone https://github.com/thangquang09/aws-spark-streaming-project
    cd aws-spark-streaming-project
    ```

2. Set Up .env File: Create a `.env` file in the project root directory to store AWS credentials and other configuration settings.
    ```bash
    AWS_ACCESS_KEY_ID=<your-access-key>
    AWS_SECRET_ACCESS_KEY=<your-secret-key>
    S3_BUCKET=<your-s3-bucket>
    ```
3. Start the Dockerized Spark Cluster: Use Docker Compose to start the Spark master and worker nodes.
    ```bash
    docker compose up -d
    ```

4. Submit Spark Project: using docker exec to submit main.py
    ```bash
    docker exec -it <spark_master_container> spark-submit --packages org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk:1.11.469,com.fasterxml.jackson.core:jackson-databind:2.15.3 jobs/main.py
    ```
    Spark Master Container can be searched using this command: `docker ps`.

### 6.3. Generating Streaming Data

To simulate streaming data ingestion, you can add new files to the `data` directory using the following command:

```bash
python generator.py -t <file_type> -n <number_of_files_to_load>
```

- `<file_type>`: Specify the file type (`json`, `csv`, or `txt`) to generate.
- `<number_of_files_to_load>`: Number of files to generate and load into the folder.

Upon cloning the project, a few dozen files are preloaded and awaiting processing by Spark Streaming. If all preloaded files have been processed and you wish to restart the simulation, follow these steps:

1. **Clear Existing Files**: Delete the processed files in `data/<file_type>` directories under `data/` to reset the input folders.
   
2. **Clear Checkpoints and Data on S3**: Remove all checkpoints and output data in the designated S3 bucket. This will clear the state of the stream to allow fresh data processing.

This reset ensures that you can repeatedly test the streaming pipeline without conflicts from previously processed files.