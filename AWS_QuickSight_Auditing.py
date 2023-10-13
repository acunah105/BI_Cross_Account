import boto3
import pandas as pd

main_path = '{accesskey.csv}'
file = pd.read_csv(main_path)
region = 'us-east-1'
account = '{account_number}'
# print(file)

# AWS Programatic access
'''AWS_Access'''
quicksight = boto3.client('quicksight',
                          aws_access_key_id=file['Access key ID'][0],
                          aws_secret_access_key=file['Secret access key'][0],
                          region_name=region)


def dashboardList(quicksight, account):
    # Dashboards
    # AWS client only queries 100 lines of information, hence NEXT TOKEN must be used for full extraction
    # All csvs are going to be output on absolute path(project path)

    response = quicksight.list_dashboards(AwsAccountId=account, MaxResults=100)
    print(response)
    usersFrame = pd.DataFrame()
    while "NextToken" in response:
        userList = response['DashboardSummaryList']
        for i in response['DashboardSummaryList']:
            user = i['Name']
            # print(user)
            userRow = pd.DataFrame([user], columns=['Name'])
            usersFrame = pd.concat([usersFrame, userRow], ignore_index=True)
        nextToken = response['NextToken']
        print(nextToken)
        response = quicksight.list_dashboards(AwsAccountId=account, NextToken=nextToken, MaxResults=100)
        # print(response)
    usersFrame = pd.DataFrame(usersFrame)
    # print(users)
    usersFrame.to_csv('dashboardQuickSight{}.csv'.format(account), index_label=False)
    return print("Sucessfully extract the list of dashboards")


def listUsers(quicksight, account):
    # USERS Access
    # AWS client only queries 100 lines of information, hence NEXT TOKEN must be used for full extraction
    # All csvs are going to be output on absolute path(project path)
    response = quicksight.list_users(AwsAccountId=account, MaxResults=100, Namespace='default')
    print(response)
    usersFrame = pd.DataFrame()
    while "NextToken" in response:
        userList = response['UserList']
        for i in response['UserList']:
            user = i['Email']
            # print(user)
            userRow = pd.DataFrame([user], columns=['users'])
            usersFrame = pd.concat([usersFrame, userRow], ignore_index=True)
        nextToken = response['NextToken']
        print(nextToken)
        response = quicksight.list_users(AwsAccountId=account, NextToken=nextToken, MaxResults=100,
                                         Namespace='default')
        # print(response)
    usersFrame = pd.DataFrame(usersFrame)
    # print(users)
    usersFrame.to_csv('usersQuickSight{}.csv'.format(account), index_label=False)
    return print("Extraction of all users in the Quicksight account")


if __name__ == '__main__':
    listUsers(quicksight, account)
    dashboardList(quicksight, account)
