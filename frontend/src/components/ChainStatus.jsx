import { Activity, Database, Cpu, Network } from 'lucide-react';

export default function ChainStatus({ oracleStatus }) {
  const statusIndicator = oracleStatus?.status === 'active' ? 'online' : 'offline';

  return (
    <div className="chain-status">
      <div className="status-header">
        <h3>System Status</h3>
        <div className={`status-indicator status-${statusIndicator}`}>
          <span className="status-dot"></span>
          {statusIndicator === 'online' ? 'Online' : 'Offline'}
        </div>
      </div>

      <div className="status-grid">
        <div className="status-item">
          <Activity size={20} className="status-icon" />
          <div className="status-content">
            <span className="status-label">Oracle Service</span>
            <span className="status-value">{oracleStatus?.status || 'Unknown'}</span>
          </div>
        </div>

        <div className="status-item">
          <Network size={20} className="status-icon" />
          <div className="status-content">
            <span className="status-label">Network</span>
            <span className="status-value">{oracleStatus?.network || 'testnet'}</span>
          </div>
        </div>

        <div className="status-item">
          <Cpu size={20} className="status-icon" />
          <div className="status-content">
            <span className="status-label">AI Model</span>
            <span className="status-value">
              {oracleStatus?.ai_model?.split('/').pop() || 'Qwen3'}
            </span>
          </div>
        </div>

        <div className="status-item">
          <Database size={20} className="status-icon" />
          <div className="status-content">
            <span className="status-label">Contract</span>
            <span className="status-value">
              {oracleStatus?.contract_package 
                ? `${oracleStatus.contract_package.substring(0, 8)}...`
                : 'Not configured'}
            </span>
          </div>
        </div>
      </div>

      {oracleStatus?.use_mock_ai && (
        <div className="status-warning">
          ⚠️ Using mock AI responses (API token not configured)
        </div>
      )}
    </div>
  );
}