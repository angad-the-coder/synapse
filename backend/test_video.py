"""Test script for video generation."""

import asyncio
from video_service import VideoService

async def main():
    # Initialize video service
    video_service = VideoService()
    
    # Test prompt
    prompt = "a house by the beach that is burning in broad daylight, cinematic quality, dramatic lighting, smoke billowing into clear blue sky"
    
    try:
        # Generate video
        print("Generating video...")
        video_url = await video_service.generate_video(prompt)
        print(f"\nVideo generated successfully!")
        print(f"Video URL: {video_url}")
        
    except Exception as e:
        print(f"Error generating video: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
