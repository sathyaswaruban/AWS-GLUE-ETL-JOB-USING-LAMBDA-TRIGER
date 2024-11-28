import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
from pyspark.sql import functions as SqlFuncs

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
AmazonS3_node1732703798600 = glueContext.create_dynamic_frame.from_catalog(database="insurance_db", table_name="newcrawlerdatabucket_tostore_in_redshift", transformation_ctx="AmazonS3_node1732703798600")

# Script generated for node Change Schema
ChangeSchema_node1732712690066 = ApplyMapping.apply(frame=AmazonS3_node1732703798600, mappings=[("custid", "string", "custid", "string"), ("age", "long", "age", "int"), ("sex", "string", "sex", "string"), ("bmi", "double", "bmi", "int"), ("children", "long", "no_of_children", "int"), ("smoker", "string", "smoker", "string"), ("region", "string", "region", "string"), ("expenses", "double", "expenses", "int")], transformation_ctx="ChangeSchema_node1732712690066")

# Script generated for node Drop Duplicates
DropDuplicates_node1732793453089 =  DynamicFrame.fromDF(ChangeSchema_node1732712690066.toDF().dropDuplicates(["custid"]), glueContext, "DropDuplicates_node1732793453089")

# Script generated for node Amazon Redshift
AmazonRedshift_node1732703812903 = glueContext.write_dynamic_frame.from_options(frame=DropDuplicates_node1732793453089, connection_type="redshift", connection_options={"redshiftTmpDir": "s3://aws-glue-assets-311141565701-ap-southeast-1/temporary/", "useConnectionProperties": "true", "dbtable": "public.sample_insurance", "connectionName": "Redshift connection", "preactions": "CREATE TABLE IF NOT EXISTS public.sample_insurance (custid VARCHAR, age INTEGER, sex VARCHAR, bmi INTEGER, no_of_children INTEGER, smoker VARCHAR, region VARCHAR, expenses INTEGER);"}, transformation_ctx="AmazonRedshift_node1732703812903")
