import React, { useState, useCallback } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import ProcessingStatus from './components/ProcessingStatus';
import Header from './components/Header';

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('idle');
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);

  const handleFileSelect = useCallback((selectedFile) => {
    setFile(selectedFile);
    setStatus('idle');
    setError(null);
  }, []);

  const handleUpload = useCallback(async () => {
    if (!file) return;

    setStatus('uploading');
    setProgress(10);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      setProgress(30);
      setStatus('processing');

      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      setProgress(70);

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || 'Upload failed');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = 'deal_export.xlsx';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      setProgress(100);
      setStatus('success');
    } catch (err) {
      setStatus('error');
      setError(err.message || 'An error occurred');
    }
  }, [file]);

  const handleReset = useCallback(() => {
    setFile(null);
    setStatus('idle');
    setProgress(0);
    setError(null);
  }, []);

  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <div className="container">
          <div className="card">
            <div className="card-header">
              <h2>Upload Deal Document</h2>
              <p>Extract deal & placement data from PDF documents automatically</p>
            </div>
            
            <div className="card-body">
              <FileUpload 
                file={file}
                onFileSelect={handleFileSelect}
                disabled={status === 'uploading' || status === 'processing'}
              />

              {file && status === 'idle' && (
                <button className="btn btn-primary" onClick={handleUpload}>
                  Extract Data
                </button>
              )}

              {(status !== 'idle') && (
                <ProcessingStatus 
                  status={status}
                  progress={progress}
                  error={error}
                  onReset={handleReset}
                />
              )}
            </div>
          </div>

          <div className="info-section">
            <h3>How it works</h3>
            <div className="steps">
              <div className="step">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h4>Upload PDF</h4>
                  <p>Deal letters, release orders, insertion orders</p>
                </div>
              </div>
              <div className="step">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h4>AI Extraction</h4>
                  <p>Automatic deal & placement data extraction</p>
                </div>
              </div>
              <div className="step">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h4>Download Excel</h4>
                  <p>Ready for YuktaOne import</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
