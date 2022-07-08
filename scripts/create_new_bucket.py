import sys
import boto3

def main():
    if not sys.argv[1:]:
        print("No bucket name specified")
        sys.exit(0)

    bucket_name = sys.argv[1]

    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=bucket_name)

    response = s3_client.list_buckets()
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')

if __name__=='__main__':
    main()