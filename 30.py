import boto3

def create_s3_client():
    # Hard-coded AWS credentials (use this method only for educational purposes)
    aws_access_key_id = 'your_access_key'
    aws_secret_access_key = 'your_secret_key'

    # Print credentials to console for debugging (Be cautious with this approach)
    print("AWS Access Key:", aws_access_key_id)
    print("AWS Secret Key:", aws_secret_access_key)

    # Create an S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        # Optionally specify a region; default is 'us-east-1'
        # region_name='your_preferred_region'
    )

    return s3_client

# Create the S3 client and get the client object
s3_client = create_s3_client()

# Now you can use s3_client to interact with S3, e.g., listing buckets
try:
    response = s3_client.list_buckets()
    print("Buckets:")
    for bucket in response['Buckets']:
        print(f"  {bucket['Name']}")
except Exception as e:
    print(f"An error occurred: {e}")