"""
Video generation service using Replicate's Zeroscope model.
Handles video generation and storage in Google Cloud Storage.
"""

import os
import asyncio
import aiohttp
from typing import Dict, Optional
from google.cloud import storage
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VideoGenerationError(Exception):
    """Custom error for video generation failures."""
    pass

class VideoService:
    def __init__(self):
        """Initialize video service with Google Cloud and Replicate credentials."""
        # Get environment variables
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        self.bucket_name = os.getenv('VIDEO_OUTPUT_BUCKET')
        self.replicate_token = os.getenv('REPLICATE_API_TOKEN')
        
        if not all([self.project_id, self.bucket_name, self.replicate_token]):
            raise ValueError("Missing required environment variables")
            
        # Initialize Google Cloud Storage
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(self.bucket_name)
        
        # Zeroscope model settings
        self.model_version = "9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351"
    
    async def generate_video(self, prompt: str, transition_context: Optional[Dict] = None) -> str:
        """Generate a video from a prompt and apply transitions.
        
        Args:
            prompt: Text prompt for video generation
            transition_context: Optional context for smooth transitions
            
        Returns:
            str: Public URL of the generated video
        """
        try:
            # 1. Generate video using Replicate
            video_url = await self._generate_with_replicate(prompt)
            
            # 2. Download video
            video_data = await self._download_video(video_url)
            
            # 3. Apply transition if needed
            if transition_context and transition_context.get('previous_video'):
                video_data = await self._apply_transition(
                    video_data,
                    transition_context
                )
            
            # 4. Upload to Google Cloud Storage
            gcs_uri = await self._upload_to_gcs(video_data)
            
            # 5. Get public URL
            public_url = self.get_public_url(gcs_uri)
            
            return public_url
            
        except Exception as e:
            raise VideoGenerationError(f"Failed to generate video: {str(e)}")
    
    async def _generate_with_replicate(self, prompt: str) -> str:
        """Generate video using Replicate's Zeroscope model.
        
        Args:
            prompt: Text prompt for video generation
            
        Returns:
            str: URL to download the generated video
        """
        headers = {
            "Authorization": f"Token {self.replicate_token}",
            "Content-Type": "application/json",
        }
        
        # Model parameters
        payload = {
            "version": self.model_version,
            "input": {
                "prompt": prompt,
                "num_frames": 72,  # 3 seconds at 24fps
                "fps": 24,
                "width": 1024,
                "height": 576
            }
        }
        
        async with aiohttp.ClientSession() as session:
            # Start prediction
            async with session.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 201:
                    raise VideoGenerationError(
                        f"Failed to start video generation: {await response.text()}"
                    )
                prediction = await response.json()
            
            # Poll until complete
            while True:
                async with session.get(
                    f"https://api.replicate.com/v1/predictions/{prediction['id']}",
                    headers=headers
                ) as response:
                    prediction = await response.json()
                    if prediction["status"] == "succeeded":
                        return prediction["output"]
                    elif prediction["status"] == "failed":
                        raise VideoGenerationError(
                            f"Video generation failed: {prediction.get('error', 'Unknown error')}"
                        )
                    await asyncio.sleep(1)
    
    async def _download_video(self, url: str) -> bytes:
        """Download video from URL.
        
        Args:
            url: Video URL
            
        Returns:
            bytes: Video data
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise VideoGenerationError(f"Failed to download video: {response.status}")
                return await response.read()
    
    async def _apply_transition(self, video_data: bytes, transition_context: Dict) -> bytes:
        """Apply transition effect between videos.
        
        Args:
            video_data: Current video data
            transition_context: Transition information
            
        Returns:
            bytes: Video with transition applied
        """
        # For now, return the video as is
        # TODO: Implement video transitions using moviepy or similar
        return video_data
    
    async def _upload_to_gcs(self, video_data: bytes) -> str:
        """Upload video to Google Cloud Storage.
        
        Args:
            video_data: Video data to upload
            
        Returns:
            str: GCS URI of uploaded video
        """
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        blob_name = f"videos/{timestamp}.mp4"
        
        # Upload
        blob = self.bucket.blob(blob_name)
        blob.upload_from_string(video_data, content_type='video/mp4')
        
        # Make public
        blob.make_public()
        
        return f"gs://{self.bucket_name}/{blob_name}"
    
    def get_public_url(self, gcs_uri: str) -> str:
        """Convert GCS URI to public URL.
        
        Args:
            gcs_uri: Google Cloud Storage URI
            
        Returns:
            str: Public URL for video access
        """
        # Convert gs:// URI to public URL
        # From: gs://bucket-name/path/to/video.mp4
        # To: https://storage.googleapis.com/bucket-name/path/to/video.mp4
        _, path = gcs_uri.split("gs://", 1)
        return f"https://storage.googleapis.com/{path}"
