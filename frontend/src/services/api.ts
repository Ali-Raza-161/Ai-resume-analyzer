import axios from 'axios'
const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000' })
api.interceptors.request.use(c => { const t = localStorage.getItem('token'); if (t) c.headers.Authorization = `Bearer ${t}`; return c })
export default api
export const register = (d: any) => api.post('/api/auth/register', d).then(r => r.data)
export const login = (d: any) => api.post('/api/auth/login', d).then(r => r.data)
export const analyzeCv = (file: File, jd: string) => { const f = new FormData(); f.append('file', file); f.append('job_description', jd); return api.post('/api/resumes/analyze', f).then(r => r.data) }
export const listAnalyses = () => api.get('/api/analyses').then(r => r.data)
export const getAnalysis = (id: number) => api.get(`/api/analyses/${id}`).then(r => r.data)
export const deleteAnalysis = (id: number) => api.delete(`/api/analyses/${id}`).then(r => r.data)
export const adminStats = () => api.get('/api/admin/stats').then(r => r.data)
export const addSkill = (d: any) => api.post('/api/admin/skills', d).then(r => r.data)
