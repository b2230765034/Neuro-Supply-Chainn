"""
Cryptographic utilities for Ed25519 signing.
Provides key generation, signing, and verification for oracle reports.
"""
import hashlib
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder
import binascii


class CryptoUtils:
    """Ed25519 cryptographic operations"""
    
    @staticmethod
    def generate_keypair():
        """
        Generate a new Ed25519 keypair.
        
        Returns:
            tuple: (private_key_hex, public_key_hex)
        """
        signing_key = SigningKey.generate()
        verify_key = signing_key.verify_key
        
        private_key_hex = signing_key.encode(encoder=HexEncoder).decode('utf-8')
        public_key_hex = verify_key.encode(encoder=HexEncoder).decode('utf-8')
        
        return private_key_hex, public_key_hex
    
    @staticmethod
    def sign_message(message: str, private_key_hex: str) -> str:
        """
        Sign a message using Ed25519.
        
        Args:
            message: The message to sign
            private_key_hex: Private key in hex format
            
        Returns:
            str: Signature in hex format
        """
        try:
            # Load private key
            signing_key = SigningKey(private_key_hex, encoder=HexEncoder)
            
            # Create message hash for signing
            message_bytes = message.encode('utf-8')
            message_hash = hashlib.sha256(message_bytes).digest()
            
            # Sign the hash
            signed = signing_key.sign(message_hash)
            signature_hex = binascii.hexlify(signed.signature).decode('utf-8')
            
            return signature_hex
            
        except Exception as e:
            raise ValueError(f"Failed to sign message: {str(e)}")
    
    @staticmethod
    def verify_signature(message: str, signature_hex: str, public_key_hex: str) -> bool:
        """
        Verify a signature using Ed25519.
        
        Args:
            message: The original message
            signature_hex: Signature in hex format
            public_key_hex: Public key in hex format
            
        Returns:
            bool: True if signature is valid
        """
        try:
            # Load public key
            verify_key = VerifyKey(public_key_hex, encoder=HexEncoder)
            
            # Create message hash
            message_bytes = message.encode('utf-8')
            message_hash = hashlib.sha256(message_bytes).digest()
            
            # Convert signature to bytes
            signature_bytes = binascii.unhexlify(signature_hex)
            
            # Verify signature
            verify_key.verify(message_hash, signature_bytes)
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def create_report_payload(shipment_id: str, ai_summary: str, confidence_score: int) -> str:
        """
        Create a canonical payload string for signing.
        
        Args:
            shipment_id: Unique shipment identifier
            ai_summary: AI-generated report text
            confidence_score: Confidence score (0-100)
            
        Returns:
            str: Canonical payload string
        """
        # Create deterministic payload for signing
        payload = f"{shipment_id}|{ai_summary}|{confidence_score}"
        return payload


# Example usage and testing
if __name__ == "__main__":
    print("=== Ed25519 Crypto Utilities Test ===\n")
    
    # Generate keypair
    private_key, public_key = CryptoUtils.generate_keypair()
    print(f"Generated Private Key: {private_key}")
    print(f"Generated Public Key: {public_key}\n")

    # Create test payload
    test_shipment_id = "SHIP-2025-001"
    test_summary = "Shipment delayed due to weather conditions"
    test_confidence = 85
    
    payload = CryptoUtils.create_report_payload(
        test_shipment_id, 
        test_summary, 
        test_confidence
    )
    print(f"Payload: {payload}\n")
    
    # Sign payload
    signature = CryptoUtils.sign_message(payload, private_key)
    print(f"Signature: {signature[:32]}...\n")
    
    # Verify signature
    is_valid = CryptoUtils.verify_signature(payload, signature, public_key)
    print(f"Signature Valid: {is_valid}\n")
    
    # Test with wrong message
    wrong_payload = "SHIP-2025-002|Different message|90"
    is_valid_wrong = CryptoUtils.verify_signature(wrong_payload, signature, public_key)
    print(f"Wrong Message Valid: {is_valid_wrong}")