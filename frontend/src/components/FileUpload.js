import React, { useCallback, useState } from 'react';
import './FileUpload.css';

function FileUpload({ file, onFileSelect, disabled }) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    if (!disabled) setIsDragging(true);
  }, [disabled]);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    if (disabled) return;

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === 'application/pdf') {
      onFileSelect(droppedFile);
    }
  }, [disabled, onFileSelect]);

  const handleFileInput = useCallback((e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      onFileSelect(selectedFile);
    }
  }, [onFileSelect]);

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="file-upload">
      <div 
        className={`dropzone ${isDragging ? 'dragging' : ''} ${file ? 'has-file' : ''} ${disabled ? 'disabled' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !disabled && document.getElementById('file-input').click()}
      >
        {!file ? (
          <>
            <div className="dropzone-icon">📁</div>
            <p className="dropzone-text">
              Drag & drop your PDF here
            </p>
            <p className="dropzone-subtext">or click to browse</p>
            <span className="dropzone-hint">Supports: PDF files only</span>
          </>
        ) : (
          <div className="file-preview">
            <div className="file-icon">📄</div>
            <div className="file-info">
              <p className="file-name">{file.name}</p>
              <p className="file-size">{formatFileSize(file.size)}</p>
            </div>
            {!disabled && (
              <button 
                className="file-remove" 
                onClick={(e) => {
                  e.stopPropagation();
                  onFileSelect(null);
                }}
              >
                ✕
              </button>
            )}
          </div>
        )}
      </div>
      <input
        id="file-input"
        type="file"
        accept=".pdf"
        onChange={handleFileInput}
        disabled={disabled}
        hidden
      />
    </div>
  );
}

export default FileUpload;
