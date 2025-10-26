"""
Main oracle service that orchestrates the entire flow:
1. Receive event description
2. Generate AI report via Qwen3
3. Sign the report with Ed25519
4. Submit to Sui blockchain
"""
import json
import time
import logging
from typing import Dict
from datetime import datetime

from config import Config
from qwen_client import QwenClient
from crypto_utils import CryptoUtils
from sui_client import SuiClient


# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class OracleService:
    """Main oracle service for supply chain optimization"""
    
    def __init__(self, use_mock_ai: bool = False):
        """
        Initialize oracle service.
        
        Args:
            use_mock_ai: If True, use mock AI responses (for testing without API token)
        """
        if Config.LLM_TYPE == 'local':
            from local_llm_client import LocalLLMClient
            self.llm_client = LocalLLMClient()
        else:
            from qwen_client import QwenClient
            self.llm_client = QwenClient()
            
        self.sui_client = SuiClient()
        self.use_mock_ai = use_mock_ai
        
        # Generate or load oracle keypair
        if Config.ORACLE_PRIVATE_KEY:
            self.private_key = Config.ORACLE_PRIVATE_KEY
            logger.info("Loaded oracle private key from config")
        else:
            self.private_key, self.public_key = CryptoUtils.generate_keypair()
            logger.warning("Generated new oracle keypair (should be saved for production)")
            logger.info(f"Public Key: {self.public_key}")
        
        logger.info("Oracle service initialized")
    
    def process_event(self, event_description: str, shipment_id: str = None) -> Dict:
        """
        Process a logistics event end-to-end.
        
        Args:
            event_description: Description of the logistics event
            shipment_id: Optional shipment ID (auto-generated if not provided)
            
        Returns:
            dict: Complete processing result including transaction details
        """
        start_time = time.time()
        
        # Generate shipment ID if not provided
        if not shipment_id:
            shipment_id = self._generate_shipment_id()
        
        logger.info(f"Processing event for shipment: {shipment_id}")
        logger.info(f"Event: {event_description}")
        
        try:
            # Step 1: Generate AI report
            logger.info("Step 1: Generating AI report...")
            if self.use_mock_ai:
                ai_result = self.llm_client.generate_mock_report(event_description) if hasattr(self.llm_client, 'generate_mock_report') else {
                    'summary': 'Mock report not available',
                    'confidence_score': 0,
                    'raw_response': ''
                }
            else:
                ai_result = self.llm_client.generate_report(event_description)
            
            ai_summary = ai_result['summary']
            confidence_score = ai_result['confidence_score']
            
            logger.info(f"AI report generated (confidence: {confidence_score})")
            
            # Step 2: Create and sign payload
            logger.info("Step 2: Signing report...")
            payload = CryptoUtils.create_report_payload(
                shipment_id,
                ai_summary,
                confidence_score
            )
            signature = CryptoUtils.sign_message(payload, self.private_key)
            logger.info("Report signed successfully")
            
            # Step 3: Submit to blockchain
            logger.info("Step 3: Submitting to Sui blockchain...")
            tx_result = self.sui_client.oracle_update(
                shipment_id,
                ai_summary,
                confidence_score,
                signature
            )
            
            if tx_result.get('success'):
                logger.info(f"Transaction successful: {tx_result.get('digest', 'N/A')}")
            else:
                logger.error(f"Transaction failed: {tx_result.get('error', 'Unknown error')}")
            
            # Compile complete result
            processing_time = time.time() - start_time
            
            result = {
                'success': tx_result.get('success', False),
                'shipment_id': shipment_id,
                'event_description': event_description,
                'ai_report': {
                    'summary': ai_summary,
                    'confidence_score': confidence_score
                },
                'signature': signature,
                'transaction': tx_result,
                'processing_time': round(processing_time, 2),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            logger.info(f"Event processed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error processing event: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'shipment_id': shipment_id,
                'event_description': event_description,
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def query_shipment(self, shipment_id: str) -> Dict:
        """
        Query shipment details from blockchain.
        
        Args:
            shipment_id: Shipment identifier
            
        Returns:
            dict: Shipment data
        """
        logger.info(f"Querying shipment: {shipment_id}")
        result = self.sui_client.get_shipment(shipment_id)
        return result
    
    def _generate_shipment_id(self) -> str:
        """Generate a unique shipment ID"""
        timestamp = int(time.time())
        return f"SHIP-{timestamp}"
    
    def get_oracle_info(self) -> Dict:
        """Get oracle service information"""
        return {
            'status': 'active',
            'network': Config.SUI_NETWORK,
            'contract_package': Config.CONTRACT_PACKAGE_ID or 'Not configured',
            'ai_model': Config.LOCAL_LLM_MODEL if Config.LLM_TYPE == 'local' else Config.QWEN_MODEL,
            'use_mock_ai': self.use_mock_ai
        }


# CLI interface for testing
def main():
    """Command-line interface for testing the oracle"""
    print("=" * 70)
    print("NEURO-GENERATIVE SUPPLY CHAIN OPTIMIZER - Oracle Service")
    print("=" * 70)
    print()
    
    # Initialize oracle with mock AI (no API token required for testing)
    oracle = OracleService(use_mock_ai=True)
    
    # Get oracle info
    info = oracle.get_oracle_info()
    print("Oracle Info:")
    print(json.dumps(info, indent=2))
    print()
    
    # Test scenarios
    test_events = [
        "Truck carrying electronics delayed by 3 hours due to highway accident on I-95",
        "Shipment of medical supplies stuck at port due to customs inspection",
        "Severe weather conditions causing delivery delays in midwest region"
    ]
    
    print("Running Test Scenarios:")
    print("-" * 70)
    
    for idx, event in enumerate(test_events, 1):
        print(f"\n[Test {idx}] Event: {event}\n")
        
        result = oracle.process_event(event)
        
        if result['success']:
            print(f"✓ Success!")
            print(f"  Shipment ID: {result['shipment_id']}")
            print(f"  Confidence: {result['ai_report']['confidence_score']}")
            print(f"  Processing Time: {result['processing_time']}s")
            print(f"  Transaction: {result['transaction'].get('digest', 'N/A')[:32]}...")
        else:
            print(f"✗ Failed: {result.get('error', 'Unknown error')}")
        
        print()
    
    print("=" * 70)
    print("Test completed. Check oracle.log for detailed logs.")
    print()
    print("Next steps:")
    print("1. Deploy the Move smart contract (see contracts/)")
    print("2. Set CONTRACT_PACKAGE_ID in .env")
    print("3. Add HUGGINGFACE_API_TOKEN for real AI generation")
    print("4. Run the frontend to interact with the oracle")


if __name__ == "__main__":
    main()