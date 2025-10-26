import { useState } from 'react';
import { Send, AlertCircle } from 'lucide-react';

export default function EventInput({ onSubmit, isLoading }) {
  const [eventText, setEventText] = useState('');
  const [shipmentId, setShipmentId] = useState('');
  
  const exampleEvents = [
    "Truck carrying electronics delayed by 3 hours due to highway accident on I-95",
    "Shipment of medical supplies stuck at customs inspection for 24 hours",
    "Severe snowstorm causing delivery delays across midwest region",
    "Container ship waiting 48 hours at Los Angeles port due to congestion",
    "Refrigerated truck breakdown - perishable goods at risk"
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (eventText.trim()) {
      onSubmit(eventText, shipmentId || null);
    }
  };

  const handleExampleClick = (example) => {
    setEventText(example);
  };

  return (
    <div className="event-input-container">
      <div className="card">
        <h2 className="card-title">
          <AlertCircle size={24} />
          Submit Logistics Event
        </h2>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="shipment-id">Shipment ID (Optional)</label>
            <input
              id="shipment-id"
              type="text"
              value={shipmentId}
              onChange={(e) => setShipmentId(e.target.value)}
              placeholder="SHIP-2025-001 (leave blank to auto-generate)"
              disabled={isLoading}
              className="input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="event-description">Event Description *</label>
            <textarea
              id="event-description"
              value={eventText}
              onChange={(e) => setEventText(e.target.value)}
              placeholder="Describe the logistics event (delay, accident, weather, etc.)"
              rows={4}
              disabled={isLoading}
              required
              className="textarea"
            />
          </div>

          <button 
            type="submit" 
            disabled={isLoading || !eventText.trim()}
            className="button button-primary"
          >
            {isLoading ? (
              <>
                <div className="spinner" />
                Processing...
              </>
            ) : (
              <>
                <Send size={18} />
                Generate AI Report
              </>
            )}
          </button>
        </form>

        <div className="examples-section">
          <p className="examples-title">Example Events:</p>
          <div className="examples-grid">
            {exampleEvents.map((example, idx) => (
              <button
                key={idx}
                onClick={() => handleExampleClick(example)}
                disabled={isLoading}
                className="example-button"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}