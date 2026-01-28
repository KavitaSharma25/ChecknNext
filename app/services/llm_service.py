"""
OpenAI LLM service for resume-JD matching analysis.
Implements prompt engineering and API communication with GPT models.
"""

import os
import json
import logging
from typing import Dict, List
from openai import OpenAI
from openai import RateLimitError, APIError

logger = logging.getLogger(__name__)

# Initialize OpenAI client - optional (will work without it for testing)
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None
    logger.warning("⚠️ OPENAI_API_KEY not set - API calls will fail, but server will run")


def create_analysis_prompt(resume_text: str, job_description_text: str) -> str:
    """
    Create a well-structured prompt for resume-JD matching analysis.
    Implements prompt engineering best practices for consistent, structured output.
    
    Args:
        resume_text: Full resume content
        job_description_text: Full job description content
        
    Returns:
        str: Formatted prompt for LLM
    """
    
    prompt = f"""Analyze the following resume against the job description. 
Provide a structured JSON response with the exact fields specified below.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description_text}

Analyze and respond in the following JSON format ONLY (no additional text):
{{
    "match_percentage": <integer 0-100>,
    "missing_skills": [<list of 3-5 important skills not mentioned in resume>],
    "improvement_suggestions": [<list of 3-5 specific, actionable suggestions to improve resume for this role>]
}}

Guidelines:
1. Match percentage should reflect how well the resume fits the job description (0-100 scale)
2. Missing skills should be explicitly mentioned in the JD but not in the resume
3. Improvement suggestions should be specific, actionable, and focused on recruiter expectations
4. Return ONLY valid JSON, no additional text or markdown formatting
5. All strings in arrays should be clear and concise (10-20 words max)

Focus on technical skills, experience level, and specific domain expertise mentioned in the JD."""
    
    return prompt


def parse_llm_response(response_text: str) -> Dict:
    """
    Parse and validate LLM response.
    Extracts JSON from response and validates structure.
    
    Args:
        response_text: Raw response from OpenAI API
        
    Returns:
        dict: Parsed and validated response
        
    Raises:
        ValueError: If response cannot be parsed or is invalid
    """
    
    try:
        # Try to extract JSON from response
        # Sometimes LLM might include extra text, so we search for JSON block
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1
        
        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON found in response")
        
        json_str = response_text[json_start:json_end]
        parsed = json.loads(json_str)
        
        # Validate required fields
        required_fields = ["match_percentage", "missing_skills", "improvement_suggestions"]
        for field in required_fields:
            if field not in parsed:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate match_percentage is integer between 0-100
        match_percentage = parsed["match_percentage"]
        if not isinstance(match_percentage, int) or match_percentage < 0 or match_percentage > 100:
            raise ValueError(f"Invalid match_percentage: {match_percentage}")
        
        # Validate missing_skills is a list
        if not isinstance(parsed["missing_skills"], list):
            raise ValueError("missing_skills must be a list")
        
        # Validate improvement_suggestions is a list
        if not isinstance(parsed["improvement_suggestions"], list):
            raise ValueError("improvement_suggestions must be a list")
        
        logger.debug(f"✓ Successfully parsed LLM response")
        return parsed
        
    except json.JSONDecodeError as e:
        logger.error(f"✗ JSON parsing error: {str(e)}")
        raise ValueError(f"Invalid JSON in LLM response: {str(e)}")
    except ValueError as e:
        logger.error(f"✗ Validation error: {str(e)}")
        raise


def analyze_resume_vs_jd(resume_text: str, job_description_text: str) -> Dict:
    """
    Main function to analyze resume against job description using OpenAI.
    Handles API communication and error management.
    
    Args:
        resume_text: Full resume content
        job_description_text: Full job description content
        
    Returns:
        dict: Analysis result with match_percentage, missing_skills, improvement_suggestions
        
    Raises:
        Exception: If API call fails or response is invalid
    """
    
    try:
        # Validate inputs
        if not resume_text or len(resume_text) < 50:
            raise ValueError("Resume text must be at least 50 characters")
        
        if not job_description_text or len(job_description_text) < 50:
            raise ValueError("Job description must be at least 50 characters")
        
        # Check if OpenAI is configured
        if not client:
            logger.warning("⚠️ OpenAI API key not configured - using demo response")
            return get_demo_response()
        
        logger.info("📤 Sending analysis request to OpenAI API...")
        
        # Create prompt with best practices
        prompt = create_analysis_prompt(resume_text, job_description_text)
        
        # Call OpenAI API with specified parameters
        # Using GPT-4 for better analysis quality, fallback to gpt-3.5-turbo if needed
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert recruiter and resume analyst. Analyze resumes against job descriptions and provide structured, JSON-formatted feedback."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for more consistent, structured output
            max_tokens=1000,
            top_p=0.9
        )
        
        # Extract response content
        response_text = response.choices[0].message.content
        logger.debug(f"📥 Received response from OpenAI")
        
        # Parse and validate response
        analysis_result = parse_llm_response(response_text)
        
        logger.info(f"✓ Analysis complete - Match: {analysis_result['match_percentage']}%")
        return analysis_result
        
    except RateLimitError as e:
        logger.error(f"✗ OpenAI API rate limit exceeded: {str(e)}")
        raise Exception("OpenAI API rate limit exceeded. Please try again later.")
    except APIError as e:
        logger.error(f"✗ OpenAI API error: {str(e)}")
        raise Exception(f"OpenAI API error: {str(e)}")
    except ValueError as e:
        logger.error(f"✗ Validation error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"✗ Unexpected error in analysis: {str(e)}")
        raise Exception(f"Failed to analyze resume: {str(e)}")


def get_demo_response() -> Dict:
    """
    Return a demo response when OpenAI API is not configured.
    Useful for testing the API without an API key.
    """
    return {
        "match_percentage": 75,
        "missing_skills": [
            "Docker containerization",
            "Kubernetes orchestration",
            "AWS cloud platform expertise"
        ],
        "improvement_suggestions": [
            "Add Docker containerization projects to demonstrate DevOps knowledge",
            "Include Kubernetes deployment case studies to show orchestration skills",
            "Highlight AWS certifications and cloud architecture experience",
            "Document infrastructure-as-code projects using Terraform",
            "Showcase CI/CD pipeline design and implementation examples"
        ]
    }
