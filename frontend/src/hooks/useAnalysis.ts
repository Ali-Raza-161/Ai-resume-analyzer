import { useState } from 'react'
import { analyzeCv } from '../services/api'
export function useAnalysis() {
  const [result, setResult] = useState<any>(null); const [loading, setLoading] = useState(false); const [error, setError] = useState('')
  const run = async (file: File, jd: string) => { setLoading(true); setError(''); try { const r = await analyzeCv(file, jd); setResult(r); return r } catch (e: any) { setError(e.response?.data?.detail || 'Analysis failed'); throw e } finally { setLoading(false) } }
  return { result, loading, error, run, setResult }
}
