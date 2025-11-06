
import './assets/css/style.css'
import Main from './components/Main.jsx'
import Register from './components/Register.jsx'
import Header from './components/Header.jsx'
import Footer from './components/Footer.jsx'
import Login from './components/Login.jsx'
import AuthProvider from './AuthProvider'
import Dashboard from './components/dashboard/Dashboard'
import PrivateRoute from './PrivateRoute'
import PublicRoute from './PublicRoute'

import {BrowserRouter, Routes, Route} from "react-router-dom"

function App() {

  return (
    <>
    <AuthProvider>
    <BrowserRouter>
    <Header />
      <Routes>
        <Route path='/' element ={<Main />}/>
        <Route path='/register' element = {<PublicRoute><Register /></PublicRoute>}/>
        <Route path='/login' element = {<PublicRoute><Login/></PublicRoute>}/>
        <Route path ='/dashboard' element={<PrivateRoute><Dashboard /></PrivateRoute>}></Route>
      
      </Routes>
      <Footer />
    </BrowserRouter>
    </AuthProvider>
    
    </>
  )
}

export default App
