"""
SQLAlchemy ORM models and Pydantic schemas
"""
from sqlalchemy import Column, String, Float, Text, DateTime
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

from app.database import Base


# SQLAlchemy ORM Model
class ParsedStatement(Base):
    __tablename__ = "parsed_statements"
    
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    issuer = Column(String, nullable=False)
    card_last_four = Column(String, nullable=True)
    billing_cycle = Column(String, nullable=True)
    due_date = Column(String, nullable=True)
    total_amount_due = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=False)
    raw_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Pydantic Response Models
class ExtractedField(BaseModel):
    value: Optional[str]
    confidence: float
    method: str  # "regex", "ocr", "keyword"


class ParseResponse(BaseModel):
    id: str
    filename: str
    issuer: str
    extracted_fields: Dict[str, Dict[str, Any]]
    confidence_score: float
    status: str
    
    class Config:
        from_attributes = True


class HistoryItem(BaseModel):
    id: str
    filename: str
    issuer: str
    confidence_score: float
    created_at: str