import boto3
import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "aws_config.yaml")

with open(CONFIG_PATH, "r") as f:
    aws_config = yaml.safe_load(f)

# Fallbacks in case keys are missing
aws_access_key_id = aws_config.get("aws_access_key_id", os.getenv("AWS_ACCESS_KEY_ID"))
aws_secret_access_key = aws_config.get("aws_secret_access_key", os.getenv("AWS_SECRET_ACCESS_KEY"))
region_name = aws_config.get("region_name", os.getenv("AWS_REGION"))
bucket_name = aws_config.get("bucket_name", os.getenv("AWS_BUCKET_NAME"))

if not aws_access_key_id or not aws_secret_access_key or not bucket_name:
    raise ValueError("❌ Missing AWS credentials or bucket_name in aws_config.yaml or environment variables")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name,
)

def upload_to_s3(file_path, s3_key):
    s3_client.upload_file(file_path, bucket_name, s3_key)
    return f"s3://{bucket_name}/{s3_key}"

def download_from_s3(s3_key, local_path):
    s3_client.download_file(bucket_name, s3_key, local_path)
    return local_path

def list_s3(prefix=""):
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    return [item["Key"] for item in response.get("Contents", [])]
