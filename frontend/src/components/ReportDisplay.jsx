import { FileText, CheckCircle, AlertTriangle, Clock, Hash } from 'lucide-react';

export default function ReportDisplay({ result }) {
  if (!result) {
    return (
      <div className="report-placeholder">
        <FileText size={48} className="placeholder-icon" />
        <p>No report generated yet</p>
        <p className="placeholder-subtext">Submit an event above to generate an AI-powered logistics report</p>
      </div>
    );
  }

  const { success, shipment_id, event_description, ai_report, transaction, processing_time, timestamp } = result;

  if (!success) {
    return (
      <div className="card error-card">
        <h3 className="error-title">
          <AlertTriangle size={20} />
          Error Processing Event
        </h3>
        <p className="error-message">{result.error || 'Unknown error occurred'}</p>
      </div>
    );
  }

  const confidenceColor = 
    ai_report.confidence_score >= 80 ? 'high' :
    ai_report.confidence_score >= 60 ? 'medium' : 'low';

  return (
    <div className="report-container">
      <div className="card">
        <div className="report-header">
          <h2 className="card-title">
            <CheckCircle size={24} className="success-icon" />
            AI Analysis Complete
          </h2>
          <div className={`confidence-badge confidence-${confidenceColor}`}>
            {ai_report.confidence_score}% Confidence
          </div>
        </div>

        <div className="report-metadata">
          <div className="metadata-item">
            <Hash size={16} />
            <span className="metadata-label">Shipment ID:</span>
            <span className="metadata-value">{shipment_id}</span>
          </div>
          <div className="metadata-item">
            <Clock size={16} />
            <span className="metadata-label">Processing Time:</span>
            <span className="metadata-value">{processing_time}s</span>
          </div>
          <div className="metadata-item">
            <FileText size={16} />
            <span className="metadata-label">Timestamp:</span>
            <span className="metadata-value">{new Date(timestamp).toLocaleString()}</span>
          </div>
        </div>

        <div className="event-description">
          <h3>Event Description</h3>
          <p>{event_description}</p>
        </div>

        <div className="ai-summary">
          <h3>AI-Generated Report</h3>
          <pre className="report-text">{ai_report.summary}</pre>
        </div>

        {transaction && transaction.digest && (
          <div className="transaction-info">
            <h3>Blockchain Transaction</h3>
            <div className="tx-details">
              <div className="tx-item">
                <span className="tx-label">Status:</span>
                <span className="tx-value success">✓ Confirmed</span>
              </div>
              <div className="tx-item">
                <span className="tx-label">Transaction Hash:</span>
                <code className="tx-hash">{transaction.digest}</code>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}