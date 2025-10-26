"""
Configuration management for the oracle service.
Loads environment variables and provides centralized config access.
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Centralized configuration class"""
    
    # LLM Configuration
    LLM_TYPE = os.getenv('LLM_TYPE', 'local')  # 'local' or 'huggingface'
    LOCAL_LLM_URL = os.getenv('LOCAL_LLM_URL', 'http://localhost:11434')  # Ollama default port
    LOCAL_LLM_MODEL = os.getenv('LOCAL_LLM_MODEL', 'qwen3:1.7b')
    LLM_MAX_TOKENS = int(os.getenv('LLM_MAX_TOKENS', '500'))  # Reduced max tokens
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', '0.5'))
    
    # Hugging Face Configuration (fallback)
    HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')
    # Use a smaller instruct model by default for faster inference on Hugging Face
    QWEN_MODEL = os.getenv('QWEN_MODEL', 'Qwen/Qwen2.5-7B-Instruct')
    QWEN_MAX_TOKENS = int(os.getenv('QWEN_MAX_TOKENS', '1000'))
    QWEN_TEMPERATURE = float(os.getenv('QWEN_TEMPERATURE', '0.7'))
    
    # Sui Blockchain Configuration
    SUI_RPC_URL = os.getenv('SUI_RPC_URL', 'https://fullnode.testnet.sui.io:443')
    SUI_NETWORK = os.getenv('SUI_NETWORK', 'testnet')
    
    # Oracle Configuration
    ORACLE_PRIVATE_KEY = os.getenv('ORACLE_PRIVATE_KEY')
    ORACLE_ADDRESS = os.getenv('ORACLE_ADDRESS')
    
    # Smart Contract Configuration
    CONTRACT_PACKAGE_ID = os.getenv('CONTRACT_PACKAGE_ID')
    CONTRACT_MODULE_NAME = os.getenv('CONTRACT_MODULE_NAME', 'supply_chain')
    
    # Backend Server Configuration
    BACKEND_HOST = os.getenv('BACKEND_HOST', '0.0.0.0')
    BACKEND_PORT = int(os.getenv('BACKEND_PORT', '8000'))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'oracle.log')
    
    @classmethod
    def validate(cls):
        """Validate required configuration values"""
        required_fields = [
            ('HUGGINGFACE_API_TOKEN', cls.HUGGINGFACE_API_TOKEN),
        ]
        
        missing = [field for field, value in required_fields if not value]
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        return True
    
    @classmethod
    def get_prompt_template(cls):
        """Return the prompt template for Qwen3"""
        return """Analyze this supply chain event and provide a detailed report. End your analysis with a confidence score.

EVENT: {event_description}

Format your response exactly as follows:

SUMMARY:
[Provide a brief overview]
Severity: [Low/Medium/High]

IMPACT ANALYSIS:
- Delay Duration: [Specify expected delays]
- Cost Impact: [Estimate financial impact]
- Affected Areas: [List affected operations]

RECOMMENDED ACTIONS:
1. [Most urgent action]
2. [Second priority]
3. [Additional step if needed]

End your response with one line showing your confidence score like this:
Confidence: [X] (where X is a number between 0-100)"""

# Initialize config validation at import
try:
    Config.validate()
except ValueError as e:
    print(f"Configuration Warning: {e}")
    print("Some features may not work without proper configuration.")