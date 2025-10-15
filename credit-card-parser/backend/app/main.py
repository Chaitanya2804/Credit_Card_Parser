"""
FastAPI Backend for Credit Card Statement Parser
Provides REST API for PDF upload, parsing, and result retrieval
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from pathlib import Path
import uuid
from datetime import datetime

from app.database import engine, SessionLocal, Base
from app.models import ParsedStatement, ParseResponse
from app.parser.pdf_reader import extract_text_from_pdf
from app.parser.ocr_handler import extract_text_with_ocr
from app.parser.issuer_detector import detect_issuer
from app.parser.extractors import extract_fields
from app.utils.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Credit Card Statement Parser API",
    description="Extract key details from credit card statements",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary storage for uploaded files
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Credit Card Statement Parser",
        "version": "1.0.0"
    }


@app.post("/upload", response_model=ParseResponse)
async def upload_statement(file: UploadFile = File(...)):
    """
    Upload and parse credit card statement PDF
    
    Returns:
        ParseResponse with extracted fields and confidence scores
    """
    logger.info(f"Received file: {file.filename}")
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Generate unique ID for this parsing session
        session_id = str(uuid.uuid4())
        
        # Save uploaded file temporarily
        file_path = UPLOAD_DIR / f"{session_id}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"File saved: {file_path}")
        
        # Step 1: Extract text (with OCR fallback)
        text = extract_text_from_pdf(str(file_path))
        
        if not text or len(text.strip()) < 50:
            logger.warning("Text extraction failed, trying OCR...")
            text = extract_text_with_ocr(str(file_path))
        
        if not text:
            raise HTTPException(
                status_code=422, 
                detail="Could not extract text from PDF. File may be corrupted."
            )
        
        logger.info(f"Extracted {len(text)} characters")
        
        # Step 2: Detect issuer
        issuer = detect_issuer(text)
        logger.info(f"Detected issuer: {issuer}")
        
        # Step 3: Extract fields
        extracted_data = extract_fields(text, issuer)
        logger.info(f"Extracted fields: {extracted_data}")
        
        # Step 4: Calculate overall confidence
        confidence_scores = [v.get('confidence', 0) for v in extracted_data.values()]
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        # Step 5: Save to database
        db = SessionLocal()
        try:
            db_statement = ParsedStatement(
                id=session_id,
                filename=file.filename,
                issuer=issuer,
                card_last_four=extracted_data.get('card_last_four', {}).get('value'),
                billing_cycle=extracted_data.get('billing_cycle', {}).get('value'),
                due_date=extracted_data.get('due_date', {}).get('value'),
                total_amount_due=extracted_data.get('total_amount_due', {}).get('value'),
                confidence_score=overall_confidence,
                raw_text=text[:1000],  # Store first 1000 chars
                created_at=datetime.utcnow()
            )
            db.add(db_statement)
            db.commit()
            db.refresh(db_statement)
            logger.info(f"Saved to database with ID: {session_id}")
        finally:
            db.close()
        
        # Clean up uploaded file
        file_path.unlink(missing_ok=True)
        
        return ParseResponse(
            id=session_id,
            filename=file.filename,
            issuer=issuer,
            extracted_fields=extracted_data,
            confidence_score=overall_confidence,
            status="success"
        )
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.get("/results/{session_id}")
async def get_results(session_id: str):
    """Retrieve parsed results by session ID"""
    db = SessionLocal()
    try:
        result = db.query(ParsedStatement).filter(ParsedStatement.id == session_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")
        
        return {
            "id": result.id,
            "filename": result.filename,
            "issuer": result.issuer,
            "card_last_four": result.card_last_four,
            "billing_cycle": result.billing_cycle,
            "due_date": result.due_date,
            "total_amount_due": result.total_amount_due,
            "confidence_score": result.confidence_score,
            "created_at": result.created_at.isoformat()
        }
    finally:
        db.close()


@app.get("/history")
async def get_history():
    """Get all parsed statements history"""
    db = SessionLocal()
    try:
        statements = db.query(ParsedStatement).order_by(
            ParsedStatement.created_at.desc()
        ).limit(50).all()
        
        return [
            {
                "id": s.id,
                "filename": s.filename,
                "issuer": s.issuer,
                "confidence_score": s.confidence_score,
                "created_at": s.created_at.isoformat()
            }
            for s in statements
        ]
    finally:
        db.close()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)