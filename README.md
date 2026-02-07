# YuktaMedia Deal Document Extractor

AI-powered document extraction system for deal letters, release orders, and insertion orders.

## Quick Start (Development)

### 1. Backend Setup
```bash
cd backend
pip install fastapi uvicorn openai python-multipart pymupdf openpyxl python-dotenv
python run_server.py
```
Backend runs at: http://127.0.0.1:8000

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```
Frontend runs at: http://localhost:3000

## Deployment Options

### Option 1: Simple Local Demo (Recommended for POC)
1. Run backend: `python backend/run_server.py`
2. Build frontend: `cd frontend && npm run build`
3. Serve the `frontend/build` folder with any static server

### Option 2: Docker Deployment
```bash
docker-compose up --build
```

### Option 3: Cloud Deployment

**Backend (Railway/Render/Heroku):**
1. Push backend folder to GitHub
2. Connect to Railway/Render
3. Set environment variables from .env
4. Deploy

**Frontend (Vercel/Netlify):**
1. Push frontend folder to GitHub
2. Connect to Vercel/Netlify
3. Set `REACT_APP_API_URL` to your backend URL
4. Deploy

## Environment Variables

Create `.env` file in project root:
```
AZURE_OPENAI_ENDPOINT=your-endpoint
AZURE_OPENAI_API_KEY=your-key
AZURE_DEPLOYMENT_NAME=gpt-4o
AZURE_API_VERSION=2024-02-15-preview
```

## API Endpoints

- `POST /upload` - Upload PDF and get Excel output
- `GET /docs` - API documentation

## Tech Stack

- **Backend:** FastAPI, PyMuPDF, OpenAI, OpenPyXL
- **Frontend:** React
- **AI:** Azure OpenAI GPT-4o
