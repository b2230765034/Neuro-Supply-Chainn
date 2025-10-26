"""
End-to-end integration test for the oracle service.
Tests the complete flow: Event → AI Generation → Signing → Blockchain Update
"""
import json
import time
from oracle import OracleService

def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def print_result(label, value, indent=0):
    """Print formatted result"""
    prefix = "  " * indent
    print(f"{prefix}{label}: {value}")

def test_complete_flow():
    """Test the complete oracle flow"""
    
    print_section("NEURO-GENERATIVE SUPPLY CHAIN OPTIMIZER - Integration Test")
    
    # Initialize oracle
    print("Initializing Oracle Service...")
    oracle = OracleService(use_mock_ai=True)
    print("✓ Oracle initialized\n")
    
    # Get oracle info
    info = oracle.get_oracle_info()
    print("Oracle Configuration:")
    for key, value in info.items():
        print_result(key, value, indent=1)
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Highway Accident Delay",
            "event": "Truck carrying medical supplies delayed by 4 hours due to multi-vehicle accident on I-95 near Baltimore",
            "shipment_id": "SHIP-TEST-001"
        },
        {
            "name": "Port Congestion",
            "event": "Container ship delayed 36 hours at Port of Los Angeles due to severe congestion and labor shortage",
            "shipment_id": "SHIP-TEST-002"
        },
        {
            "name": "Weather Event",
            "event": "Severe winter storm causing widespread delivery delays across midwest region, affecting 50+ shipments",
            "shipment_id": None  # Test auto-generation
        }
    ]
    
    results = []
    
    for idx, scenario in enumerate(test_scenarios, 1):
        print_section(f"Test Scenario {idx}: {scenario['name']}")
        
        print(f"Event: {scenario['event']}")
        if scenario['shipment_id']:
            print(f"Shipment ID: {scenario['shipment_id']}\n")
        else:
            print("Shipment ID: (auto-generate)\n")
        
        # Process event
        start_time = time.time()
        result = oracle.process_event(
            event_description=scenario['event'],
            shipment_id=scenario['shipment_id']
        )
        end_time = time.time()
        
        # Display results
        if result['success']:
            print("✓ Processing Successful!\n")
            
            print("Results:")
            print_result("Shipment ID", result['shipment_id'], indent=1)
            print_result("Processing Time", f"{result['processing_time']}s", indent=1)
            print_result("Confidence Score", f"{result['ai_report']['confidence_score']}%", indent=1)
            
            print("\n  AI Report Summary:")
            summary_lines = result['ai_report']['summary'].split('\n')
            for line in summary_lines[:5]:  # Show first 5 lines
                if line.strip():
                    print(f"    {line}")
            if len(summary_lines) > 5:
                print(f"    ... ({len(summary_lines) - 5} more lines)")
            
            print("\n  Blockchain Transaction:")
            tx = result['transaction']
            print_result("Status", "✓ Confirmed" if tx.get('success') else "✗ Failed", indent=2)
            print_result("Digest", tx.get('digest', 'N/A')[:32] + "...", indent=2)
            
            print("\n  Cryptographic Signature:")
            print_result("Length", len(result['signature']), indent=2)
            print_result("Preview", result['signature'][:32] + "...", indent=2)
            
            results.append({
                "scenario": scenario['name'],
                "success": True,
                "shipment_id": result['shipment_id'],
                "confidence": result['ai_report']['confidence_score'],
                "time": result['processing_time']
            })
        else:
            print(f"✗ Processing Failed: {result.get('error', 'Unknown error')}")
            results.append({
                "scenario": scenario['name'],
                "success": False,
                "error": result.get('error')
            })
        
        # Small delay between tests
        if idx < len(test_scenarios):
            time.sleep(1)
    
    # Summary
    print_section("Test Summary")
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"Tests Run: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Success Rate: {(successful/total)*100:.1f}%\n")
    
    print("Individual Results:")
    for result in results:
        status = "✓" if result['success'] else "✗"
        print(f"  {status} {result['scenario']}")
        if result['success']:
            print(f"      Shipment: {result['shipment_id']}")
            print(f"      Confidence: {result['confidence']}%")
            print(f"      Time: {result['time']}s")
        else:
            print(f"      Error: {result.get('error', 'Unknown')}")
    
    print_section("Test Complete")
    
    print("Next Steps:")
    print("  1. Review oracle.log for detailed execution logs")
    print("  2. Deploy smart contract: cd contracts && ./deploy.sh")
    print("  3. Update CONTRACT_PACKAGE_ID in .env")
    print("  4. Start API server: python server.py")
    print("  5. Launch frontend: cd ../frontend && npm run dev")
    print("\nDemo Ready! 🎉\n")
    
    return results

if __name__ == "__main__":
    try:
        test_complete_flow()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()