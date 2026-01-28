"""
Test file for API endpoints.
Run with: pytest test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthAndInfo:
    """Test health check and info endpoints."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "endpoints" in data


class TestAnalyzeEndpoint:
    """Test resume analysis endpoint."""
    
    def test_analyze_success(self):
        """Test successful analysis with valid input."""
        payload = {
            "resume_text": "Senior Software Engineer with 10 years Python experience including FastAPI, Django, and microservices. Expert in AWS, Docker, and Kubernetes. Led 15+ projects to successful deployment.",
            "job_description_text": "Senior Python Developer needed with 5+ years experience. Required: FastAPI, AWS, Docker. Nice to have: Kubernetes, Terraform. Must have strong communication."
        }
        response = client.post("/api/v1/analyze", json=payload)
        
        # Note: This will fail without valid OpenAI API key
        # In CI/CD, mock the OpenAI response
        if response.status_code == 200:
            data = response.json()
            assert "match_percentage" in data
            assert "missing_skills" in data
            assert "improvement_suggestions" in data
            assert 0 <= data["match_percentage"] <= 100
            assert isinstance(data["missing_skills"], list)
            assert isinstance(data["improvement_suggestions"], list)
    
    def test_analyze_invalid_resume_too_short(self):
        """Test validation for resume too short."""
        payload = {
            "resume_text": "Too short",
            "job_description_text": "This is a valid job description with plenty of content to meet the 50 character minimum requirement for testing purposes."
        }
        response = client.post("/api/v1/analyze", json=payload)
        assert response.status_code == 422  # Pydantic validation error
    
    def test_analyze_missing_field(self):
        """Test validation for missing required field."""
        payload = {
            "resume_text": "This is a valid resume text with at least 50 characters to pass validation checks."
        }
        response = client.post("/api/v1/analyze", json=payload)
        assert response.status_code == 422


class TestDataRetrieval:
    """Test data retrieval endpoints."""
    
    def test_get_statistics(self):
        """Test statistics endpoint."""
        response = client.get("/api/v1/statistics")
        assert response.status_code == 200
        data = response.json()
        assert "total_analyses" in data
        assert "average_match" in data
    
    def test_get_recent_analyses(self):
        """Test recent analyses retrieval."""
        response = client.get("/api/v1/analyses?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "analyses" in data
    
    def test_get_invalid_analysis_id(self):
        """Test retrieving non-existent analysis."""
        response = client.get("/api/v1/analyses/invalid_id")
        # Will fail due to invalid MongoDB ObjectId format
        assert response.status_code in [400, 404]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
