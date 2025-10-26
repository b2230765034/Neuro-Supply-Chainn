import { useState, useEffect } from 'react';
import { Brain, Package, Lock } from 'lucide-react';
import EventInput from './components/EventInput';
import ReportDisplay from './components/ReportDisplay';
import ChainStatus from './components/ChainStatus';
import apiService from './services/api';
import WalletConnect from './components/WalletConnect';
import { useCurrentAccount } from '@mysten/dapp-kit';

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [oracleStatus, setOracleStatus] = useState(null);
  const [error, setError] = useState(null);
  const currentAccount = useCurrentAccount();

  // Fetch oracle status on mount
  useEffect(() => {
    fetchOracleStatus();
  }, []);

  const fetchOracleStatus = async () => {
    try {
      const status = await apiService.getOracleStatus();
      setOracleStatus(status);
    } catch (err) {
      console.error('Failed to fetch oracle status:', err);
    }
  };

  const handleSubmitEvent = async (eventDescription, shipmentId) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await apiService.submitEvent(eventDescription, shipmentId);
      setResult(response);

      // Scroll to results
      setTimeout(() => {
        document.querySelector('.report-container')?.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        });
      }, 100);
    } catch (err) {
      setError(err.message || 'Failed to process event');
      console.error('Error processing event:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="header-title">
            <div className="logo">
              <Brain size={32} />
              <Package size={32} className="logo-accent" />
            </div>
            <div>
              <h1>Neuro-Generative Supply Chain Optimizer</h1>
              <p className="header-subtitle">
                AI-Powered Logistics Intelligence on Blockchain
              </p>
            </div>
            {currentAccount && <WalletConnect />}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        <div className="container">
          {/* Status Panel */}
          <aside className="sidebar">
            <ChainStatus oracleStatus={oracleStatus} />
            
            <div className="info-panel">
              <h4>How It Works</h4>
              <ol className="info-steps">
                <li>Submit a logistics event description</li>
                <li>Qwen3 AI generates analysis report</li>
                <li>Oracle signs and verifies report</li>
                <li>Data recorded on Sui blockchain</li>
                <li>View results and transaction proof</li>
              </ol>
            </div>

            <div className="tech-stack">
              <h4>Tech Stack</h4>
              <div className="tech-badges">
                <span className="tech-badge">Qwen3 AI</span>
                <span className="tech-badge">Sui Blockchain</span>
                <span className="tech-badge">Move Lang</span>
                <span className="tech-badge">React</span>
                <span className="tech-badge">Python</span>
              </div>
            </div>
          </aside>

          {/* Main Content Area */}
          <div className="main-content">
            {currentAccount ? (
              <>
                <EventInput 
                  onSubmit={handleSubmitEvent} 
                  isLoading={isLoading}
                />

                {error && (
                  <div className="error-banner">
                    <span>⚠️ {error}</span>
                  </div>
                )}

                <ReportDisplay result={result} />
              </>
            ) : (
              <div className="card connect-wallet-prompt">
                <div className="connect-wallet-content">
                  <Lock size={48} className="lock-icon" />
                  <h2>Connect Your Wallet</h2>
                  <p>Please connect your wallet to access the AI report generation system.</p>
                  <WalletConnect />
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>
          Built for hackathon • Combining GenAI with Blockchain • 
          <a href="https://github.com" target="_blank" rel="noopener noreferrer"> View on GitHub</a>
        </p>
      </footer>
    </div>
  );
}

export default App;