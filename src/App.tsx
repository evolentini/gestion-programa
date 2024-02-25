import { useState, useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import './App.css'

import { Navbar, ProtectedRoute } from './components'
import useProfile from './hooks/useProfile'
import useGoogleAuthLink from './hooks/useGoogleAuthLink'
import useGoogleAuthToken from './hooks/useGoogleAuthToken'
import { PAGINAS } from './constants/constants'

export default function App() {
  // TODO: Empujar el contenido del main hacia la izquierda si se abre el sidebar
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const { refetch: fetchProfile } = useProfile()
  const { data: googleAuth, refetch: fetchGoogleAuth } = useGoogleAuthLink()
  const { mutate, isSuccess } = useGoogleAuthToken()

  useEffect(() => {
    const searchParams = new URLSearchParams(document.location.search)

    const code = searchParams.get('code')
    const state = searchParams.get('state')

    if (code && state) {
      mutate({ code, state })
    }
  }, [mutate])

  useEffect(() => {
    if (isSuccess) {
      // fetchProfile()
    }
  }, [isSuccess, fetchProfile])

  useEffect(() => {
    if (googleAuth) {
      window.location.replace(googleAuth.authorizationUrl)
    }
  }, [googleAuth])

  // Handlers
  const handleGoogleLogin = () => {
    fetchGoogleAuth()
  }

  const handleLogout = () => {
    localStorage.removeItem('token') // Remueve el token

    // Redirecciona a la página principal
    // TODO: Cambiar por la página de login
    // TODO: Implementar en el backend
    window.location.href = '/'
  }

  return (
    <>
      <Navbar
        isSidebarOpen={isSidebarOpen}
        setIsSidebarOpen={setIsSidebarOpen}
        handleLogin={handleGoogleLogin}
        handleLogout={handleLogout}
      />
      <main className={`main-content ${isSidebarOpen ? 'sidebar-active' : ''}`}>
        <ProtectedRoute>
          <Routes>
            {PAGINAS.map((pagina) => (
              <Route
                key={pagina.key}
                path={pagina.path}
                element={
                  pagina.modo ? (
                    <pagina.component modo={pagina.modo} />
                  ) : (
                    <pagina.component />
                  )
                }
              />
            ))}
            <Route path="*" element={<h1>Not found</h1>} />
          </Routes>
        </ProtectedRoute>
      </main>
    </>
  )
}
