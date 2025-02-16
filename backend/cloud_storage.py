from google.cloud import storage
import json
from typing import Optional, Dict, Any, Set
from datetime import datetime

class CloudStorageManager:
    def __init__(self, bucket_name: str = "synapse-ai-bucket", credentials_path: str = "credentials.json"):
        """Initialize the Cloud Storage Manager.
        
        Args:
            bucket_name: Name of the GCS bucket
            credentials_path: Path to the credentials file
        """
        self.bucket_name = bucket_name
        self.credentials_path = credentials_path
        self.client = storage.Client.from_service_account_json(credentials_path)
        self.bucket = self.client.get_bucket(bucket_name)
        
    def get_latest_thought(self) -> Optional[Dict[str, Any]]:
        """Get the latest thought data from cloud storage.
        
        Returns:
            Dict containing the thought data if found, None otherwise
        """
        # List all blobs in the bucket
        blobs = list(self.bucket.list_blobs())
        if not blobs:
            print("No files found in bucket")
            return None

        # Sort by timestamp in the filename (assuming ISO format timestamps)
        latest_blob = max(blobs, key=lambda x: x.name)
        print(f"Found latest file: {latest_blob.name}")
        
        try:
            content = latest_blob.download_as_string()
            print(f"Downloaded content: {content}")
            data = json.loads(content)
            print(f"Parsed data: {data}")
            
            # Only process if there's a thought
            if data.get('thought'):
                print(f"Found thought: {data['thought']}")
                return data
            else:
                print(f"No thought found in file {latest_blob.name}")
                return None
                
        except Exception as e:
            print(f"Error processing file {latest_blob.name}: {e}")
            return None

# Global instance
storage_manager = CloudStorageManager()
