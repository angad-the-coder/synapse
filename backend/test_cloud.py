from cloud_storage import storage_manager

# Test cloud storage connection
print("Testing cloud storage connection...")
thought_data = storage_manager.get_latest_thought()
print(f"Latest thought data: {thought_data}")
