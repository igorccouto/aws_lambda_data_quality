import csv
import boto3

s3 = boto3.client('s3')

def read_csv(body):
    data = body.read().decode('utf-8').splitlines()
    records = csv.reader(data)
    content = []
    for eachRecord in records:
        content.append(eachRecord)
    
    return content

def check_csv_header(content):
    mandatory_headers = ['column1', 'column2', 'column3', 'column4']
    headers = content[0]
    if mandatory_headers == headers:
        return True
    else:
        return False

def lambda_handler(event, context):
    record = event['Records'][0]
    user_id = record['userIdentity']['principalId']
    csv_file_key = record['s3']['object']['key']
    bucket_name = record['s3']['bucket']['name']
    print(f'User {user_id} uploaded a CSV file {csv_file_key} in {bucket_name} bucket')

    try:
        response = s3.get_object(Bucket=bucket_name, Key=csv_file_key)
    except Exception as e:
        print(f'Error getting object {csv_file_key} from bucket {bucket_name}.')
        raise e
    
    body = response['Body']
    content = read_csv(body)
    
    if check_csv_header(content):
        s3.upload_fileobj(body, 'good-csv-files', csv_file_key)
        print(f'File {csv_file_key} moved to good-csv-files bucket')
    else:
        print(f'File {csv_file_key} is out of standard. Please check and resend.')

