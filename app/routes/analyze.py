"""
API routes for resume-JD matching analysis.
Defines all endpoints for the FastAPI application.
"""

from fastapi import APIRouter, HTTPException
from typing import List
import logging

from app.models.schemas import AnalyzeRequest, AnalyzeResponse, ErrorResponse
from app.services.llm_service import analyze_resume_vs_jd

logger = logging.getLogger(__name__)

# Create router for analysis endpoints
router = APIRouter(
    prefix="/api/v1",
    tags=["analysis"],
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analyze resume against job description",
    description="Compare a resume with a job description and get match analysis, missing skills, and improvement suggestions."
)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Main endpoint for resume-JD matching analysis.
    
    Accepts resume and job description text, sends to OpenAI for analysis,
    and stores results in MongoDB.
    
    Args:
        request: AnalyzeRequest containing resume_text and job_description_text
        
    Returns:
        AnalyzeResponse: Match percentage, missing skills, and suggestions
        
    Raises:
        HTTPException: If validation fails or API error occurs
    """
    
    try:
        logger.info("🔄 Processing analysis request...")
        
        # Input validation (additional to Pydantic validation)
        resume_text = request.resume_text.strip()
        jd_text = request.job_description_text.strip()
        
        if not resume_text or len(resume_text) < 50:
            logger.warning("❌ Invalid resume: too short")
            raise HTTPException(
                status_code=400,
                detail="Resume must be at least 50 characters long"
            )
        
        if not jd_text or len(jd_text) < 50:
            logger.warning("❌ Invalid job description: too short")
            raise HTTPException(
                status_code=400,
                detail="Job description must be at least 50 characters long"
            )
        
        # Call LLM service for analysis
        logger.debug("📊 Calling LLM service for analysis...")
        analysis_result = analyze_resume_vs_jd(resume_text, jd_text)
        
        logger.info(f"✅ Analysis complete")
        
        # Return structured response
        return AnalyzeResponse(
            match_percentage=analysis_result["match_percentage"],
            missing_skills=analysis_result["missing_skills"],
            improvement_suggestions=analysis_result["improvement_suggestions"]
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        logger.warning(f"❌ Validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"❌ Unexpected error in analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred during analysis. Please try again later."
        )
