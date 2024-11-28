# Project: S3 to Redshift ETL Pipeline

## Overview
This project involves the automation of data fetching from an S3 bucket, transforming the data, and loading it into an
Amazon Redshift database. The ETL pipeline leverages AWS Glue for schema inference and transformation, 
and AWS Lambda is used to trigger the ETL process when new files are uploaded to the S3 bucket.
---------------------------------------------------------------------------------------------------------------------------------------------
## EXPLANATION FOR FILES IN GIT:
   -The PNG files uploaded shows the process done in each AWS services to create a pipeline.
       -S3_bucket_dataset.png --- Dataset stored in the S3 bucket.
       -ETL_JOB_GRAPH.png --- ETL job Graph is created having S3 as source and Redshift as Destination and Changing schema , drop duplicates                               as transformation.
       -Successful_CRAWLER_RUN.png --- A crawler is creasted and successfully fetched the schema of dataset in s3 bucket.
       -S3_Bucket_added_as_trigger.png --- A lamda function is created and s3 bucket is added as a trigger.
       -Successful_run_of_ETLJOB.png --- The successful run of ETL JOB after lambda trigers the etl job when a new file uploaded in s3 bucket
       -Cloud_logs_For_triggering_both_Crawler and ETLjob.png --- Shows the log values while the lambda function runs to trigger crawler and                                                                   Etl job.
       -VALUES_STORED_IN_REDSHIFT_BY_ETLJOB.png --- Shows that the data from s3 bucket stored in redshift database table sample_insurance                                                        without any dupliucate values.
    -The python file 
         - ETL_JOB_SCRIPT.py -- The python code for the ETL JOB run is in this file. 
         - Lambda_Triggercode.py -- The lambda function python code written to trigger the crawler and ETL JOB is in this file. 
---------------------------------------------------------------------------------------------------------------------------------------------
### High-Level Workflow:
1. **AWS S3**: Stores the incoming data files (e.g., CSV, etc.).
2. **AWS Glue Crawler**: Infers the schema of the files stored in S3.
3. **AWS Glue ETL Job**: Transforms the data (e.g., changing the schema, dropping duplicates).
4. **Amazon Redshift**: Stores the transformed data in a table named `sample_insurance` in a development database.
5. **AWS Lambda**: Triggers the Glue ETL job whenever a new file is uploaded to the S3 bucket.

---

## Prerequisites

1. **AWS Account** with the necessary permissions to access:
   - S3
   - AWS Glue
   - AWS Lambda
   - Amazon Redshift

3. **Redshift Cluster** set up and a database (e.g., `dev`) with the `sample_insurance` table created.

4. **IAM Roles** with the necessary permissions:
   - Lambda execution role (access to S3, Glue, Redshift).
   - Glue service role (access to S3 and Redshift).
   
5. **S3 Bucket** created to store the incoming data files.

---

## Steps to Set Up the Project

### 1. Set Up S3 Bucket

- Create an S3 bucket where data files will be uploaded. For example, `s3://databucket-tostore-inredshift/`.

### 2. Set Up Glue Crawler

- Create a Glue Crawler that points to the S3 bucket where data files are uploaded.
- This crawler will automatically detect the schema of the files.
  - **Crawler Source**: `s3:/databucket-tostore-inredshift/`
  - **Crawler Target**: Create a database in Glue (e.g., `insurance_db`) and store the metadata.

### 3. Set Up Glue ETL Job

- Create an ETL job in AWS Glue to perform the following transformations:
  - **Schema Change**: Modify the data schema if needed (e.g., renaming columns or changing data types).
  - **Remove Duplicates**: Use AWS Glue’s DynamicFrame to remove duplicates based on some key.
  - **Destination**: Load the transformed data into Amazon Redshift, specifically into the `sample_insurance` table in the `dev` database.
  
- The Glue job script will leverage the following steps:
  - Use the `DynamicFrame` API to read from the S3 source.
  - Apply any necessary transformations.
  - Write the transformed data into Redshift using the JDBC connection.

### 4. Set Up Lambda Function

- Create an AWS Lambda function to monitor the S3 bucket for new file uploads and trigger the Glue ETL job.
  
  Lambda function:
  - Trigger: `s3:ObjectCreated:*` event type on the S3 bucket.
  - Action: Start the Crawler to fetch schema and Glue ETL job whenever a new file is uploaded to the S3 bucket.

### 5. Set Up Redshift Table

- Ensure that the `sample_insurance` table exists in the Redshift database. The schema for this table should match the transformed data.
  
  Example table schema in Redshift:
  ```sql
  CREATE TABLE sample_insurance (
    column names 
  );
  ```
 SEE : Values_stored_in_redshift_by_etljob.png 
---

## AWS Resources Setup

### 1. Glue Crawler Setup
- Go to the AWS Glue Console.
- Create a new crawler and specify the S3 bucket as the source.
- Set up a target Glue database (e.g., `insurance_db`).
- Run the crawler to detect the file schema and populate the Glue Data Catalog.

### 2. Glue ETL Job Script

The ETL job script is in file ETL_JOB_SCRIPT.PY

### 3. Lambda Function to Trigger Glue CRAWLER AND ETL JOB

The Lambda function is in LAMBDA_TRIGGERCODE.PY

This Lambda function will be triggered by the event when a new file is uploaded to the S3 bucket.

### 4. Redshift Table Setup

Create the table in Redshift using SQL

SEE : Values_stored_in_redshift_by_etljob.png 
---

## How It Works

1. A new file is uploaded to the S3 bucket.
2. The S3 event triggers the Lambda function.
3. The Lambda function triggers the Glue Crawler and the ETL job.
4. The Glue ETL job reads the file from the S3 bucket, performs transformations like schema changes and removing duplicates,
5. and then loads the data into the `sample_insurance` table in the Redshift database.

---

## Conclusion

This project automates the process of loading data from S3 to Redshift using AWS Glue and Lambda, 
with transformations applied to ensure data quality and consistency. 
The architecture allows for easy scaling as new files are uploaded to the S3 bucket, and the data can be analyzed in Amazon Redshift.
