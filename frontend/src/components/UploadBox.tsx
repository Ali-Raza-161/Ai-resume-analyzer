import { useState } from 'react'
export default function UploadBox({ onFile, onJd }: { onFile: (f: File) => void; onJd: (s: string) => void }) {
  const [drag, setDrag] = useState(false)
  return <div onDragOver={e => { e.preventDefault(); setDrag(true) }} onDragLeave={() => setDrag(false)}
    onDrop={e => { e.preventDefault(); setDrag(false); const f = e.dataTransfer.files[0]; if (f) onFile(f) }}
    className={`border-2 border-dashed rounded-xl p-8 text-center ${drag ? 'border-blue-600 bg-blue-50' : 'border-slate-300'}`}>
    <p className="font-semibold">Drag and drop your CV here (PDF or DOCX, max 5 MB)</p>
    <input className="mt-3" type="file" accept=".pdf,.docx" onChange={e => { const f = e.target.files?.[0]; if (f) onFile(f) }} />
    <textarea className="block w-full border rounded-lg p-3 mt-4" rows={4} placeholder="Optional: paste the target job description here" onChange={e => onJd(e.target.value)} />
  </div>
}
