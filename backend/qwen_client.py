"""
Qwen3 AI client for generating logistics reports.
Uses Hugging Face Inference API.
"""
import requests
import re
from typing import Dict, Tuple
from config import Config


class QwenClient:
    """Client for interacting with Qwen3 model via Hugging Face API"""
    
    def __init__(self, api_token: str = None):
        """
        Initialize Qwen client.
        
        Args:
            api_token: Hugging Face API token (defaults to Config value)
        """
        self.api_token = api_token or Config.HUGGINGFACE_API_TOKEN
        self.model = Config.QWEN_MODEL
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
    
    def generate_report(self, event_description: str) -> Dict[str, any]:
        """
        Generate a logistics report using Qwen3.
        
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
            
            # Prepare API payload
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": Config.QWEN_MAX_TOKENS,
                    "temperature": Config.QWEN_TEMPERATURE,
                    "top_p": 0.9,
                    "return_full_text": False
                }
            }
            
            # Call Hugging Face API
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract generated text
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
            else:
                generated_text = result.get('generated_text', '')
            
            # Parse confidence score from response
            confidence_score = self._extract_confidence_score(generated_text)
            
            return {
                'summary': generated_text.strip(),
                'confidence_score': confidence_score,
                'raw_response': generated_text
            }
            
        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors with clearer messages (e.g., 404 if model not found)
            status = None
            body = ''
            try:
                status = e.response.status_code
                body = e.response.text
            except Exception:
                pass

            if status == 404:
                msg = (
                    f"Model not found (404) at {self.api_url}. "
                    f"Check QWEN_MODEL='{self.model}' and that the model exists and is accessible with your token."
                )
            else:
                msg = f"HTTP error {status} when calling model endpoint: {str(e)}"

            return {
                'summary': f"Error generating report: {msg}",
                'confidence_score': 0,
                'raw_response': body or str(e)
            }
        except requests.exceptions.RequestException as e:
            # Handle other request-related errors gracefully
            return {
                'summary': f"Error generating report: {str(e)}",
                'confidence_score': 0,
                'raw_response': str(e)
            }
    
    def _extract_confidence_score(self, text: str) -> int:
        """
        Extract confidence score from AI response.
        
        Args:
            text: Generated report text
            
        Returns:
            int: Confidence score (0-100)
        """
        # Look for patterns like "confidence: 85" or "confidence score: 85"
        patterns = [
            r'confidence\s*score\s*:?\s*(\d+)',
            r'confidence\s*:?\s*(\d+)',
            r'score\s*:?\s*(\d+)\s*%',
            r'(\d+)\s*%\s*confidence'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                return min(max(score, 0), 100)  # Clamp between 0-100
        
        # Default confidence if not found
        return 75
    
    def generate_mock_report(self, event_description: str) -> Dict[str, any]:
        """
        Generate a mock report for testing without API calls.
        
        Args:
            event_description: Description of the logistics event
            
        Returns:
            dict: Mock report data
        """
        mock_summary = f"""INCIDENT SUMMARY
Event: {event_description}
Severity: Medium
Status: Active monitoring required

IMPACT ANALYSIS
- Estimated delay: 2-4 hours
- Affected shipments: 1-3 units
- Financial impact: $2,000 - $5,000
- Customer notification: Required

RECOMMENDED ACTIONS
1. Contact carrier for updated ETA
2. Notify affected customers within 1 hour
3. Assess alternative routing options
4. Document incident for insurance purposes
5. Update tracking systems

CONFIDENCE SCORE
This analysis has a confidence score of 82 based on historical incident patterns and current data."""
        
        return {
            'summary': mock_summary,
            'confidence_score': 82,
            'raw_response': mock_summary
        }

    def check_model(self) -> Dict[str, any]:
        """
        Lightweight check to verify the model endpoint exists and the token can access it.

        Returns a dict with status_code and either 'ok' or error message/body.
        """
        try:
            resp = requests.get(self.api_url, headers=self.headers, timeout=10)
            return {
                'status_code': resp.status_code,
                'ok': resp.status_code == 200,
                'body': resp.text
            }
        except requests.exceptions.RequestException as e:
            return {
                'status_code': None,
                'ok': False,
                'body': str(e)
            }


# Example usage and testing
if __name__ == "__main__":
    import json
    
    print("=== Qwen3 Client Test ===\n")
    
    # Initialize client
    client = QwenClient()
    
    # Test event
    test_event = "Truck carrying medical supplies delayed by 3 hours due to highway accident on I-95"
    
    print(f"Event: {test_event}\n")
    print("Generating mock report (for testing without API token)...\n")
    
    # Generate mock report
    report = client.generate_mock_report(test_event)
    
    print("Generated Report:")
    print("-" * 60)
    print(report['summary'])
    print("-" * 60)
    print(f"\nConfidence Score: {report['confidence_score']}")
    
    print("\n\nTo use real API:")
    print("1. Set HUGGINGFACE_API_TOKEN in .env file")
    print("2. Call client.generate_report(event_description)")