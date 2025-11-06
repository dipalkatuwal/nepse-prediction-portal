import { useContext } from 'react'
import { AuthContext } from './AuthProvider'
import { Navigate } from 'react-router-dom'

const PublicRoute = ({ children }) => {
  const { isloggedIn } = useContext(AuthContext)

  return !isloggedIn ? (
    children
  ) : (
    <Navigate to="/dashboard" replace />
  )
}

export default PublicRoute
