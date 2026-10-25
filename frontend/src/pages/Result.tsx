import { useEffect, useState } from 'react'; import { useParams } from 'react-router-dom'; import { getAnalysis } from '../services/api'; import ScoreCard from '../components/ScoreCard'; import SkillsList from '../components/SkillsList'; import TipsList from '../components/TipsList'; import CategoryChart from '../components/CategoryChart'
export default function Result() { const { id } = useParams(); const [a, setA] = useState<any>(null)
  useEffect(() => { if (id) getAnalysis(Number(id)).then(setA).catch(() => {}) }, [id])
  if (!a) return <p className="p-8">Loading result…</p>
  return <main className="max-w-3xl mx-auto p-8 space-y-4"><ScoreCard score={a.overall_score} /><CategoryChart data={a.category_scores} /><SkillsList matched={a.matched_skills} missing={a.missing_skills} /><TipsList tips={a.tips} /><a className="inline-block bg-slate-900 text-white px-5 py-2 rounded-full" href={`http://localhost:8000/api/analyses/${a.id}/report`}>Download PDF report (via API)</a></main> }
