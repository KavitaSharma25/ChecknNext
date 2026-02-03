"""
Pydantic models and schemas for request/response validation.
Ensures type safety and automatic API documentation with OpenAPI.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class AnalyzeRequest(BaseModel):
    """
    Request model for resume-JD analysis endpoint.
    Accepts resume text and job description text.
    """
    resume_text: str = Field(
        ..., 
        min_length=50, 
        description="The full text of the resume"
    )
    job_description_text: str = Field(
        ..., 
        min_length=50, 
        description="The full text of the job description"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "resume_text": "Senior Software Engineer with 5 years experience in Python...",
                "job_description_text": "We are looking for a Python developer with FastAPI experience..."
            }
        }


class AnalyzeResponse(BaseModel):
    """
    Response model containing analysis results from LLM.
    Includes match percentage, missing skills, and suggestions.
    """
    match_percentage: int = Field(
        ..., 
        ge=0, 
        le=100,
        description="Match percentage between resume and job description"
    )
    missing_skills: List[str] = Field(
        default_factory=list,
        description="List of important skills missing from the resume"
    )
    improvement_suggestions: List[str] = Field(
        default_factory=list,
        description="Actionable suggestions to improve resume fit"
    )
    analysis_id: Optional[str] = Field(
        None,
        description="MongoDB document ID for this analysis result"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "match_percentage": 75,
                "missing_skills": ["Docker", "Kubernetes"],
                "improvement_suggestions": [
                    "Add Docker containerization experience",
                    "Highlight cloud deployment projects"
                ]
            }
        }


class AnalysisResult(BaseModel):
    """
    Database model for storing analysis results with metadata.
    """
    analysis_id: Optional[str] = None  # MongoDB ObjectId as string
    match_percentage: int
    missing_skills: List[str]
    improvement_suggestions: List[str]
    resume_length: int  # Character count of resume
    jd_length: int  # Character count of job description
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "match_percentage": 75,
                "missing_skills": ["Docker", "Kubernetes"],
                "improvement_suggestions": [
                    "Add Docker containerization experience"
                ],
                "resume_length": 2500,
                "jd_length": 1800,
                "created_at": "2026-01-28T10:30:00",
                "updated_at": "2026-01-28T10:30:00"
            }
        }


class ErrorResponse(BaseModel):
    """
    Standard error response model for API errors.
    """
    error: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    detail: Optional[str] = Field(None, description="Additional error details")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid input",
                "status_code": 400,
                "detail": "Resume text must be at least 50 characters"
            }
        }
