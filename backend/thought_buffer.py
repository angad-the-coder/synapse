"""
Manages a buffer of thoughts and their associated prompts/videos to ensure smooth transitions.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class ThoughtContext:
    """Represents a thought and its generated assets."""
    thought: str
    stress_level: float
    prompt: str
    video_uri: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class ThoughtBuffer:
    """Maintains a history of thoughts and their context for smooth transitions."""
    
    def __init__(self, buffer_size: int = 5):
        """Initialize thought buffer.
        
        Args:
            buffer_size: Number of recent thoughts to maintain
        """
        self.buffer_size = buffer_size
        self.thoughts: List[ThoughtContext] = []
        
    def add_thought(self, thought: str, stress_level: float, prompt: str) -> ThoughtContext:
        """Add a new thought and its prompt to the buffer.
        
        Args:
            thought: Raw thought from EEG
            stress_level: Current stress level
            prompt: Generated video prompt
            
        Returns:
            ThoughtContext: The newly created thought context
        """
        context = ThoughtContext(
            thought=thought,
            stress_level=stress_level,
            prompt=prompt
        )
        
        self.thoughts.append(context)
        
        # Maintain buffer size
        if len(self.thoughts) > self.buffer_size:
            self.thoughts.pop(0)
            
        return context
    
    def update_video_uri(self, thought: str, video_uri: str):
        """Update the video URI for a specific thought."""
        for context in self.thoughts:
            if context.thought == thought:
                context.video_uri = video_uri
                break
    
    def get_transition_context(self, current_thought: str) -> Dict:
        """Get context for smooth video transition.
        
        Args:
            current_thought: The current thought being processed
            
        Returns:
            dict: Context for video generation including:
                - previous_thought: The last thought processed
                - previous_prompt: The last prompt generated
                - previous_video: URI of the last video
                - transition_type: Suggested transition type
        """
        if not self.thoughts:
            return {
                'previous_thought': None,
                'previous_prompt': None,
                'previous_video': None,
                'transition_type': 'fade_in'
            }
            
        previous = self.thoughts[-1]
        return {
            'previous_thought': previous.thought,
            'previous_prompt': previous.prompt,
            'previous_video': previous.video_uri,
            'transition_type': self._determine_transition_type(
                previous.thought, 
                current_thought
            )
        }
    
    def _determine_transition_type(self, prev_thought: str, curr_thought: str) -> str:
        """Determine appropriate transition type based on thought similarity."""
        # For now, use cross-fade for all transitions
        # TODO: Implement more sophisticated transition logic based on thought similarity
        return "cross_fade"
    
    def get_recent_thoughts(self, limit: Optional[int] = None) -> List[ThoughtContext]:
        """Get recent thoughts, optionally limited to a specific count."""
        if limit is None or limit >= len(self.thoughts):
            return self.thoughts
        return self.thoughts[-limit:]
