import { Link } from 'react-router-dom'
export default function Home() {
  return <main className="max-w-3xl mx-auto p-8 text-center">
    <h1 className="text-4xl font-bold">AI Resume Analyzer</h1>
    <p className="mt-4 text-slate-600">Upload your CV (PDF or DOCX) and get an instant ATS-style score out of 100, a section-by-section breakdown, keyword match against a job description, and clear tips to improve it.</p>
    <Link to="/analyze" className="inline-block mt-6 bg-blue-700 text-white px-6 py-3 rounded-full">Analyze my CV</Link>
    <p className="mt-6 text-sm text-slate-500">English CVs only in v1. Scanned image-only PDFs need OCR, which is out of scope.</p>
  </main>
}
