"""
S3 integration utilities using boto3.
Handles upload, download, and listing of S3 objects.
"""

import boto3
import logging
import os
from botocore.exceptions import ClientError, NoCredentialsError
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)

class S3Manager:
    """S3 operations manager."""
    
    def __init__(self):
        """Initialize S3 client with configuration."""
        self.s3_client = None
        self.bucket_name = None
        self._load_config()
        self._init_client()
    
    def _load_config(self):
        """Load AWS configuration from file or environment."""
        config_path = Path("config/aws_config.yaml")
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    self.bucket_name = config.get('s3', {}).get('bucket_name')
                    logger.info(f"Loaded S3 config from {config_path}")
            except Exception as e:
                logger.warning(f"Error loading S3 config: {e}")
        
        # Override with environment variables if available
        self.bucket_name = os.getenv('S3_BUCKET_NAME', self.bucket_name)
        
        if not self.bucket_name:
            logger.warning("S3 bucket name not configured")
    
    def _init_client(self):
        """Initialize S3 client."""
        try:
            # Try to create S3 client with default credentials
            self.s3_client = boto3.client('s3')
            logger.info("S3 client initialized successfully")
        except NoCredentialsError:
            logger.warning("AWS credentials not found. S3 operations will fail.")
        except Exception as e:
            logger.error(f"Error initializing S3 client: {e}")
    
    def upload_file(self, local_path: str, s3_key: str) -> bool:
        """Upload a file to S3."""
        if not self.s3_client or not self.bucket_name:
            logger.error("S3 not properly configured")
            return False
        
        try:
            self.s3_client.upload_file(local_path, self.bucket_name, s3_key)
            logger.info(f"Successfully uploaded {local_path} to s3://{self.bucket_name}/{s3_key}")
            return True
        except FileNotFoundError:
            logger.error(f"Local file not found: {local_path}")
            return False
        except ClientError as e:
            logger.error(f"S3 upload error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during S3 upload: {e}")
            return False
    
    def download_file(self, s3_key: str, local_path: str) -> bool:
        """Download a file from S3."""
        if not self.s3_client or not self.bucket_name:
            logger.error("S3 not properly configured")
            return False
        
        try:
            # Create directory if it doesn't exist
            local_dir = Path(local_path).parent
            local_dir.mkdir(parents=True, exist_ok=True)
            
            self.s3_client.download_file(self.bucket_name, s3_key, local_path)
            logger.info(f"Successfully downloaded s3://{self.bucket_name}/{s3_key} to {local_path}")
            return True
        except ClientError as e:
            logger.error(f"S3 download error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during S3 download: {e}")
            return False
    
    def list_objects(self, prefix: str = "") -> list:
        """List objects in S3 bucket with given prefix."""
        if not self.s3_client or not self.bucket_name:
            logger.error("S3 not properly configured")
            return []
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            objects = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    objects.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'],
                        'etag': obj['ETag']
                    })
            
            logger.info(f"Listed {len(objects)} objects with prefix '{prefix}'")
            return objects
            
        except ClientError as e:
            logger.error(f"S3 list error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during S3 list: {e}")
            return []

# Global S3 manager instance
s3_manager = S3Manager()

# Convenience functions for backward compatibility
def upload_to_s3(local_path: str, s3_key: str) -> bool:
    """Upload a file to S3."""
    return s3_manager.upload_file(local_path, s3_key)

def download_from_s3(s3_key: str, local_path: str) -> bool:
    """Download a file from S3."""
    return s3_manager.download_file(s3_key, local_path)

def list_s3(prefix: str = "") -> list:
    """List objects in S3 bucket."""
    return s3_manager.list_objects(prefix)