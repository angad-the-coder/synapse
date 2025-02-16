import requests
import json
import time

def create_video(prompt):
    """Create a video using Luma API with the exact curl format."""
    url = "https://api.lumalabs.ai/dream-machine/v1/generations"
    headers = {
        "accept": "application/json",
        "authorization": "Bearer luma-efc0f466-b22b-4659-aa8a-24bfac20b167-2c620503-1c85-42bc-ae0e-b8395f34ae7d",
        "content-type": "application/json"
    }
    data = {
        "prompt": prompt,
        "model": "ray-2",
        "resolution": "720p",
        "duration": "10s"
    }

    try:
        print(f"\nStarting video generation with prompt: {prompt}")
        
        # Create generation
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if not result.get('id'):
            print("Error: No generation ID in response")
            return None
            
        generation_id = result['id']
        print(f"Generation started with ID: {generation_id}")
        
        # Poll for completion
        while True:
            status_url = f"{url}/{generation_id}"
            status_response = requests.get(status_url, headers=headers)
            status_response.raise_for_status()
            status = status_response.json()
            
            print(f"Status: {status.get('state', 'unknown')}")
            
            if status.get('state') == 'completed':
                if status.get('assets', {}).get('video'):
                    video_url = status['assets']['video']
                    print(f"\nVideo generated successfully!")
                    print(f"Video URL: {video_url}")
                    return video_url
                print("Error: No video URL in completed status")
                return None
            elif status.get('state') == 'failed':
                print(f"Generation failed: {status.get('failure_reason', 'Unknown error')}")
                return None
                
            time.sleep(2)
            
    except Exception as e:
        print(f"Error generating video: {e}")
        return None

if __name__ == "__main__":
    # Test the video generation
    test_prompt = "an old lady laughing underwater, wearing a scuba diving suit"
    create_video(test_prompt)
