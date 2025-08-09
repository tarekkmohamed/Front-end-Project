import React from 'react'
import './CartItem.css'
import { Link } from 'react-router-dom'
import ButtonUsage from '../Button/Button';

const CartItem = ({ cartItem, removeFromCart }) => {
  return (
    // <div className='cart-layout'>
    //   <h1>Your Cart</h1>
    //   <div className="cart-container">
    //    <div className="single-cart">
    //         <div className="image">
    //           <img src={cartItem.image} alt={cartItem.title} />
    //         </div>
    //         <div className="text-container">
    //           <h2>{cartItem.title}</h2>
    //           <p>{cartItem.description}</p>
    //           <div className="shape-container">
    //             <p style={{backgroundColor : '#3E5F44' , color : 'white'}}>Category : {cartItem.category}</p>
    //             <p style={{ color : 'red' }}>${cartItem.price}</p>
    //           </div>
    //           <div className="cart-button">
    //            <Link onClick={() => removeFromCart(cartItem.id)} to='/cart'>
    //             <ButtonUsage value={'Remove From Cart'}></ButtonUsage>
    //            </Link>
    //           </div>
    //         </div>
    //   </div>
    //   </div>
    // </div>
    <div className='product-card'>
      <div className="image-container">
        <img src={cartItem.image} alt={cartItem.title} />
      </div>
      <div className="text-container">
        <h3>{cartItem.title}</h3>
        {/* <p className='desc'>{product.description}</p> */}
        <p className='price'>${cartItem.price}</p>
        <div className='rating'>
          <p>{cartItem.rating.rate}⭐</p>
          <p>{`(${cartItem.rating.count})`}</p>
        </div>
      </div>
      <div>
        <Link onClick={() => removeFromCart(cartItem.id)} to='/cart'>
          <ButtonUsage value={'Remove From Cart'}></ButtonUsage>
        </Link>
      </div>
    </div>
  )
}

export default CartItem;
