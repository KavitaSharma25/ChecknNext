import React from 'react'

function Header() {
  return (
    <header className="bg-gradient-to-r from-white via-deep-sea-50 to-white shadow-xl border-b-4 border-deep-sea-500 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-between gap-6">
          <div className="flex-1 flex items-center gap-4">
            {/* Logo */}
            <div className="w-16 h-16 flex-shrink-0">
              <img src="/Screenshot 2026-01-28 113104.png" alt="ChecknNext Logo" className="w-full h-full object-cover rounded-lg drop-shadow-lg hover:drop-shadow-xl transition-all duration-300" />
            </div>

            {/* Title */}
            <div>
              <h1 className="text-5xl sm:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-deep-sea-900 via-deep-sea-600 to-deep-sea-400 animate-fade-in-up">
                ChecknNext
              </h1>
              <p className="text-deep-sea-600 mt-1 text-lg font-semibold">AI-Powered Resume-JD Matcher</p>
            </div>
          </div>

          {/* Info Card */}
          <div className="text-right hidden sm:block">
            <div className="bg-gradient-to-r from-deep-sea-100 to-deep-sea-200 rounded-lg p-4 shadow-md border border-deep-sea-300">
              <p className="text-deep-sea-700 font-bold text-sm">🚀 Instant Analysis</p>
              <p className="text-deep-sea-600 text-xs mt-2 leading-relaxed max-w-xs">Find the perfect match between your resume and job requirements</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
