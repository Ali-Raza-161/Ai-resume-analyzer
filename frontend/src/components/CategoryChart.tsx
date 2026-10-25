export default function CategoryChart({ data }: { data: Record<string, number> }) {
  const max = 25
  return <div className="bg-white border rounded-xl p-4">{Object.entries(data).map(([k, v]) => <div key={k} className="my-2"><div className="flex justify-between text-sm"><span>{k}</span><span>{v}</span></div><div className="h-3 bg-slate-100 rounded"><div className="h-3 bg-blue-600 rounded" style={{ width: `${(v / max) * 100}%` }} /></div></div>)}</div>
}
