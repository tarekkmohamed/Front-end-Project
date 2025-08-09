import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navbar from './components/Navbar/Navbar'
import { Route, Routes } from 'react-router-dom'
import Home from './screens/Home'
import ProductDetails from './screens/ProductDetails'
import Cart from './screens/Cart'
import Login from './screens/Login'
import userDetails from './components/userDetails'

function App() {

  return (
    <>
        <Navbar></Navbar>
        <Routes>
          <Route path='/' Component={Home}></Route>
          <Route path='/product/:id' Component={ProductDetails}></Route>
          <Route path='/cart' Component={Cart}></Route>
          <Route path='/login-page' Component={Login}></Route>
          <Route path='/Profile-Page' Component={userDetails}></Route>
        </Routes>
    </>
  )
}

export default App
