import React, { useState } from 'react'

function History({ history }) {
  const [expandedId, setExpandedId] = useState(null)

  if (history.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-12 text-center border-2 border-dashed border-gray-300">
        <p className="text-5xl mb-4">📋</p>
        <p className="text-gray-600 font-semibold text-lg">No analysis history yet</p>
        <p className="text-gray-500 mt-2">Your analysis results will appear here</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="grid gap-4">
        {history.map((item) => (
          <div key={item.id} className="bg-white rounded-lg shadow-lg overflow-hidden border-l-4 border-blue-500">
            <button
              onClick={() => setExpandedId(expandedId === item.id ? null : item.id)}
              className="w-full p-6 text-left hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-4">
                    <span className={`text-3xl font-bold ${
                      item.match_percentage >= 80
                        ? 'text-green-600'
                        : item.match_percentage >= 60
                        ? 'text-blue-600'
                        : 'text-yellow-600'
                    }`}>
                      {item.match_percentage}%
                    </span>
                    <div>
                      <p className="text-gray-500 text-sm">Match Score</p>
                      <p className="text-gray-400 text-xs">{item.timestamp}</p>
                    </div>
                  </div>
                </div>
                <span className={`text-2xl transition-transform ${expandedId === item.id ? 'rotate-180' : ''}`}>
                  ▼
                </span>
              </div>
            </button>

            {expandedId === item.id && (
              <div className="border-t border-gray-200 p-6 bg-gray-50">
                {/* Missing Skills */}
                {item.missing_skills && item.missing_skills.length > 0 && (
                  <div className="mb-6">
                    <h4 className="font-bold text-gray-800 mb-3">🚫 Missing Skills</h4>
                    <div className="flex flex-wrap gap-2">
                      {item.missing_skills.map((skill, idx) => (
                        <span key={idx} className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-medium">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Suggestions */}
                {item.improvement_suggestions && item.improvement_suggestions.length > 0 && (
                  <div>
                    <h4 className="font-bold text-gray-800 mb-3">💡 Suggestions</h4>
                    <ul className="space-y-2">
                      {item.improvement_suggestions.map((suggestion, idx) => (
                        <li key={idx} className="text-gray-700 text-sm flex items-start gap-2">
                          <span className="text-blue-600 font-bold mt-0.5">→</span>
                          <span>{suggestion}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default History
