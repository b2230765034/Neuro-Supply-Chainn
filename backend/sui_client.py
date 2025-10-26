"""
Sui blockchain client for interacting with smart contracts.
Handles transaction building and submission.
"""
import requests
import json
from typing import Dict, List
from config import Config


class SuiClient:
    """Client for Sui blockchain interactions"""
    
    def __init__(self, rpc_url: str = None):
        """
        Initialize Sui client.
        
        Args:
            rpc_url: Sui RPC endpoint URL
        """
        self.rpc_url = rpc_url or Config.SUI_RPC_URL
        self.package_id = Config.CONTRACT_PACKAGE_ID
        self.module_name = Config.CONTRACT_MODULE_NAME
    
    def call_contract(
        self,
        function_name: str,
        arguments: List,
        type_arguments: List = None
    ) -> Dict:
        """
        Call a Move contract function.
        
        Args:
            function_name: Name of the function to call
            arguments: List of function arguments
            type_arguments: List of type arguments (generics)
            
        Returns:
            dict: Transaction result
        """
        try:
            # Build transaction payload
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "sui_executeTransactionBlock",
                "params": [
                    {
                        "kind": "moveCall",
                        "data": {
                            "packageObjectId": self.package_id,
                            "module": self.module_name,
                            "function": function_name,
                            "arguments": arguments,
                            "typeArguments": type_arguments or []
                        }
                    }
                ]
            }
            
            # For now, return mock response since we need actual deployment
            return self._mock_transaction_response(function_name, arguments)
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def oracle_update(
        self,
        shipment_id: str,
        ai_summary: str,
        confidence_score: int,
        signature: str
    ) -> Dict:
        """
        Call oracle_update function on the smart contract.
        
        Args:
            shipment_id: Unique shipment identifier
            ai_summary: AI-generated report
            confidence_score: Confidence score (0-100)
            signature: Ed25519 signature in hex
            
        Returns:
            dict: Transaction result
        """
        # Convert signature to vector<u8> format for Move
        signature_bytes = [int(signature[i:i+2], 16) for i in range(0, len(signature), 2)]
        
        arguments = [
            shipment_id,
            ai_summary,
            confidence_score,
            signature_bytes
        ]
        
        result = self.call_contract("oracle_update", arguments)
        return result
    
    def get_shipment(self, shipment_id: str) -> Dict:
        """
        Query shipment details from the blockchain.
        
        Args:
            shipment_id: Unique shipment identifier
            
        Returns:
            dict: Shipment data
        """
        try:
            # Build query payload
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "sui_getObject",
                "params": [shipment_id, {"showContent": True}]
            }
            
            # For now, return mock response
            return self._mock_shipment_query(shipment_id)
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _mock_transaction_response(self, function_name: str, arguments: List) -> Dict:
        """Generate mock transaction response for testing"""
        import time
        
        return {
            "success": True,
            "digest": f"0x{'a' * 64}",
            "transaction": {
                "function": function_name,
                "arguments": arguments,
                "timestamp": int(time.time()),
                "status": "success"
            },
            "effects": {
                "status": "success",
                "gasUsed": 1000000
            }
        }
    
    def _mock_shipment_query(self, shipment_id: str) -> Dict:
        """Generate mock shipment query response"""
        import time
        
        return {
            "success": True,
            "data": {
                "shipment_id": shipment_id,
                "ai_summary": "Mock shipment data",
                "confidence_score": 85,
                "timestamp": int(time.time()),
                "status": "active"
            }
        }


# Example usage and testing
if __name__ == "__main__":
    print("=== Sui Client Test ===\n")
    
    # Initialize client
    client = SuiClient()
    
    # Test data
    test_shipment_id = "SHIP-2025-001"
    test_summary = "Shipment delayed due to weather conditions"
    test_confidence = 85
    test_signature = "a" * 128  # Mock signature
    
    print(f"Testing oracle_update...")
    print(f"Shipment ID: {test_shipment_id}")
    print(f"Summary: {test_summary}")
    print(f"Confidence: {test_confidence}\n")
    
    # Call oracle_update
    result = client.oracle_update(
        test_shipment_id,
        test_summary,
        test_confidence,
        test_signature
    )
    
    print("Transaction Result:")
    print(json.dumps(result, indent=2))
    
    print("\n\nNote: This uses mock responses. Real blockchain interaction requires:")
    print("1. Deployed smart contract")
    print("2. Valid Sui wallet with gas")
    print("3. Proper transaction signing")