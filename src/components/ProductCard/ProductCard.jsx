import React from 'react'
import './ProductCard.css'
import ButtonUsage from '../Button/Button'
import { Link } from 'react-router-dom'

const ProductCard = ({product}) => {
  return (
    <div className='product-card'> 
      <div className="image-container">
        <img src={product.image} alt={product.title} />
      </div>
      <div className="text-container">
        <h3>{product.title}</h3>
        {/* <p className='desc'>{product.description}</p> */}
        <p className='price'>${product.price}</p>
        <div className='rating'>
          <p>{product.rating.rate}⭐</p>
          <p>{`(${product.rating.count})`}</p>
        </div>
      </div>
      <div>
        <Link to={`/product/${product.id}`}>
           <ButtonUsage value={'Show More'}></ButtonUsage>
        </Link>
      </div>
    </div>
  )
}

export default ProductCard
