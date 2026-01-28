import React from 'react'
import { downloadResultsAsPDF } from '../services/pdfExport'

function ResultsDisplay({ results }) {
  const [downloading, setDownloading] = React.useState(false)
  const [pdfMessage, setPdfMessage] = React.useState(null)
  const getMatchColor = (percentage) => {
    if (percentage >= 80) return 'text-green-600'
    if (percentage >= 60) return 'text-blue-600'
    if (percentage >= 40) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getMatchBgColor = (percentage) => {
    if (percentage >= 80) return 'bg-green-100'
    if (percentage >= 60) return 'bg-blue-100'
    if (percentage >= 40) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  const getMatchBorderColor = (percentage) => {
    if (percentage >= 80) return 'border-green-500'
    if (percentage >= 60) return 'border-blue-500'
    if (percentage >= 40) return 'border-yellow-500'
    return 'border-red-500'
  }

  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* Match Percentage */}
      <div className={`rounded-lg shadow-lg p-8 border-l-4 transform transition-all duration-300 hover:shadow-xl ${getMatchBgColor(results.match_percentage)} ${getMatchBorderColor(results.match_percentage)}`}>
        <p className="text-deep-sea-600 text-sm font-semibold mb-2">Match Score</p>
        <div className="flex items-baseline gap-3 mb-4">
          <span className={`text-7xl font-bold animate-pulse-soft ${getMatchColor(results.match_percentage)}`}>
            {results.match_percentage}%
          </span>
          <span className="text-deep-sea-700 text-lg font-semibold">
            {results.match_percentage >= 80
              ? '🎉 Excellent Match!'
              : results.match_percentage >= 60
              ? '✨ Good Match'
              : results.match_percentage >= 40
              ? '⚠️ Moderate Match'
              : '❌ Needs Work'}
          </span>
        </div>
        <div className="mt-4 bg-white rounded-full h-4 overflow-hidden shadow-inner">
          <div
            className={`h-full transition-all duration-1000 ease-out rounded-full ${
              results.match_percentage >= 80
                ? 'bg-gradient-to-r from-green-400 to-green-600'
                : results.match_percentage >= 60
                ? 'bg-gradient-to-r from-deep-sea-500 to-deep-sea-700'
                : results.match_percentage >= 40
                ? 'bg-gradient-to-r from-yellow-400 to-yellow-600'
                : 'bg-gradient-to-r from-red-400 to-red-600'
            }`}
            style={{ width: `${results.match_percentage}%` }}
          />
        </div>
      </div>

      {/* Matched Skills */}
      {results.matched_skills && results.matched_skills.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-green-500 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          <h3 className="text-xl font-bold text-deep-sea-900 mb-4 flex items-center gap-2">
            <span className="text-2xl animate-bounce-gentle">✅</span> Matched Skills
          </h3>
          <div className="space-y-2">
            {results.matched_skills.map((skill, index) => (
              <div key={index} className="bg-gradient-to-r from-green-50 to-transparent border border-green-200 rounded-lg p-3 flex items-start gap-3 hover:border-green-400 transition-colors duration-300">
                <span className="text-green-600 font-bold text-lg mt-0.5">✓</span>
                <p className="text-deep-sea-700 font-medium">{skill}</p>
              </div>
            ))}
          </div>
          <p className="text-sm text-deep-sea-600 mt-4">
            ✨ <span className="font-semibold">Great:</span> These skills match the job requirements.
          </p>
        </div>
      )}

      {/* Missing Skills */}
      {results.missing_skills && results.missing_skills.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-red-500 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          <h3 className="text-xl font-bold text-deep-sea-900 mb-4 flex items-center gap-2">
            <span className="text-2xl animate-bounce-gentle">🚫</span> Missing Skills
          </h3>
          <div className="space-y-2">
            {results.missing_skills.map((skill, index) => (
              <div key={index} className="bg-gradient-to-r from-red-50 to-transparent border border-red-200 rounded-lg p-3 flex items-start gap-3 hover:border-red-400 transition-colors duration-300">
                <span className="text-red-600 font-bold text-lg mt-0.5">✗</span>
                <p className="text-deep-sea-700">{skill}</p>
              </div>
            ))}
          </div>
          <p className="text-sm text-deep-sea-600 mt-4">
            💡 <span className="font-semibold">Opportunity:</span> Learning these skills could significantly improve your candidacy.
          </p>
        </div>
      )}

      {/* Improvement Suggestions */}
      {results.improvement_suggestions && results.improvement_suggestions.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-deep-sea-600 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          <h3 className="text-xl font-bold text-deep-sea-900 mb-4 flex items-center gap-2">
            <span className="text-2xl animate-bounce-gentle">💡</span> Improvement Suggestions
          </h3>
          <div className="space-y-3">
            {results.improvement_suggestions.map((suggestion, index) => (
              <div key={index} className="bg-gradient-to-r from-deep-sea-50 to-transparent border border-deep-sea-300 rounded-lg p-4 flex items-start gap-4 hover:border-deep-sea-500 transition-colors duration-300">
                <span className="bg-gradient-to-br from-deep-sea-900 to-deep-sea-700 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold flex-shrink-0 shadow-md">
                  {index + 1}
                </span>
                <p className="text-deep-sea-700 font-medium mt-0.5">{suggestion}</p>
              </div>
            ))}
          </div>
          <p className="text-sm text-deep-sea-600 mt-4">
            🎯 <span className="font-semibold">Action Plan:</span> Implement these changes to strengthen your application.
          </p>
        </div>
      )}

      {/* Metadata */}
      <div className="bg-gradient-to-r from-deep-sea-100 to-deep-sea-200 rounded-lg p-4 text-xs text-deep-sea-600 shadow-sm">
        <p>📅 Analyzed: {results.timestamp}</p>
      </div>

      {/* PDF Download Status Message */}
      {pdfMessage && (
        <div className={`rounded-lg p-5 border-l-4 animate-bounce-gentle shadow-lg ${
          pdfMessage.success 
            ? 'bg-gradient-to-r from-green-50 to-green-100 border-green-500' 
            : 'bg-gradient-to-r from-red-50 to-red-100 border-red-500'
        }`}>
          <p className={`font-bold text-lg flex items-center gap-2 ${pdfMessage.success ? 'text-green-700' : 'text-red-700'}`}>
            {pdfMessage.success ? '✅ Success!' : '❌ Error'}
          </p>
          <p className={`mt-2 text-sm ${pdfMessage.success ? 'text-green-600' : 'text-red-600'}`}>
            {pdfMessage.message}
          </p>
          <button
            onClick={() => setPdfMessage(null)}
            className="mt-3 text-sm font-semibold underline cursor-pointer hover:opacity-70 transition-opacity"
            style={{color: pdfMessage.success ? '#059669' : '#dc2626'}}
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Download PDF Button */}
      <button
        onClick={async () => {
          setDownloading(true)
          setPdfMessage(null)
          const result = await downloadResultsAsPDF(results, results.resumeText, results.jobDescriptionText)
          setPdfMessage(result)
          setDownloading(false)
        }}
        disabled={downloading}
        className="w-full bg-gradient-to-r from-deep-sea-900 via-deep-sea-700 to-deep-sea-600 hover:from-deep-sea-800 hover:via-deep-sea-600 hover:to-deep-sea-500 disabled:from-gray-400 disabled:via-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed text-white font-bold py-4 px-6 rounded-lg transition-all duration-300 transform hover:scale-105 hover:shadow-xl flex items-center justify-center gap-3 shadow-lg"
      >
        {downloading ? (
          <>
            <span className="inline-block animate-spin">⏳</span>
            <span>Generating PDF...</span>
          </>
        ) : (
          <>
            <span>📥</span>
            <span>Download as PDF</span>
          </>
        )}
      </button>
    </div>
  )
}

export default ResultsDisplay
