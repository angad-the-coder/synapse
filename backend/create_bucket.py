from google.cloud import storage
import os

# Set credentials path
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_application_credentials.json'

def create_bucket():
    # Initialize the client
    storage_client = storage.Client()
    
    # Create bucket name
    bucket_name = "eeg-video-stream-treehacks"
    
    # Create new bucket
    bucket = storage_client.create_bucket(
        bucket_name,
        location="us-central1"
    )
    
    # Make bucket public
    bucket.make_public()
    
    print(f"Bucket {bucket.name} created successfully")
    return bucket.name

if __name__ == "__main__":
    bucket_name = create_bucket()
    print(f"Use this bucket name in your .env file: {bucket_name}")
