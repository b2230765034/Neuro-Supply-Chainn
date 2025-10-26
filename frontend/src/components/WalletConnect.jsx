import { ConnectButton, useCurrentAccount } from '@mysten/dapp-kit';
import { Wallet } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function WalletConnect() {
  const currentAccount = useCurrentAccount();
  const [showFullAddress, setShowFullAddress] = useState(false);

  // Custom component to show address with toggle
  const AddressDisplay = ({ account }) => {
    return (
      <div 
        style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '8px',
          cursor: 'pointer',
          padding: '8px 12px',
          background: 'var(--bg-secondary)',
          borderRadius: '8px',
          fontSize: '14px'
        }}
        onClick={() => setShowFullAddress(!showFullAddress)}
        title="Click to toggle full address"
      >
        <Wallet size={18} />
        <div style={{ 
          whiteSpace: 'nowrap',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          maxWidth: showFullAddress ? 'none' : '150px'
        }}>
          {account.address}
        </div>
      </div>
    );
  };
  
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
        displayAccount={AddressDisplay}
      />
      {currentAccount && showFullAddress && (
        <div style={{
          position: 'absolute',
          top: '100%',
          right: '0',
          marginTop: '8px',
          padding: '12px',
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border)',
          borderRadius: '8px',
          zIndex: 1000,
          maxWidth: '400px',
          wordBreak: 'break-all'
        }}>
          <strong>Full Address:</strong><br/>
          {currentAccount.address}
        </div>
      )}
    </div>
  );
}