import os
   import boto3

   def create_s3_client():
       access_key = os.environ.get('AWS_ACCESS_KEY_ID')
       secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

       if not access_key or not secret_key:
           raise ValueError("AWS credentials are not set in environment variables.")

       s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
       return s3_client