export default function TipsList({ tips }: { tips: { priority: string; text: string }[] }) {
  const order = { High: 0, Medium: 1, Low: 2 } as Record<string, number>
  const sorted = [...tips].sort((a, b) => (order[a.priority] ?? 9) - (order[b.priority] ?? 9))
  return <div className="bg-white border rounded-xl p-4"><h3 className="font-bold mb-2">Improvement tips</h3>{sorted.map((t, i) => <p key={i} className="py-1"><span className="font-semibold">[{t.priority}]</span> {t.text}</p>)}</div>
}
