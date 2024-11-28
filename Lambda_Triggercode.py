import json
import boto3
import time
glue_etl = boto3.client('glue')
def lambda_handler(event, context):
    # TODO implement 
    #to access glue and trigger crawler
    etl_job_name = 'Schema_change_insurance'
    while True:
        state = glue_etl.get_crawler(
            Name='s3-to-redshift-etl' 
        )['Crawler']['State']

        if state == 'READY':
            break
        print(f"The crawler s3-to-redshift-etl is {state}")
        time.sleep(30)
    print("The crawler s3-to-redshift-etl is 'READY'")
    response = glue_etl.start_crawler(
        Name='s3-to-redshift-etl'
    )
    while True:
        state = glue_etl.get_crawler(
        Name='s3-to-redshift-etl' 
        )['Crawler']['State']
        if state == 'STOPPING':
            print(f"Triggering Glue ETL Job: {etl_job_name}")
            response = glue_etl.start_job_run(JobName=etl_job_name)
            print(f"ETL Job started successfully: {response['JobRunId']}")
            break
        else:
            print(f"Crawler did not complete successfully. Crawler state: {state}")
            time.sleep(30)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
