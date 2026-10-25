export default function SkillsList({ matched, missing }: { matched: string[]; missing: string[] }) {
  return <div className="grid md:grid-cols-2 gap-4">
    <div className="bg-green-50 border rounded-xl p-4"><h3 className="font-bold">Matched skills</h3>{matched.length ? matched.map(s => <span key={s} className="inline-block bg-white border rounded-full px-3 py-1 m-1 text-sm">{s}</span>) : <p>None yet</p>}</div>
    <div className="bg-red-50 border rounded-xl p-4"><h3 className="font-bold">Missing skills</h3>{missing.length ? missing.map(s => <span key={s} className="inline-block bg-white border rounded-full px-3 py-1 m-1 text-sm">{s}</span>) : <p>None — good match</p>}</div>
  </div>
}
