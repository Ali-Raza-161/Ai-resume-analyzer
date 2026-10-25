import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
export default function Navbar() {
  const { user, logout } = useAuth()
  return <header className="bg-slate-900 text-white px-6 py-3 flex gap-5 items-center">
    <Link to="/" className="font-bold text-lg">AI Resume Analyzer</Link>
    <Link to="/analyze">Analyze</Link><Link to="/history">History</Link><Link to="/admin">Admin</Link>
    <span className="ml-auto">{user ? <>{user.name} <button className="underline ml-2" onClick={logout}>Logout</button></> : <><Link to="/login">Login</Link> <Link to="/register" className="ml-3">Register</Link></>}</span>
  </header>
}
