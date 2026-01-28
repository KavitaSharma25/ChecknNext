import React, { useState } from 'react'

function AnalysisForm({ onSubmit, loading }) {
  const [resumeText, setResumeText] = useState('')
  const [jobDescriptionText, setJobDescriptionText] = useState('')
  const [errors, setErrors] = useState({})

  const validateForm = () => {
    const newErrors = {}
    if (resumeText.trim().length < 500) {
      newErrors.resume = 'Resume must be at least 500 characters'
    }
    if (jobDescriptionText.trim().length < 500) {
      newErrors.jd = 'Job description must be at least 500 characters'
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (validateForm()) {
      onSubmit(resumeText, jobDescriptionText)
    }
  }

  const sampleResume = `SENIOR FULL-STACK ENGINEER | Python | FastAPI | AWS | Docker

PROFESSIONAL SUMMARY
Accomplished Senior Software Engineer with 8+ years of progressive experience designing, developing, and deploying enterprise-scale applications. Proven expertise in backend systems, cloud architecture, and DevOps practices. Strong track record of leading cross-functional teams, mentoring junior engineers, and delivering high-impact projects. Passionate about clean code, system design, and continuous improvement.

CORE COMPETENCIES
Backend Development: Python, FastAPI, Django, REST APIs, GraphQL, microservices architecture
Cloud & Infrastructure: AWS (EC2, S3, Lambda, RDS), GCP (Compute Engine, Cloud SQL), Azure basics
Containerization & Orchestration: Docker, Docker Compose, Kubernetes (EKS, GKE), Helm charts
Databases: PostgreSQL, MongoDB, Redis, Elasticsearch, DynamoDB, database optimization
DevOps & CI/CD: Jenkins, GitHub Actions, GitLab CI/CD, Terraform, CloudFormation, infrastructure-as-code
Tools & Frameworks: Git, Agile/Scrum, JIRA, Linux/Ubuntu, testing frameworks (pytest, unittest)

PROFESSIONAL EXPERIENCE

Senior Backend Engineer - Tech Innovations Corp (2021 - Present)
- Led architecture and implementation of microservices platform serving 2M+ daily users
- Designed and built high-performance REST APIs handling 100K+ requests/minute with <100ms latency
- Implemented automated testing pipeline increasing code coverage from 45% to 92%
- Mentored team of 4 junior engineers, conducting code reviews and technical training
- Reduced infrastructure costs by 35% through AWS optimization and resource consolidation

Backend Developer - CloudScale Solutions (2018 - 2021)
- Developed scalable Flask and FastAPI applications for SaaS platform
- Implemented Docker containerization reducing deployment time by 60%
- Built CI/CD pipelines using GitHub Actions processing 50+ deployments daily
- Optimized database queries reducing API response time by 40%
- Collaborated with DevOps team to migrate legacy systems to Kubernetes

TECHNICAL PROJECTS
Resume-JD Matcher AI System - Open Source Contribution
- Built FastAPI backend for intelligent resume and job description matching
- Integrated OpenAI API for NLP-based skill extraction and analysis
- Developed MongoDB data persistence layer with aggregation pipelines
- Achieved 85%+ matching accuracy through prompt engineering optimization

E-commerce Platform Redesign
- Architected new microservices replacing monolithic application
- Implemented event-driven architecture using RabbitMQ and Kafka
- Reduced API response time from 500ms to 120ms through caching and optimization
- Managed successful migration of 50M+ customer records with zero downtime

EDUCATION
Bachelor of Science in Computer Science
State University (2015)

CERTIFICATIONS
- AWS Certified Solutions Architect (2022)
- Docker Certified Associate (2021)

ADDITIONAL SKILLS
- Strong problem-solving and analytical abilities
- Excellent communication and team collaboration
- Fluent in English, conversational Spanish
- Open source contributor with 500+ GitHub stars`

  const sampleJD = `SENIOR BACKEND ENGINEER - PYTHON

COMPANY OVERVIEW
Join a fast-growing fintech startup revolutionizing how businesses manage their operations. We serve 10,000+ companies and process billions in transactions annually. Our engineering team is dedicated to building reliable, scalable systems that millions depend on.

POSITION OVERVIEW
We are seeking an experienced Senior Backend Engineer to lead the development of our core payment processing platform. You will architect scalable microservices, optimize database performance, and mentor junior engineers while working with cutting-edge technologies.

REQUIRED QUALIFICATIONS
- 7+ years of professional software development experience
- 5+ years working with Python in production environments
- Proven expertise with FastAPI or Django frameworks
- Strong understanding of microservices architecture and design patterns
- Production experience with AWS (EC2, S3, RDS, Lambda, SQS) or GCP
- Proficiency in containerization using Docker and Kubernetes
- Solid knowledge of SQL databases (PostgreSQL, MySQL) and NoSQL (MongoDB, Redis)
- Experience with CI/CD pipelines and DevOps practices (Git, Jenkins, GitHub Actions)
- Excellent problem-solving skills and attention to detail
- Strong communication and team collaboration abilities

PREFERRED QUALIFICATIONS
- Experience with message queues (RabbitMQ, Kafka, SQS)
- Knowledge of system design and scalability
- Familiarity with infrastructure-as-code (Terraform, CloudFormation)
- Experience with monitoring and observability tools (DataDog, New Relic, Prometheus)
- Contributions to open-source projects
- AWS or GCP certifications

RESPONSIBILITIES
- Design and build scalable backend services and APIs handling millions of transactions
- Lead technical initiatives and architectural decisions for platform improvements
- Mentor and code review junior engineers, fostering technical growth
- Collaborate with product managers, DevOps, and frontend teams
- Implement robust testing strategies and improve code quality
- Optimize database queries and API performance
- Troubleshoot production issues and implement solutions
- Stay current with emerging technologies and best practices

NICE TO HAVE
- Experience with GraphQL
- Knowledge of machine learning/AI integration
- Experience with blockchain or cryptocurrency
- Healthcare or fintech industry experience

COMPENSATION & BENEFITS
- Competitive salary: $150K - $190K based on experience
- Stock options
- Comprehensive health insurance
- 401(k) matching
- Unlimited PTO
- Remote work flexibility
- Professional development budget`

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Resume Input */}
      <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-deep-sea-500">
        <label className="block text-lg font-semibold text-deep-sea-900 mb-3">
          📄 Your Resume
        </label>
        <textarea
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
          placeholder="Paste your resume here..."
          className={`w-full h-48 p-4 border-2 rounded-lg font-mono text-sm resize-none focus:outline-none transition-colors ${
            errors.resume ? 'border-red-500' : 'border-deep-sea-300 focus:border-deep-sea-600'
          }`}
        />
        {errors.resume && <p className="text-red-600 text-sm mt-2">⚠️ {errors.resume}</p>}
        <p className="text-deep-sea-500 text-xs mt-2">{resumeText.length} / 500 characters minimum</p>
      </div>

      {/* Job Description Input */}
      <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-deep-sea-600">
        <label className="block text-lg font-semibold text-deep-sea-900 mb-3">
          💼 Job Description
        </label>
        <textarea
          value={jobDescriptionText}
          onChange={(e) => setJobDescriptionText(e.target.value)}
          placeholder="Paste the job description here..."
          className={`w-full h-48 p-4 border-2 rounded-lg font-mono text-sm resize-none focus:outline-none transition-colors ${
            errors.jd ? 'border-red-500' : 'border-deep-sea-300 focus:border-deep-sea-600'
          }`}
        />
        {errors.jd && <p className="text-red-600 text-sm mt-2">⚠️ {errors.jd}</p>}
        <p className="text-deep-sea-500 text-xs mt-2">{jobDescriptionText.length} / 500 characters minimum</p>
      </div>

      {/* Quick Fill Button */}
      <button
        type="button"
        onClick={() => {
          setResumeText(sampleResume)
          setJobDescriptionText(sampleJD)
        }}
        className="w-full bg-gradient-to-r from-deep-sea-200 to-deep-sea-300 hover:from-deep-sea-300 hover:to-deep-sea-400 text-deep-sea-900 font-semibold py-3 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 shadow-md"
      >
        🎯 Load Sample Data
      </button>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading}
        className={`w-full py-4 px-6 rounded-lg font-bold text-white text-lg transition-all duration-300 transform ${
          loading
            ? 'bg-gray-400 cursor-not-allowed opacity-75'
            : 'bg-gradient-to-r from-deep-sea-900 to-deep-sea-600 hover:from-deep-sea-800 hover:to-deep-sea-500 shadow-lg hover:shadow-xl hover:scale-105'
        }`}
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <span className="animate-spin">⏳</span> Analyzing...
          </span>
        ) : (
          '🚀 Analyze Resume'
        )}
      </button>

      {/* Info Box */}
      <div className="bg-gradient-to-r from-deep-sea-100 to-deep-sea-200 border border-deep-sea-400 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow duration-300">
        <p className="text-sm text-deep-sea-800">
          <span className="font-semibold">ℹ️ How it works:</span> Our AI analyzes your resume against the job description to find matches, missing skills, and improvement suggestions.
        </p>
      </div>
    </form>
  )
}

export default AnalysisForm
