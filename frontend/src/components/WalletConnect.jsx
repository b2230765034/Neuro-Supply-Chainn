import { ConnectButton } from '@mysten/dapp-kit';
import { Wallet } from 'lucide-react';

export default function WalletConnect() {
  return (
    <div className="wallet-container">
      <ConnectButton 
        className="button button-secondary wallet-connect-button"
        connectText={
          <>
            <Wallet size={18} />
            Connect Wallet
          </>
        }
      />
    </div>
  );
}