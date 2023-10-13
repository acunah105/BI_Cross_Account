# BI_Cross_Account

Use Amazon Athena and Amazon QuickSight in a cross-account environment

The aim of the documentation is to ease the step by step for the cross account access for QuickSight as visualization tool and Athena as table consulting and troubleshooting when is needed. 


# Architecture:

![image (1)](https://github.com/acunah105/BI_Cross_Account/assets/62151237/5378d100-20be-43d5-b119-d64d79e03d84)


# Important:

-Source data(from account A) is not mutable, hence it cannot be changed only with the admin access for the source account(Account A).
-Documentation based on solution: https://aws.amazon.com/es/blogs/big-data/use-amazon-athena-and-amazon-quicksight-in-a-cross-account-environment/


# Prerequisites:

Main QuickSight Account & Athena table review and troubleshooting:
Conduit admin access LatamData:https://bindles.amazon.com/resource/amzn1.bindle.resource.4frc5z7nscf2pymkjzlq
Mailing List: https://email-list.amazon.com/email-list/expand-list/ba-finops-latam

New Accounts:
Conduit admin access sjo-bi-apcorp: https://bindles.amazon.com/resource/amzn1.bindle.resource.m36pmfkiok62syr3hlfai
Mailing List: https://email-list.amazon.com/email-list/expand-list/sjo-bi-apcorp


# AWS Tools:


Athena: Interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL. To learn more 

QuickSight: Cloud-scale business intelligence (BI) service that you can use to deliver easy-to-understand insights to the people who you work with, wherever they are. To learn more

S3: Object storage service that offers industry-leading scalability, data availability, security, and performance. To learn more

IAM: Web service that helps you securely control access to AWS resources. To learn more

AWS Glue:  scalable, serverless data integration service that makes it easy to discover, prepare, and combine data for analytics, machine learning, and application development. To learn more

LakeFormation: Fully managed service that makes it easy to build, secure, and manage data lakes. To learn more

Boto3: Python SDK for AWS that allows you to directly create, update, and delete AWS resources from your Python scripts. To learn more


# Development based on:

 https://aws.amazon.com/es/blogs/big-data/use-amazon-athena-and-amazon-quicksight-in-a-cross-account-environment/


# Development Steps: 


1- Create IAM to connect with CLI. Follow documentation for Creating an IAM user in your AWS account
2-Pip Install Boto3 in the terminal for your IDE. PYPI   
3-Configure your IAM user previously created in the IDE terminal. Example code:

```
aws configure 

AWS Access Key ID [None]:TEST
AWS Secret Access Key [None]:TEST
Default region name [None]: us-east-1 
Default output format [None]: 

-- 4-Run catalog policy update: Example code:
##
import boto3
import json

REGION = 'us-east-1'
PRODUCER_ACCOUNT_ID = '{accountA}'
CONSUMER_ACCOUNT_IDs = ['accountB']

glue = glue_client = boto3.client('glue')

policy_glue_x_account = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Cataloguers",
            "Effect": "Allow",
            "Action": [
                "glue:*"
            ],
            "Principal": {
                "AWS": CONSUMER_ACCOUNT_IDs
            },
            "Resource": [
                f"arn:aws:glue:{REGION}:{PRODUCER_ACCOUNT_ID}:catalog",
                f"arn:aws:glue:{REGION}:{PRODUCER_ACCOUNT_ID}:database/*",
                f"arn:aws:glue:{REGION}:{PRODUCER_ACCOUNT_ID}:table/*/*"
            ]
        }
    ]
}

policy = json.dumps(policy_glue_x_account)
glue.put_resource_policy(PolicyInJson=policy, EnableHybrid='TRUE')
```

5-Register Data Source in Athena:

* On the Athena console, choose Administration>Data sources in the navigation pane.
* Choose Connect data source.
* For Choose where your data is located, select S3 - AWS Glue Data Catalog and Next.
* Choose AWS Glue Data Catalog in another account.
* For Connection details, enter a Data Catalog name, optional description, and the Data Catalog owner’s AWS account ID.
* Choose Register.

Note: For best practice keep in mind alias like “glue-catalog-<account#>”

6-Grant QuickSight cross-account access to an S3 bucket(where data is storage)

* On the Amazon S3 console, choose Buckets.
* Choose the bucket that you want to create a policy for, or whose policy you want to edit.
* Choose Permissions.
* Enter the following policy:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    role or account to add
                ]
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::BUCKET/*"
        },
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    role or account to add
                ]
            },
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::BUCKET"
        }
    ]
}
```
* Choose Save changes.

Note: For more deeper understanding on amazon policies you can use policy generatoror Watch Policy Amazon Master: https://www.youtube.com/watch?v=YQsK4MtsELU and https://awspolicygen.s3.amazonaws.com/policygen.html
