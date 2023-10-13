import boto3
import pandas as pd

main_path = '{credentialPath}'
file = pd.read_csv(corp_path)
region = 'us-east-1'
# print(file)

# AWS Programatic access
'''AWS_Access'''
lambda_client = boto3.client('lambda',
                             aws_access_key_id=file['Access key ID'][0],
                             aws_secret_access_key=file['Secret access key'][0],
                             region_name=region)
# print(lambda_client)

response = lambda_client.list_functions()
print(response)

x = 1
for function in response['Functions']:
    function_name = function['FunctionName']
    print(x)
    x = x+1
    # Update the runtime
    lambda_client.update_function_configuration(
        FunctionName=function_name,
        Runtime='python3.10'
    )

    print(f"Updated runtime of {function_name} to Python 3.10")

print("All Lambda functions updated to Python 3.10")
