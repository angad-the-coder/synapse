"""
Test suite for the video generation pipeline. Tests the pipeline's ability to
generate appropriate prompts based on different stress levels and verifies that
the emotional tone matches the expected intensity.
"""

import unittest
from pipeline import LangchainPipeline
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def print_formatted_result(prompt, stress_level):
    """Pretty print the pipeline result.
    
    Args:
        prompt (str): Generated video prompt
        stress_level (float): Stress level used to generate the prompt
    """
    print(f"\n{'='*80}")
    print(f"🎯 Testing: 'grandson and football' at stress level {stress_level}")
    print(f"{'='*80}\n")
    print("🎬 FINAL VIDEO PROMPT:")
    print("-" * 40)
    print(prompt)
    print("\n" + "="*80 + "\n")

class TestPipeline(unittest.TestCase):
    """Test cases for the video generation pipeline."""

    def setUp(self):
        """Set up test environment before each test."""
        self.llm = ChatOpenAI(
            temperature=float(os.getenv('TEMPERATURE', 0.7)),
            max_tokens=int(os.getenv('MAX_TOKENS', 2000)),
            model_name=os.getenv('MODEL_NAME', 'gpt-3.5-turbo-0125')
        )
        self.pipeline = LangchainPipeline(self.llm)

    def test_stress_comparison(self):
        """Compare pipeline output for 'grandson and football' at different stress levels.
        
        Tests three scenarios:
        1. Low stress (20): Should produce gentle, warm, peaceful content
        2. Medium stress (50): Should produce balanced, natural content
        3. High stress (87): Should produce intense, urgent, dynamic content
        """
        test_cases = [
            ("Low Stress", 20),
            ("Medium Stress", 50),
            ("High Stress", 87)
        ]
        
        for label, stress_level in test_cases:
            with self.subTest(label=label):
                # Generate prompt
                prompt = self.pipeline.generate_video_prompt(
                    thought="grandson and football",
                    stress_level=stress_level
                )
                
                # Print result for manual inspection
                print_formatted_result(prompt, stress_level)
                
                # Basic validation
                self.assertIsInstance(prompt, str)
                self.assertTrue(len(prompt) > 100)  # Should be reasonably detailed
                
                # Verify technical specs are included
                self.assertIn("1080p", prompt)
                self.assertIn("16:9", prompt)
                self.assertIn("30fps", prompt)
                
                # Verify stress-appropriate language
                if stress_level < 30:
                    self.assertTrue(
                        any(word in prompt.lower() for word in ["gentle", "peaceful", "calm", "soft"])
                    )
                elif stress_level > 70:
                    self.assertTrue(
                        any(word in prompt.lower() for word in ["dynamic", "intense", "rapid", "energetic"])
                    )

    def test_input_validation(self):
        """Test input validation for stress levels and thoughts."""
        invalid_inputs = [
            (-10, "thought", "stress_level must be between 0 and 100"),
            (110, "thought", "stress_level must be between 0 and 100"),
            (50, "", "thought must be a non-empty string"),
            (50, None, "thought must be a non-empty string")
        ]
        
        for stress_level, thought, expected_error in invalid_inputs:
            with self.subTest(stress_level=stress_level, thought=thought):
                with self.assertRaises(ValueError) as context:
                    self.pipeline.generate_video_prompt(thought, stress_level)
                self.assertIn(expected_error, str(context.exception))

def main():
    """Run the test suite."""
    # Add a small delay between tests to avoid rate limiting
    unittest.TestLoader.sortTestMethodsUsing = None
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPipeline)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == "__main__":
    main()
