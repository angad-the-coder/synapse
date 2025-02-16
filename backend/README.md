# EEG-to-Video Pipeline Component

This repository contains the middle component of a larger EEG-to-Video generation project:
```
[EEG Processing] → [This Pipeline] → [Video Generation]
```

## Project Context

This pipeline is the crucial middle component that:
1. Receives processed EEG thoughts and Garmin stress levels
2. Transforms them into video-ready prompts
3. Outputs prompts formatted for video generation services

## Integration Points

### Input (From EEG Processing)
- Thought string (from EEG data via embeddings and cosine similarity)
- Stress level (0-100, from Garmin)

### Output (To Video Generation)
The pipeline provides two API endpoints for video generation integration:

1. **Video-Ready Endpoint** (Recommended for Video Generation):
```python
# This endpoint returns just the prompt string, perfect for video generation
POST /generate_prompt/video_ready
{
    "thought": "grandson and football",
    "stress_level": 75
}

# Response: Plain string ready for video generation
"A young athlete throws a football across a sunlit field, his movements quick and purposeful..."
```

2. **Full Data Endpoint**:
```python
POST /generate_prompt
{
    "thought": "grandson and football",
    "stress_level": 75
}

# Response: Includes prompt and metadata
{
    "prompt": "A young athlete throws a football...",
    "metadata": {
        "stress_level": 75,
        "technical_specs": {
            "resolution": "1080p",
            "aspect_ratio": "16:9",
            "frame_rate": "30fps",
            "duration": "5-10 seconds"
        }
    }
}
```

## Quick Setup

1. Environment:
```bash
# .env file
OPENAI_API_KEY=your_key_here
TEMPERATURE=0.7
MAX_TOKENS=2000
MODEL_NAME=gpt-3.5-turbo-0125
```

2. Install:
```bash
pip install -r requirements.txt
```

3. Run:
```bash
python main.py  # Starts server on port 8000
```

## Pipeline Architecture

The pipeline processes inputs through three specialized layers:

1. **Expansion Layer**: Three independent agents enhance the thought:
   - Visual Details Agent
   - Sequential Steps Agent
   - Emotional Context Agent

2. **Evaluator Layer**: Research-backed synthesis based on stress:
   - Low stress (0-30): Emphasizes visual details
   - Medium stress (31-69): Balanced processing
   - High stress (70-100): Prioritizes emotional and action elements

3. **Prompt Generator Layer**: Creates video-ready output:
   - Concrete, filmable descriptions
   - Stress-appropriate pacing
   - Standard video specifications

## Example Integration

```python
import requests

# Your EEG processing outputs
eeg_thought = "grandson and football"
garmin_stress = 75

# Get video-ready prompt
response = requests.post(
    "http://localhost:8000/generate_prompt/video_ready",
    json={
        "thought": eeg_thought,
        "stress_level": garmin_stress
    }
)

# The prompt is now ready for your video generation service
video_prompt = response.text
video_service.generate(video_prompt)  # Your video generation call
