import pandas as pd
import boto3
import io
from dotenv import load_dotenv
import os

load_dotenv()

# AWS S3 Configuration
s3_endpoint = "https://s3.fr-par.scw.cloud"  # Replace with your S3-compatible endpoint
access_key = os.getenv("SCW_ACCESS_KEY")  # Replace with your access key
secret_key = os.getenv("SCW_SECRET_KEY")  # Replace with your secret key
bucket_name = "pollution-eau-s3"  # Replace with your bucket name
file_key = "test/test.txt"  # Key (file name) in the S3 bucket
file_name = "test.txt"

# Connect to S3
s3_client = boto3.client(
    "s3",
    endpoint_url=s3_endpoint,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name="fr-par",  
)

# Example DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
}
df = pd.DataFrame(data)
df.to_csv(file_name, index=False)



response = s3_client.upload_file(file_name, bucket_name, file_key)

response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
csv_data = response["Body"].read().decode("utf-8")

# Load the CSV data into a DataFrame
df_read = pd.read_csv(io.StringIO(csv_data))
print(df_read)

## Attention avec boto3 1.36 le upload file ne fonctionne pas, ce code utilise "boto3==1.34.11"
