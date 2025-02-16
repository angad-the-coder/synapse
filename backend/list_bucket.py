from google.cloud import storage

# Initialize the client
client = storage.Client.from_service_account_json('credentials.json')
bucket = client.get_bucket('synapse-ai-bucket')

# List all blobs in the bucket
print("Contents of synapse-ai-bucket:")
print("-" * 50)
for blob in bucket.list_blobs():
    print(f"File: {blob.name}")
    try:
        content = blob.download_as_string()
        print(f"Content: {content[:200]}...") # Show first 200 chars
    except Exception as e:
        print(f"Could not read content: {e}")
    print("-" * 50)
