import React from 'react'
import { LINKS } from '../../constants/links'
import { Link, NavLink } from 'react-router-dom'
import './Navbar.css'
import { FaBasketShopping } from "react-icons/fa6";
import ButtonUsage from '../Button/Button';

const Navbar = () => {
  return (
    <div className='nav-bar'>
      <div className='logo'>
        <FaBasketShopping style={{fontSize : '35px'}}/>
        <h1>Shopwise</h1>
      </div>
      <nav>
        {LINKS.map((item , index) => 
            <NavLink to={`/${item.to}`} key={index}>{item.value}</NavLink>
            )}
      </nav>
      <div>
      </div>
    </div>
  )
}
export default Navbar
