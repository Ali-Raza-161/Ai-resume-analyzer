export default function ScoreCard({ score }: { score: number }) {
  return <div className="bg-white border rounded-2xl p-6 text-center shadow"><p className="text-slate-500">Overall ATS score</p><p className="text-5xl font-bold text-blue-700">{score} / 100</p></div>
}
