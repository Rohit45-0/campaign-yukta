import fitz  # PyMuPDF

def extract_text(pdf_path: str) -> str:
    """Extract text from PDF using PyMuPDF"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num, page in enumerate(doc):
            page_text = page.get_text()
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page_text
        
        doc.close()
        return text.strip()
        
    except Exception as e:
        print(f"Error extracting text: {e}")
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

