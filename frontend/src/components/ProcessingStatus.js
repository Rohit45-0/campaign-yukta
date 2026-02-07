import React from 'react';
import './ProcessingStatus.css';

function ProcessingStatus({ status, progress, error, onReset }) {
  return (
    <div className="processing-status">
      {(status === 'uploading' || status === 'processing') && (
        <div className="status-processing">
          <div className="spinner"></div>
          <div className="status-text">
            <h4>{status === 'uploading' ? 'Uploading document...' : 'Extracting campaign data...'}</h4>
            <p>This may take a moment</p>
          </div>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }}></div>
          </div>
        </div>
      )}

      {status === 'success' && (
        <div className="status-success">
          <div className="status-icon">✅</div>
          <div className="status-text">
            <h4>Extraction Complete!</h4>
            <p>Your Excel file has been downloaded</p>
          </div>
          <button className="btn btn-secondary" onClick={onReset}>
            Upload Another Document
          </button>
        </div>
      )}

      {status === 'error' && (
        <div className="status-error">
          <div className="status-icon">❌</div>
          <div className="status-text">
            <h4>Extraction Failed</h4>
            <p className="error-message">{error}</p>
          </div>
          <button className="btn btn-secondary" onClick={onReset}>
            Try Again
          </button>
        </div>
      )}
    </div>
  );
}

export default ProcessingStatus;
