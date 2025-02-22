from typing import Optional, Dict, List
from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

@dataclass
class AnkiCard:
    expression: str
    phonetic: str
    usage_examples: List[str]
    image_url: Optional[str] = None

class EnglishLearningAgent:
    def __init__(self):
        """Initialize the English Learning Agent with necessary API keys."""
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def generate_anki_card(self, expression: str) -> AnkiCard:
        """Generate an Anki card for the given English expression."""
        # Get pronunciation and phonetics
        pronunciation_info = self._get_pronunciation(expression)
        
        # Get usage examples
        examples = self._generate_usage_examples(expression)
        
        # Get relevant image
        image_url = self._find_relevant_image(expression)
        
        return AnkiCard(
            expression=expression,
            phonetic=pronunciation_info["phonetic"],
            usage_examples=examples,
            image_url=image_url
        )
    
    def _get_pronunciation(self, expression: str) -> Dict[str, str]:
        """
        Get pronunciation details using GPT model.
        """
        prompt = f"""For the English expression "{expression}", provide its IPA phonetic transcription in American English:
        Format your response exactly like this example:
        IPA: /həˈloʊ/
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a linguistics expert specializing in American English pronunciation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            # Parse the response
            lines = response.choices[0].message.content.strip().split('\n')
            pronunciation_data = {}
            
            for line in lines:
                if line.startswith('IPA:'):
                    pronunciation_data['phonetic'] = line.replace('IPA:', '').strip()
            
            return pronunciation_data
            
        except Exception as e:
            print(f"Error getting pronunciation: {e}")
            return {
                "pronunciation": "Not available",
            }
    
    def _find_relevant_image(self, expression: str) -> Optional[str]:
        """Generate a relevant image using DALL-E."""
        try:
            # First, get the literal meaning explained
            meaning_response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at explaining English expressions visually. Describe the core meaning in a way that can be drawn."},
                    {"role": "user", "content": f'Explain "{expression}".'}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            visual_meaning = meaning_response.choices[0].message.content.strip()
            
            # Create the image prompt using the visual meaning
            image_prompt = f"""
            You are an expert at explaining English expressions visually. Please create a picture explaning "{expression}" with a guide to the meaning below:
            {visual_meaning}

            Style requirements:
            - Clean lines and simple shapes
            - No text or words
            - White or simple background
            """
            print(image_prompt)
            
            response = self.openai_client.images.generate(
                model="dall-e-2",
                prompt=image_prompt,
                size="256x256",
                quality="standard",
                n=1,
            )
            
            return response.data[0].url
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return None

    def _generate_usage_examples(self, expression: str) -> List[str]:
        """Generate contextual examples using OpenAI's GPT model."""
        prompt = f"""Generate 3 natural, conversational examples using "{expression}".
        Examples should:
        - Use everyday situations
        - Show different contexts
        - Include informal dialogue
        - Demonstrate the expression's typical usage
        
        Format: Just the examples, one per line."""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a native American English speaker giving natural examples."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            examples = response.choices[0].message.content.strip().split('\n')
            return [example.strip() for example in examples if example.strip()]
            
        except Exception as e:
            print(f"Error generating examples: {e}")
            return [f"Example with '{expression}' not available."]

def main():
    # Example usage
    agent = EnglishLearningAgent()
    
    # Test expressions
    test_expressions = [
        "anticipate",
        "anesthesia",
        "cavity"
    ]
    
    for expression in test_expressions:
        print(f"\nGenerating card for: {expression}")
        print("-" * 50)
        
        card = agent.generate_anki_card(expression)
        
        print(f"Expression: {card.expression}")
        print(f"Phonetic: {card.phonetic}")
        for example in card.usage_examples:
            print(f"- {example}")
        if card.image_url:
            print(f"\nImage URL: {card.image_url}")

if __name__ == "__main__":
    main() 