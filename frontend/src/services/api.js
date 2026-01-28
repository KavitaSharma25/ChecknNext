import axios from 'axios'

// API base URL
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Analyze resume against job description
 */
export const analyzeResume = async (resumeText, jobDescriptionText) => {
  try {
    const response = await apiClient.post('/analyze', {
      resume_text: resumeText,
      job_description_text: jobDescriptionText,
    })
    return response.data
  } catch (error) {
    // Improved error handling
    let errorMessage = 'Failed to analyze resume'
    
    if (error.response) {
      // API returned error response
      errorMessage = error.response?.data?.detail || 
                    error.response?.data?.error || 
                    error.response?.data?.message ||
                    `Server error: ${error.response.status}`
    } else if (error.request) {
      // Request made but no response received
      errorMessage = 'Network error: Could not connect to server. Make sure the backend is running on http://localhost:8000'
    } else if (error.message) {
      // Error in request setup
      errorMessage = `Error: ${error.message}`
    }
    
    throw new Error(errorMessage)
  }
}

/**
 * Get specific analysis by ID
 */
export const getAnalysis = async (analysisId) => {
  try {
    const response = await apiClient.get(`/analyses/${analysisId}`)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch analysis')
  }
}

/**
 * Get recent analyses
 */
export const getRecentAnalyses = async (limit = 10) => {
  try {
    const response = await apiClient.get('/analyses', {
      params: { limit },
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch analyses')
  }
}

/**
 * Get database statistics
 */
export const getStatistics = async () => {
  try {
    const response = await apiClient.get('/statistics')
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch statistics')
  }
}

/**
 * Delete an analysis
 */
export const deleteAnalysis = async (analysisId) => {
  try {
    const response = await apiClient.delete(`/analyses/${analysisId}`)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to delete analysis')
  }
}

export default apiClient
