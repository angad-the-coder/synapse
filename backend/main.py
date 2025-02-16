"""
Main entry point for the EEG thought-to-video pipeline.
"""

import os
import json
from google.cloud import storage
from cloud_storage import storage_manager
from lumaAPI import create_video

def main():
    """Main entry point."""
    try:
        # Get latest thought from storage
        thought_data = storage_manager.get_latest_thought()
        if not thought_data or not thought_data.get('thought'):
            print("No thought data available")
            return
            
        # Create video from thought
        thought = thought_data['thought']
        print(f"\nCreating video for thought: {thought}")
        video_url = create_video(thought)
        
        if video_url:
            print("\nSuccess! Video is available at the URL above.")
        else:
            print("\nFailed to create video.")
            
    except KeyboardInterrupt:
        print("\nStopping...")

if __name__ == "__main__":
    main()
