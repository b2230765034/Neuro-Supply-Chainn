/**
 * Sui blockchain service for wallet connection and contract interaction
 * This is optional for the MVP - the backend handles blockchain interactions
 */

const SUI_NETWORK = import.meta.env.VITE_SUI_NETWORK || 'testnet';
const CONTRACT_PACKAGE_ID = import.meta.env.VITE_CONTRACT_PACKAGE_ID;

class SuiService {
  constructor() {
    this.network = SUI_NETWORK;
    this.packageId = CONTRACT_PACKAGE_ID;
    this.connected = false;
    this.address = null;
  }

  /**
   * Get available wallet (Suishi/Slush or standard Sui wallet)
   */
  getWallet() {
    if (typeof window === 'undefined') return null;
    
    // Check for Suishi (Slush) wallet first
    if (window.suishi) {
      return window.suishi;
    }
    
    // Check for standard Sui wallet
    if (window.suiWallet) {
      return window.suiWallet;
    }
    
    return null;
  }

  /**
   * Check if any Sui wallet is installed
   */
  isWalletInstalled() {
    return this.getWallet() !== null;
  }

  /**
   * Get wallet name for display
   */
  getWalletName() {
    if (typeof window === 'undefined') return 'Unknown';
    
    if (window.suishi) return 'Suishi Wallet';
    if (window.suiWallet) return 'Sui Wallet';
    
    return 'Unknown';
  }

  /**
   * Connect to Sui wallet (Suishi/Slush or standard)
   */
  async connect() {
    try {
      const wallet = this.getWallet();
      
      if (!wallet) {
        throw new Error('No Sui wallet detected. Please install Suishi Wallet or Sui Wallet extension.');
      }

      console.log(`Connecting to ${this.getWalletName()}...`);

      // Different wallets may have different connection methods
      let accounts;
      
      // Try Suishi/Slush wallet connection
      if (window.suishi) {
        try {
          // Suishi wallet connection
          const response = await wallet.connect();
          accounts = response?.accounts || [];
        } catch (e) {
          // Fallback to requestPermissions
          accounts = await wallet.requestPermissions();
        }
      } else {
        // Standard Sui wallet connection
        accounts = await wallet.requestPermissions();
      }
      
      if (accounts && accounts.length > 0) {
        this.address = accounts[0];
        this.connected = true;
        console.log('Connected to address:', this.address);
        return {
          success: true,
          address: this.address,
          wallet: this.getWalletName()
        };
      }

      throw new Error('No accounts found in wallet');
    } catch (error) {
      console.error('Error connecting to wallet:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Disconnect wallet
   */
  disconnect() {
    this.connected = false;
    this.address = null;
  }

  /**
   * Get current wallet address
   */
  getAddress() {
    return this.address;
  }

  /**
   * Check if wallet is connected
   */
  isConnected() {
    return this.connected;
  }

  /**
   * Query shipment from blockchain
   * @param {string} shipmentObjectId - The object ID of the shipment
   */
  async queryShipment(shipmentObjectId) {
    try {
      // This would use @mysten/sui.js in production
      // For MVP, we use the backend API instead
      console.log('Querying shipment:', shipmentObjectId);
      
      // Mock response for frontend-only testing
      return {
        success: true,
        data: {
          shipmentId: shipmentObjectId,
          summary: 'Shipment data from blockchain',
          confidenceScore: 85,
          timestamp: Date.now()
        }
      };
    } catch (error) {
      console.error('Error querying shipment:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get transaction details
   * @param {string} digest - Transaction digest/hash
   */
  async getTransaction(digest) {
    try {
      const explorerUrl = this.getExplorerUrl(digest);
      
      return {
        success: true,
        digest,
        explorerUrl,
        status: 'confirmed'
      };
    } catch (error) {
      console.error('Error getting transaction:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get explorer URL for transaction
   */
  getExplorerUrl(digest) {
    const baseUrl = this.network === 'mainnet' 
      ? 'https://suiexplorer.com'
      : 'https://suiexplorer.com/?network=testnet';
    
    return `${baseUrl}/txblock/${digest}`;
  }

  /**
   * Get explorer URL for object
   */
  getObjectExplorerUrl(objectId) {
    const baseUrl = this.network === 'mainnet' 
      ? 'https://suiexplorer.com'
      : 'https://suiexplorer.com/?network=testnet';
    
    return `${baseUrl}/object/${objectId}`;
  }

  /**
   * Format address for display
   */
  formatAddress(address) {
    if (!address) return '';
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  }

  /**
   * Get network info
   */
  getNetworkInfo() {
    return {
      network: this.network,
      rpcUrl: this.getRpcUrl(),
      explorerUrl: this.network === 'mainnet'
        ? 'https://suiexplorer.com'
        : 'https://suiexplorer.com/?network=testnet'
    };
  }

  /**
   * Get RPC URL for current network
   */
  getRpcUrl() {
    switch (this.network) {
      case 'mainnet':
        return 'https://fullnode.mainnet.sui.io:443';
      case 'testnet':
        return 'https://fullnode.testnet.sui.io:443';
      case 'devnet':
        return 'https://fullnode.devnet.sui.io:443';
      default:
        return 'https://fullnode.testnet.sui.io:443';
    }
  }
}

// Export singleton instance
export default new SuiService();