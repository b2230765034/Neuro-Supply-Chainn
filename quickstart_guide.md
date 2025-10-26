# Quick Start Guide - Neuro-Generative Supply Chain Optimizer

Get the demo running in **5 minutes** for your hackathon presentation!

## ⚡ Fastest Path (No External APIs Required)

### Step 1: Setup (2 minutes)

```bash
# Clone and setup
git clone <your-repo>
cd neuro-supply-chain

# Run automated setup
chmod +x setup.sh
./setup.sh
```

### Step 2: Start Backend (1 minute)

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run quick test
python test_flow.py

# Start API server
python server.py
```

Backend will run on http://localhost:8000

### Step 3: Start Frontend (1 minute)

Open a **new terminal**:

```bash
cd frontend
npm run dev
```

Frontend will open at http://localhost:5173

### Step 4: Demo! (1 minute)

1. Open http://localhost:5173
2. Click any example event or type your own
3. Click "Generate AI Report"
4. Watch the magic happen! ✨

## 🎯 Demo Scenarios

### Scenario 1: Highway Accident
```
Truck carrying electronics delayed by 3 hours due to highway accident on I-95
```
**What to highlight:**
- AI generates detailed incident analysis
- Confidence score assessment
- Cryptographic signing
- Mock blockchain transaction

### Scenario 2: Port Congestion
```
Container ship waiting 48 hours at Los Angeles port due to congestion
```
**What to highlight:**
- Real-world logistics problem
- AI-powered recommendations
- Immutable on-chain recording
- Transparent oracle process

### Scenario 3: Weather Event
```
Severe snowstorm causing delivery delays across midwest region
```
**What to highlight:**
- Multi-shipment impact analysis
- Proactive alerts
- Decentralized verification
- Supply chain optimization

## 🔧 Configuration (Optional)

### For Real AI Generation

1. Get Hugging Face API token: https://huggingface.co/settings/tokens

2. Edit `backend/.env`:
```env
HUGGINGFACE_API_TOKEN=hf_your_token_here
```

3. In `backend/server.py`, change:
```python
oracle = OracleService(use_mock_ai=False)
```

4. Restart server

### For Real Blockchain Deployment

1. Install Sui CLI: https://docs.sui.io/build/install

2. Deploy contract:
```bash
cd contracts
sui move build
sui client publish --gas-budget 100000000
```

3. Copy Package ID to `backend/.env`:
```env
CONTRACT_PACKAGE_ID=0x...
```

4. Update `backend/sui_client.py` with real transaction logic

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python3 --version` (need 3.10+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check port 8000 is free: `lsof -i :8000`

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check port 5173 is free

### "Module not found" errors
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt` again

### No AI response
- This is expected! The demo uses mock AI by default
- Mock responses are pre-generated and work without API tokens
- To use real AI, add your Hugging Face token

## 📊 Demo Talking Points

### Technical Architecture
- **Off-chain Oracle**: Python service with Ed25519 signing
- **AI Model**: Qwen3 (72B parameters) via Hugging Face
- **Smart Contract**: Sui Move for immutable record keeping
- **Frontend**: React with real-time updates

### Key Innovations
1. **AI-Powered Analysis**: Real-time logistics intelligence
2. **Cryptographic Verification**: Ed25519 signatures ensure data integrity
3. **Blockchain Transparency**: Immutable audit trail
4. **Scalable Architecture**: Microservices design

### Use Cases
- **Real-time incident response**
- **Automated insurance claims**
- **Supply chain optimization**
- **Regulatory compliance**
- **Multi-party transparency**

## 🎥 Demo Flow

1. **Introduction** (30s)
   - "We built an AI-powered supply chain oracle on blockchain"
   - Show the dashboard

2. **Submit Event** (30s)
   - Select or type a logistics event
   - Explain the problem it solves

3. **Show AI Analysis** (45s)
   - Highlight the generated report
   - Point out confidence score
   - Explain recommendations

4. **Blockchain Integration** (30s)
   - Show transaction confirmation
   - Explain cryptographic signing
   - Mention immutability

5. **Technical Deep Dive** (Optional, 1-2min)
   - Show code structure
   - Explain oracle mechanism
   - Discuss Move contract

## 📦 What's Included

```
✓ Working backend oracle service
✓ Mock AI responses (no API key needed)
✓ Cryptographic signing (Ed25519)
✓ Move smart contract (ready to deploy)
✓ Beautiful React frontend
✓ Integration tests
✓ Comprehensive documentation
```

## 🚀 Production Considerations

For a production deployment, you would need:

- [ ] Real Hugging Face API token
- [ ] Deploy to Sui mainnet
- [ ] Multi-oracle consensus
- [ ] Rate limiting and auth
- [ ] Monitoring and alerts
- [ ] Error recovery mechanisms
- [ ] Database for historical data
- [ ] Load balancing

## 📞 Support

Check `oracle.log` for detailed execution logs

**Built in 24 hours for hackathon** 🏆
