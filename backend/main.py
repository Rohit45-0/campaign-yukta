from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import uuid
import os
import traceback

from extractor import extract_text
from llm_parser import parse_document
from excel_mapper import create_excel

app = FastAPI(title="Campaign AI - Document Extractor")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Campaign AI API is running", "docs": "/docs"}

@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    pdf_path = f"temp_{file_id}.pdf"
    
    try:
        # Save uploaded file
        print(f"[1/4] Saving uploaded file: {file.filename}")
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text from PDF
        print(f"[2/4] Extracting text from PDF...")
        text = extract_text(pdf_path)
        print(f"      Extracted {len(text)} characters")
        
        if not text or len(text.strip()) < 50:
            raise HTTPException(status_code=400, detail="Could not extract enough text from PDF")
        
        # Parse with LLM
        print(f"[3/4] Parsing document with LLM...")
        data = parse_document(text)
        print(f"      Campaign: {data.get('campaign', {}).get('campaign_name', 'N/A')}")
        print(f"      Line items: {len(data.get('line_items', []))}")
        
        # Generate Excel
        print(f"[4/4] Generating Excel file...")
        excel_path = create_excel(data, file_id)
        print(f"      Output: {excel_path}")
        
        # Cleanup temp PDF
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        
        return FileResponse(
            excel_path, 
            filename="campaign_output.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: {str(e)}")
        traceback.print_exc()
        # Cleanup on error
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        raise HTTPException(status_code=500, detail=str(e))

