# Neuro-Generative Supply Chain Optimizer

**A hackathon project combining GenAI and Blockchain for intelligent supply chain management**

## 🎯 Overview

This project demonstrates how AI-generated logistics insights can be trustlessly recorded on-chain. When supply chain events occur (delays, accidents, weather disruptions), our system:

1. **Generates** an AI-powered incident report using Qwen3
2. **Signs** the report with cryptographic verification
3. **Records** the analysis on Sui blockchain via smart contract
4. **Displays** real-time updates on a web dashboard

## 🏗️ Architecture

```
User Event Input → Oracle Service (Python) → Qwen3 AI → Sign Report → Sui Smart Contract → Frontend Display
```

### Components

- **Backend Oracle**: Python service that orchestrates AI generation and blockchain updates
- **Qwen3 AI**: Generates realistic logistics reports and recommendations
- **Sui Smart Contract**: Stores immutable shipment records on-chain
- **React Frontend**: Interactive dashboard for event submission and monitoring

## 📦 Tech Stack

- **AI Model**: Qwen3 via Hugging Face Inference API
- **Blockchain**: Sui (Move language)
- **Backend**: Python 3.10+ (FastAPI optional for production)
- **Frontend**: React 18 + Vite
- **Crypto**: Ed25519 signatures

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Sui CLI (for contract deployment)
- Hugging Face API token

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Run oracle service
python oracle.py
```

### Smart Contract Deployment

```bash
cd contracts
sui move build
sui client publish --gas-budget 100000000
# Note the package ID for frontend configuration
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

## 📝 Usage

# ollama run qwen3:1.7b

# cd backend
# python server.py

# cd frontend
# npm run dev


1. **Submit Event**: Enter a logistics event description (e.g., "Truck carrying electronics delayed by 3 hours due to highway accident")

2. **AI Processing**: Qwen3 generates:
   - Detailed incident analysis
   - Impact assessment
   - Recommended actions
   - Confidence score

3. **On-Chain Recording**: Oracle signs and submits to Sui blockchain

4. **View Results**: Dashboard shows report and transaction confirmation

## 🔧 Configuration

### Environment Variables

```env
# Backend (.env)
HUGGINGFACE_API_TOKEN=your_token_here
SUI_RPC_URL=https://fullnode.testnet.sui.io:443
ORACLE_PRIVATE_KEY=your_ed25519_key_here
CONTRACT_PACKAGE_ID=0x...
CONTRACT_MODULE_NAME=supply_chain

# Frontend (.env)
VITE_BACKEND_URL=http://localhost:8000
VITE_SUI_NETWORK=testnet
```

## 📊 Smart Contract Interface

### Shipment Object
```move
struct Shipment {
    id: UID,
    shipment_id: String,
    ai_summary: String,
    confidence_score: u64,
    timestamp: u64,
    oracle_signature: vector<u8>
}
```

### Entry Functions
- `oracle_update(shipment_id, ai_summary, confidence_score, signature)`
- `get_shipment(shipment_id)` - Query shipment details

## 🎨 Demo Scenarios

### Scenario 1: Weather Delay
**Input**: "Shipment delayed due to severe snowstorm in Denver region"  
**AI Output**: Impact analysis, rerouting suggestions, customer notification templates

### Scenario 2: Accident
**Input**: "Truck collision on I-95, cargo intact but 6-hour delay expected"  
**AI Output**: Alternative transport options, insurance claim guidance, ETA recalculation

### Scenario 3: Port Congestion
**Input**: "Container ship waiting 48 hours at Los Angeles port"  
**AI Output**: Congestion analysis, cost implications, alternative port recommendations

## 🐛 Debugging

Run integration test:
```bash
python backend/test_flow.py
```

Check logs:
```bash
tail -f backend/oracle.log
```

Verify contract state:
```bash
sui client object <SHIPMENT_OBJECT_ID>
```

## 📈 Future Enhancements

- [ ] Multi-oracle consensus mechanism
- [ ] ML model fine-tuning on logistics data
- [ ] Real-time IoT sensor integration
- [ ] Automated insurance claim triggers
- [ ] Advanced analytics dashboard
- [ ] Mobile app support

## 🏆 Hackathon Notes

**Built in 24 hours** - This is an MVP demonstrating core concepts. Production deployment would require:
- Oracle network redundancy
- Enhanced security audits
- Rate limiting and scaling
- Comprehensive error handling
- User authentication

## 📄 License

MIT License - Built for educational and hackathon purposes

## 👥 Team

Built with ☕ and 🧠 for [Your Hackathon Name]

---

**Status**: 🚧 MVP Complete | 🎯 Demo Ready
