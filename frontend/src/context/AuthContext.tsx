import { createContext, useContext, useState } from 'react'
import type { ReactNode } from 'react'
type User = { id: number; name: string; email: string; role?: string } | null
const Ctx = createContext<{ user: User; token: string | null; setAuth: (u: User, t: string) => void; logout: () => void }>({ user: null, token: null, setAuth: () => {}, logout: () => {} })
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User>(() => { try { return JSON.parse(localStorage.getItem('user') || 'null') } catch { return null } })
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))
  const setAuth = (u: User, t: string) => { setUser(u); setToken(t); localStorage.setItem('user', JSON.stringify(u)); localStorage.setItem('token', t) }
  const logout = () => { setUser(null); setToken(null); localStorage.removeItem('user'); localStorage.removeItem('token') }
  return <Ctx.Provider value={{ user, token, setAuth, logout }}>{children}</Ctx.Provider>
}
export const useAuth = () => useContext(Ctx)
