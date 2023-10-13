import boto3
import pandas as pd

main_path = '{accesskey.csv}'
file = pd.read_csv(main_path)
region = 'us-east-1'
account = '{account_number}'
# print(file)

# S3 bucket name
s3_bucket_name = '{S3BUCKET}'
s3_resource = boto3.resource("s3")
s3_bucket = s3_resource.Bucket(s3_bucket_name)
files = s3_bucket.objects.all()

glueClient = boto3.client('glue')
print(glueClient)


for i in files:
    print(i)
    response = glueClient.create_crawler(
        Name='{}'.format(i),
        Role='arn:aws:iam::account##:role/GLUEROLE'.format(account),
        DatabaseName='dbname',
        Targets={'S3Targets': [{'Path': 's3:BUCKET'
                                        '/{}/'.format(i)}]})
