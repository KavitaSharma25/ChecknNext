"""
API routes for resume-JD matching analysis.
Defines all endpoints for the FastAPI application.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
import logging

from app.models.schemas import AnalyzeRequest, AnalyzeResponse, ErrorResponse, AnalysisResult
from app.services.llm_service import analyze_resume_vs_jd
from app.services.database import (
    save_analysis_result,
    get_analysis_by_id,
    get_all_analyses,
    delete_analysis,
    get_statistics
)

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
        
        # Save result to MongoDB
        logger.debug("💾 Saving analysis result to MongoDB...")
        analysis_id = await save_analysis_result(
            match_percentage=analysis_result["match_percentage"],
            missing_skills=analysis_result["missing_skills"],
            improvement_suggestions=analysis_result["improvement_suggestions"],
            resume_length=len(resume_text),
            jd_length=len(jd_text)
        )
        
        logger.info(f"✅ Analysis complete and saved with ID: {analysis_id}")
        
        # Return structured response with ID
        response = AnalyzeResponse(
            match_percentage=analysis_result["match_percentage"],
            missing_skills=analysis_result["missing_skills"],
            improvement_suggestions=analysis_result["improvement_suggestions"]
        )
        # Add analysis_id to response
        response.analysis_id = analysis_id
        return response
        
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

@router.get(
    "/analyses",
    response_model=List[AnalysisResult],
    summary="Get analysis history",
    description="Retrieve all stored analysis results with pagination support."
)
async def get_analyses_history(
    limit: int = Query(50, ge=1, le=100, description="Maximum results to return"),
    skip: int = Query(0, ge=0, description="Number of results to skip")
) -> List[AnalysisResult]:
    """
    Get analysis history from MongoDB.
    
    Args:
        limit: Maximum number of results (default 50)
        skip: Number of results to skip for pagination (default 0)
        
    Returns:
        List[AnalysisResult]: List of analysis results
    """
    try:
        logger.info(f"📚 Fetching analyses history (limit={limit}, skip={skip})...")
        results = await get_all_analyses(limit=limit, skip=skip)
        logger.info(f"✅ Retrieved {len(results)} analyses")
        return results
        
    except Exception as e:
        logger.error(f"❌ Error fetching analyses: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve analysis history"
        )


@router.get(
    "/analyses/{analysis_id}",
    response_model=AnalysisResult,
    summary="Get specific analysis result",
    description="Retrieve a specific analysis result by ID."
)
async def get_analysis(analysis_id: str) -> AnalysisResult:
    """
    Get a specific analysis result by ID.
    
    Args:
        analysis_id: MongoDB document ID
        
    Returns:
        AnalysisResult: The analysis result
        
    Raises:
        HTTPException: If analysis not found
    """
    try:
        logger.info(f"🔍 Fetching analysis: {analysis_id}")
        result = await get_analysis_by_id(analysis_id)
        
        if not result:
            logger.warning(f"⚠️ Analysis not found: {analysis_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Analysis with ID {analysis_id} not found"
            )
        
        logger.info(f"✅ Retrieved analysis: {analysis_id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve analysis"
        )


@router.delete(
    "/analyses/{analysis_id}",
    summary="Delete analysis result",
    description="Delete a specific analysis result by ID."
)
async def delete_analysis_result(analysis_id: str) -> Dict:
    """
    Delete an analysis result.
    
    Args:
        analysis_id: MongoDB document ID
        
    Returns:
        Dict: Success or error message
        
    Raises:
        HTTPException: If analysis not found
    """
    try:
        logger.info(f"🗑️ Deleting analysis: {analysis_id}")
        deleted = await delete_analysis(analysis_id)
        
        if not deleted:
            logger.warning(f"⚠️ Analysis not found: {analysis_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Analysis with ID {analysis_id} not found"
            )
        
        logger.info(f"✅ Deleted analysis: {analysis_id}")
        return {
            "message": "Analysis deleted successfully",
            "analysis_id": analysis_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete analysis"
        )


@router.get(
    "/statistics",
    summary="Get analysis statistics",
    description="Get overall statistics about all analyses."
)
async def get_analysis_statistics() -> Dict:
    """
    Get database statistics.
    
    Returns:
        Dict: Statistics including total analyses, average match percentage, etc.
    """
    try:
        logger.info("📊 Fetching statistics...")
        stats = await get_statistics()
        logger.info(f"✅ Retrieved statistics: {stats['total_analyses']} total analyses")
        return stats
        
    except Exception as e:
        logger.error(f"❌ Error fetching statistics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve statistics"
        )