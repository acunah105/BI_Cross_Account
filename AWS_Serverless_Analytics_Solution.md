# AWS Serverless Analytics Solution 

Usage of AWS Services such as S3, IAM, AWS Glue, Amazon Athena, Lamdba, and Amazon QuickSight for Analytics.  

The aim of this documentation is to provide an ease step by step of set up for serveless lakehouse and visualization through QuickSight.

# Architecture:

![Screenshot 2023-10-13 at 8 48 17 AM](https://github.com/handelenriquezacuna/BI_Solutions/assets/62151237/62fc5217-81ae-4483-a1b0-b0e05292d8b9)


# AWS Tools:
Athena: Interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL. To learn more

QuickSight: Cloud-scale business intelligence (BI) service that you can use to deliver easy-to-understand insights to the people who you work with, wherever they are. To learn more

S3: Object storage service that offers industry-leading scalability, data availability, security, and performance. To learn more

IAM: Web service that helps you securely control access to AWS resources. To learn more.

Lambda: Event-driven compute service that lets you run code for virtually any type of application or backend service

AWS Glue: scalable, serverless data integration service that makes it easy to discover, prepare, and combine data for analytics, machine learning, and application development. To learn more

Boto3: Python SDK for AWS that allows you to directly create, update, and delete AWS resources from your Python scripts.

# Steps to follow:

* Create S3 Bucket: https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html
* Create AWS Athena DB https://docs.aws.amazon.com/athena/latest/ug/getting-started.html
* Create AWS Glue job(the process will be ran with manual process): https://us-east-1.console.aws.amazon.com/gluestudio/home?region=us-east-1#/jobs 
  * Select Spark script editor:
    * Add ``` sqlContext = HiveContext(sc) ``` to use pyspark full engine.    
    * Read data from S3 with Python Spark: https://spark.apache.org/docs/latest/sql-data-sources.html
      * Code Sample:
        * csv:
             ```
              # Read a csv with delimiter and a header
              df3 = spark.read.option("delimiter", ";").option("header", True).csv(path)
              df3.show()
             ```
        * parquet:
             ```
               # Read in the Parquet file created above
                 parquetFile = spark.read.parquet("S3_Path_URI")             
               # Parquet files can also be used to create a temporary view and then used in SQL statements.
                  parquetFile.createOrReplaceTempView("parquetFile")
                  parquetFile.show()
             ```
        * pandas_dataframe:
             ```
                import pandas as pd    
                data = [['Scott', 50], ['Jeff', 45], ['Thomas', 54],['Ann',34]] 
                 
                # Create the pandas DataFrame 
                pandasDF = pd.DataFrame(data, columns = ['Name', 'Age']) 
                  
                # print dataframe. 
                print(pandasDF)
                #Create PySpark DataFrame from Pandas
                  sparkDF=spark.createDataFrame(pandasDF) 
                  sparkDF.printSchema()
                  sparkDF.show()  
             ```
  * Create AWS Glue Crawler: https://docs.aws.amazon.com/glue/latest/ug/tutorial-add-crawler.html
  * Create IAM Role for usage: https://docs.aws.amazon.com/glue/latest/dg/create-an-iam-role.html
  * Lambda function set up:
  ###  RUNNING GLUE JOB  
    ```
    import logging
    import os
    import boto3
    import json
    
    # Set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Create Glue client
    client = boto3.client('glue')
    
    # The Glue job name is passed as a variables to the Lambda function
    glueJobName = "job_name"
    
    def lambda_handler(event, context):
        # Trigger the Glue job
        response = client.start_job_run(JobName = glueJobName)
        logger.debug(response)
        logger.info('## STARTED GLUE JOB: {} with ID: {}'.format(glueJobName,response['JobRunId']))
    
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
     ```
     ###  RUNNING GLUE CRAWLER  
     ```
     LAMBDA:
     import json
     import boto3
      
      #glue client
      client = boto3.client('glue')
      
      def lambda_handler(event, context):
          # TODO implement
          print("Running Crawler")
          response = client.start_crawler(Name='crawler_name')
          
      
          return {
              'statusCode': 200,
              'body': json.dumps('Hello from Lambda!')
          }
     ``` 
     #### OR 
     ```
     GLUE JOB:
     import boto3
      
      #glue client
      try:
          client = boto3.client('glue')
          print("Running Crawler")
          response = client.start_crawler(Name='crawler_name')
      except:
          print("Crawler Already Running")
          pass
                }
     ```
 * Visualizing in QuickSight with Athena Catalog: https://aws.amazon.com/es/blogs/big-data/accessing-and-visualizing-data-from-multiple-data-sources-with-amazon-athena-and-amazon-quicksight/ 
