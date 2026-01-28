#!/usr/bin/env python
"""
Quick start script demonstrating API usage.
Run with: python quickstart.py
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_URL = "http://localhost:8000/api/v1"

# Sample resume
SAMPLE_RESUME = """
Senior Software Engineer with 5+ years of professional experience building scalable backend systems.
Proficient in Python, FastAPI, Django, and microservices architecture.
Strong expertise in cloud platforms (AWS, GCP) and containerization (Docker).
Led development of 10+ projects from conception to production deployment.
Experience with PostgreSQL, MongoDB, and Redis.
Familiar with CI/CD pipelines and DevOps practices.
"""

# Sample job description
SAMPLE_JOB_DESC = """
We are seeking a Senior Python Backend Developer with 5+ years of experience.

Required Skills:
- 5+ years Python development
- FastAPI or Django experience
- AWS or GCP cloud platform experience
- Docker containerization knowledge
- SQL and NoSQL database experience

Nice to Have:
- Kubernetes orchestration
- Terraform infrastructure-as-code
- CI/CD pipeline implementation
- Microservices architecture experience
- API design and development

Responsibilities:
- Design and implement scalable backend systems
- Collaborate with product and frontend teams
- Mentor junior developers
- Participate in code reviews

Benefits:
- Competitive salary and equity
- Flexible work environment
- Professional development budget
"""


def print_separator(title=""):
    """Print a formatted separator."""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"{'='*60}\n")


def test_health():
    """Test API health check."""
    print_separator("Testing API Health Check")
    
    try:
        response = requests.get(f"{API_URL.replace('/api/v1', '')}/health")
        if response.status_code == 200:
            print("✅ API is healthy!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"❌ API health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {str(e)}")
        print(f"Make sure the API is running at {API_URL}")
        return False


def test_analyze():
    """Test resume analysis endpoint."""
    print_separator("Testing Resume Analysis")
    
    payload = {
        "resume_text": SAMPLE_RESUME,
        "job_description_text": SAMPLE_JOB_DESC
    }
    
    try:
        print("📤 Sending analysis request...")
        response = requests.post(
            f"{API_URL}/analyze",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis successful!")
            print(f"\n📊 Results:")
            print(f"  Match Percentage: {result['match_percentage']}%")
            print(f"\n🚫 Missing Skills ({len(result['missing_skills'])}):")
            for skill in result['missing_skills']:
                print(f"    - {skill}")
            print(f"\n💡 Improvement Suggestions ({len(result['improvement_suggestions'])}):")
            for i, suggestion in enumerate(result['improvement_suggestions'], 1):
                print(f"    {i}. {suggestion}")
            return True
        else:
            print(f"❌ Analysis failed with status {response.status_code}")
            print(f"Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        return False


def test_statistics():
    """Test statistics endpoint."""
    print_separator("Testing Statistics Endpoint")
    
    try:
        response = requests.get(f"{API_URL}/statistics")
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistics retrieved!")
            print(f"\n📈 Database Statistics:")
            print(f"  Total Analyses: {stats['total_analyses']}")
            print(f"  Average Match: {stats['average_match']}%")
            return True
        else:
            print(f"❌ Failed to retrieve statistics (status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error retrieving statistics: {str(e)}")
        return False


def test_recent_analyses():
    """Test retrieving recent analyses."""
    print_separator("Testing Recent Analyses")
    
    try:
        response = requests.get(f"{API_URL}/analyses?limit=5")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {data['count']} analyses!")
            if data['analyses']:
                print(f"\n📋 Recent Analyses:")
                for analysis in data['analyses'][:3]:
                    print(f"  - Match: {analysis['match_percentage']}% | Created: {analysis['created_at']}")
            return True
        else:
            print(f"❌ Failed to retrieve analyses (status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error retrieving analyses: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("  AI Resume-JD Matcher - API Quick Start")
    print("="*60)
    
    print(f"\nAPI URL: {API_URL}")
    print(f"Interactive Docs: {API_URL.replace('/api/v1', '')}/api/docs")
    
    # Run tests
    results = {
        "Health Check": test_health(),
        "Resume Analysis": test_analyze(),
        "Statistics": test_statistics(),
        "Recent Analyses": test_recent_analyses()
    }
    
    # Summary
    print_separator("Test Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! API is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
