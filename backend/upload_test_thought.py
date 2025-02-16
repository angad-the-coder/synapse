from google.cloud import storage
import json
from datetime import datetime

# Initialize the client
client = storage.Client.from_service_account_json('credentials.json')
bucket = client.get_bucket('synapse-ai-bucket')

# Create test thought data
thought_data = {
    'thought': 'A peaceful mountain lake at sunrise, with mist rising from the water and birds flying overhead.',
    'stress_level': 30,
    'timestamp': datetime.now().isoformat()
}

# Upload to bucket
blob_name = f'thought_{thought_data["timestamp"]}.json'
blob = bucket.blob(blob_name)
blob.upload_from_string(json.dumps(thought_data))

print(f"Uploaded test thought data: {thought_data}")
