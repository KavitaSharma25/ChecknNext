import React, { useState } from 'react'
import Header from './components/Header'
import AnalysisForm from './components/AnalysisForm'
import ResultsDisplay from './components/ResultsDisplay'
import History from './components/History'
import { analyzeResume } from './services/api'

function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])
  const [activeTab, setActiveTab] = useState('analyze')

  const handleAnalyze = async (resumeText, jobDescriptionText) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await analyzeResume(resumeText, jobDescriptionText)
      setResults({
        ...response,
        resumeText: resumeText,
        jobDescriptionText: jobDescriptionText,
        timestamp: new Date().toLocaleString()
      })
      
      // Add to history
      setHistory(prev => [{
        ...response,
        id: Date.now(),
        timestamp: new Date().toLocaleString()
      }, ...prev].slice(0, 10)) // Keep last 10
      
      setActiveTab('results')
    } catch (err) {
      setError(err.message || 'An error occurred. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-deep-sea-100 via-deep-sea-200 to-deep-sea-300">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 animate-fade-in-up">
        {/* Tab Navigation */}
        <div className="flex gap-4 mb-8 border-b-2 border-deep-sea-400 overflow-x-auto">
          <button
            onClick={() => setActiveTab('analyze')}
            className={`px-6 py-3 font-semibold text-lg transition-all duration-300 whitespace-nowrap transform hover:scale-105 ${
              activeTab === 'analyze'
                ? 'text-deep-sea-900 border-b-4 border-deep-sea-900 shadow-md'
                : 'text-deep-sea-500 hover:text-deep-sea-700'
            }`}
          >
            📊 Analyze
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`px-6 py-3 font-semibold text-lg transition-all duration-300 whitespace-nowrap transform hover:scale-105 ${
              activeTab === 'history'
                ? 'text-deep-sea-900 border-b-4 border-deep-sea-900 shadow-md'
                : 'text-deep-sea-500 hover:text-deep-sea-700'
            }`}
          >
            📋 History ({history.length})
          </button>
        </div>

        {/* Content */}
        {activeTab === 'analyze' ? (
          <div className="grid lg:grid-cols-2 gap-8">
            <div className="animate-slide-in">
              <AnalysisForm onSubmit={handleAnalyze} loading={loading} />
            </div>
            <div className="animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
              {loading && (
                <div className="bg-white rounded-lg shadow-lg p-8 border-l-4 border-deep-sea-500">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="animate-spin">
                      <div className="w-12 h-12 border-4 border-deep-sea-200 border-t-deep-sea-600 rounded-full"></div>
                    </div>
                    <div>
                      <p className="text-lg font-bold text-deep-sea-900">Analyzing Your Resume...</p>
                      <p className="text-deep-sea-600 text-sm mt-1">Using AI to match your skills with the job</p>
                    </div>
                  </div>
                  <div className="bg-deep-sea-100 rounded-full h-2 overflow-hidden">
                    <div className="bg-deep-sea-600 h-full animate-pulse-soft" style={{ width: '70%' }}></div>
                  </div>
                </div>
              )}
              {error && (
                <div className="bg-red-50 border-l-4 border-red-500 rounded-lg p-6 mb-6 shadow-md animate-bounce-gentle">
                  <p className="text-red-700 font-bold text-lg flex items-center gap-2">❌ Error Occurred</p>
                  <p className="text-red-600 mt-3 whitespace-pre-wrap">{error}</p>
                  <button
                    onClick={() => setError(null)}
                    className="mt-4 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded font-semibold transition-all duration-300 transform hover:scale-105"
                  >
                    Dismiss Error
                  </button>
                </div>
              )}
              {results && !loading && <ResultsDisplay results={results} />}
              {!results && !error && !loading && (
                <div className="bg-white rounded-lg shadow-lg p-8 text-center border-2 border-dashed border-deep-sea-300 hover:border-deep-sea-500 transition-colors duration-300">
                  <div className="text-6xl mb-4 animate-bounce-gentle">🎯</div>
                  <p className="text-deep-sea-700 font-semibold text-lg">Submit your resume and job description to get started</p>
                  <p className="text-deep-sea-500 text-sm mt-2">Our AI will analyze the match and provide detailed insights</p>
                </div>
              )}
            </div>
          </div>
        ) : (
          <History history={history} />
        )}
      </main>
    </div>
  )
}

export default App
