"""
Ollama LLM client for generating logistics reports using Qwen 1.7B model.
"""
import requests
import re
from typing import Dict, Any
import json
from config import Config

class LocalLLMClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, model_url: str = None):
        """
        Initialize Ollama client.
        
        Args:
            model_url: Ollama API URL (defaults to Config value)
        """
        self.model_url = model_url or Config.LOCAL_LLM_URL
        self.model_name = Config.LOCAL_LLM_MODEL
        
    def generate_report(self, event_description: str) -> Dict[str, Any]:
        """
        Generate a logistics report using Ollama API.
        
        Args:
            event_description: Description of the logistics event
            
        Returns:
            dict: {
                'summary': str,
                'confidence_score': int,
                'raw_response': str
            }
        """
        try:
            # Create prompt using template
            prompt = Config.get_prompt_template().format(
                event_description=event_description
            )
            
            # Prepare system message and user prompt
            system_msg = "You are a logistics AI assistant. Analyze the supply chain event and provide a structured report."
            
            # Prepare Ollama API payload
            payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "system",
                        "content": system_msg
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "temperature": Config.LLM_TEMPERATURE,
                "num_predict": Config.LLM_MAX_TOKENS,
            }
            
            # Call Ollama API
            response = requests.post(
                f"{self.model_url}/api/chat",  # Using chat endpoint instead of generate
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=300  # 5 minutes timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract generated text from Ollama chat response
            generated_text = result.get('message', {}).get('content', '')
            
            if not generated_text:
                # Fallback to old response format
                generated_text = result.get('response', '')
            
            # Log the response for debugging
            print("Ollama Response:", result)
            print("Generated Text:", generated_text)
            
            # Try to extract confidence score from the text
            confidence_score = 75  # default score
            try:
                # Look for various confidence score patterns
                confidence_patterns = [
                    r'Confidence Score:\s*(\d+)',
                    r'Confidence:\s*(\d+)',
                    r'confidence score of (\d+)',
                    r'confidence: (\d+)',
                    r'confidence score: (\d+)',
                    r'(\d+)% confidence',
                    r'(\d+)% certain',
                ]
                
                for pattern in confidence_patterns:
                    match = re.search(pattern, generated_text, re.IGNORECASE)
                    if match:
                        confidence_score = int(match.group(1))
                        confidence_score = max(0, min(100, confidence_score))
                        break
                        
                print(f"Extracted confidence score: {confidence_score}")
            except Exception as e:
                print(f"Error extracting confidence score: {e}")
            
            return {
                'summary': generated_text.strip(),
                'confidence_score': confidence_score,
                'raw_response': result
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'summary': f"Error generating report: {str(e)}",
                'confidence_score': 0,
                'raw_response': str(e)
            }
    
    def check_model(self) -> Dict[str, Any]:
        """
        Check if Ollama model is accessible and responding.
        """
        try:
            # Check if Ollama is running and model is loaded
            resp = requests.post(
                f"{self.model_url}/api/show", 
                json={"name": self.model_name},
                timeout=5
            )
            
            if resp.status_code == 200:
                return {
                    'status_code': 200,
                    'ok': True,
                    'body': f"Ollama is running and {self.model_name} is available"
                }
            else:
                return {
                    'status_code': resp.status_code,
                    'ok': False,
                    'body': f"Model {self.model_name} not found or not loaded"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'status_code': None,
                'ok': False,
                'body': f"Failed to connect to Ollama API: {str(e)}"
            }