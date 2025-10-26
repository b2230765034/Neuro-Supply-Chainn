#!/bin/bash

# Deployment script for Sui Move smart contract
# Make sure you have Sui CLI installed and configured

echo "=========================================="
echo "Supply Chain Smart Contract Deployment"
echo "=========================================="
echo ""

# Check if sui CLI is installed
if ! command -v sui &> /dev/null
then
    echo "Error: Sui CLI not found. Please install it first."
    echo "Visit: https://docs.sui.io/build/install"
    exit 1
fi

# Check active address
echo "Checking active Sui address..."
sui client active-address
echo ""

# Check gas balance
echo "Checking gas balance..."
sui client gas
echo ""

# Build the contract
echo "Building Move contract..."
sui move build
if [ $? -ne 0 ]; then
    echo "Error: Build failed"
    exit 1
fi
echo "Build successful!"
echo ""

# Publish the contract
echo "Publishing contract to Sui network..."
echo "This will consume gas. Continue? (y/n)"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    sui client publish --gas-budget 100000000
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "Deployment Successful!"
        echo "=========================================="
        echo ""
        echo "IMPORTANT: Save the following information:"
        echo "1. Package ID - Add to .env as CONTRACT_PACKAGE_ID"
        echo "2. Copy the ShipmentRegistry object ID for queries"
        echo ""
        echo "Next steps:"
        echo "1. Update backend/.env with CONTRACT_PACKAGE_ID"
        echo "2. Update frontend config with package ID"
        echo "3. Test the oracle service"
    else
        echo "Deployment failed!"
        exit 1
    fi
else
    echo "Deployment cancelled"
    exit 0
fi