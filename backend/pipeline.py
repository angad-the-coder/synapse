"""
Main pipeline for converting thoughts to video prompts.
Uses a three-layer agent system for detailed, emotionally-aware video generation.
"""

from langchain_openai import ChatOpenAI
from agents import ExpansionAgents, EvaluatorAgent, VideoPromptGenerator
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Load environment variables
load_dotenv()

class LangchainPipeline:
    """Handles the conversion of thoughts to video-ready prompts."""
    
    def __init__(self):
        """Initialize the pipeline with OpenAI client."""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.expansion_agents, self.evaluator_agent, self.video_generator = initialize_pipeline(self.openai_api_key)
    
    def generate_video_prompt(self, thought: str, stress_level: float) -> str:
        """Generate a video prompt from a thought and stress level.
        
        Uses a three-layer agent system:
        1. Expansion Agents: Add details, steps, and emotions
        2. Evaluator: Synthesize based on stress level
        3. Prompt Generator: Create final video prompt
        
        Args:
            thought: Raw thought from EEG
            stress_level: Current stress level (0-100)
            
        Returns:
            str: Generated video prompt
        """
        # Layer 1: Expansion Agents
        details = self.expansion_agents.add_vivid_details(thought)
        steps = self.expansion_agents.break_into_steps(thought)
        emotions = self.expansion_agents.enhance_emotions(thought, stress_level)
        
        # Layer 2: Evaluator
        refined_thought = self.evaluator_agent.evaluate_and_synthesize(
            thought=thought,
            details=details,
            steps=steps,
            emotions=emotions,
            stress_level=stress_level
        )
        
        # Layer 3: Prompt Generator
        return self.video_generator.generate_final_prompt(refined_thought)

def initialize_pipeline(openai_api_key):
    """Initialize the complete thought-to-video pipeline with continuous processing.
    
    Args:
        openai_api_key: OpenAI API key for language model
    
    Returns:
        tuple: (ExpansionAgents, EvaluatorAgent, VideoPromptGenerator)
    """
    llm = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    
    # Initialize agents with continuous processing
    expansion_agents = ExpansionAgents(llm)
    evaluator_agent = EvaluatorAgent(llm, expansion_agents)
    video_generator = VideoPromptGenerator(llm, evaluator_agent)
    
    return expansion_agents, evaluator_agent, video_generator

def start_pipeline(openai_api_key):
    """Start the continuous processing pipeline.
    
    Args:
        openai_api_key: OpenAI API key for language model
    """
    expansion_agents, evaluator_agent, video_generator = initialize_pipeline(openai_api_key)
    
    # The continuous processing is already started in each agent's __init__
    print("Pipeline started! Processing thoughts continuously...")