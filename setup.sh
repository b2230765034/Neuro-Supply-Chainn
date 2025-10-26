#!/bin/bash

# Setup script for Neuro-Generative Supply Chain Optimizer
# Automates environment setup for hackathon development

echo "=========================================="
echo "Neuro-Generative Supply Chain Optimizer"
echo "Hackathon Setup Script"
echo "=========================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
echo ""

# Check Node.js version
echo "Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"
echo ""

# Setup Backend
echo "=========================================="
echo "Setting up Backend (Python)"
echo "=========================================="
echo ""

cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp ../.env.example .env
    echo -e "${YELLOW}⚠ Please edit backend/.env and add your configuration${NC}"
    echo -e "${YELLOW}  Required: HUGGINGFACE_API_TOKEN${NC}"
else
    echo -e "${YELLOW}.env file already exists${NC}"
fi
echo ""

# Generate oracle keypair
echo "Generating Oracle Ed25519 keypair..."
python3 << EOF
from crypto_utils import CryptoUtils
private_key, public_key = CryptoUtils.generate_keypair()
print(f"\nOracle Keypair Generated:")
print(f"Private Key: {private_key}")
print(f"Public Key: {public_key}")
print(f"\nAdd this to your .env file:")
print(f"ORACLE_PRIVATE_KEY={private_key}")
EOF
echo ""

cd ..

# Setup Frontend
echo "=========================================="
echo "Setting up Frontend (React + Vite)"
echo "=========================================="
echo ""

cd frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
    echo -e "${GREEN}✓ Node.js dependencies installed${NC}"
else
    echo -e "${YELLOW}node_modules already exists, skipping install${NC}"
fi
echo ""

cd ..

# Setup Smart Contract
echo "=========================================="
echo "Smart Contract Setup"
echo "=========================================="
echo ""

if command -v sui &> /dev/null; then
    echo -e "${GREEN}✓ Sui CLI found${NC}"
    echo "To deploy the contract:"
    echo "  1. cd contracts"
    echo "  2. sui move build"
    echo "  3. sui client publish --gas-budget 100000000"
    echo "  4. Copy the Package ID to .env as CONTRACT_PACKAGE_ID"
else
    echo -e "${YELLOW}⚠ Sui CLI not found${NC}"
    echo "Install from: https://docs.sui.io/build/install"
fi
echo ""

# Final instructions
echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "Quick Start Guide:"
echo ""
echo "1. Configure environment variables:"
echo "   Edit backend/.env and add:"
echo "   - HUGGINGFACE_API_TOKEN=your_token_here"
echo "   - ORACLE_PRIVATE_KEY=generated_key_above"
echo ""
echo "2. Test the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python test_flow.py"
echo ""
echo "3. Start the API server:"
echo "   python server.py"
echo ""
echo "4. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "5. Open http://localhost:5173 in your browser"
echo ""
echo "Optional: Deploy smart contract"
echo "   cd contracts"
echo "   ./deploy.sh"
echo ""
echo "For more information, see README.md"
echo ""