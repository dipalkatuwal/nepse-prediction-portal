
import './assets/css/style.css'
import Main from './components/Main.jsx'
import Register from './components/Register.jsx'
import Header from './components/Header.jsx'
import Footer from './components/Footer.jsx'
import Login from './components/Login.jsx'
import AuthProvider from './AuthProvider'

import {BrowserRouter, Routes, Route} from "react-router-dom"

function App() {

  return (
    <>
    <AuthProvider>
    <BrowserRouter>
    <Header />
      <Routes>
        <Route path='/' element ={<Main />}/>
        <Route path='/register' element = {<Register/>}/>
        <Route path='/login' element = {<Login/>}/>
      </Routes>
      <Footer />
    </BrowserRouter>
    </AuthProvider>
    
    </>
  )
}

export default App
