import Button from '@mui/material/Button';
import axios from 'axios';
import React, { useContext, useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import ButtonUsage from '../components/Button/Button';
import { CartContext } from '../components/CartContext';

const ProductDetails = () => {
  const { id } = useParams();
  const [product, setProduct] = useState([]);
  // const [Cart , setCart] = useState([]);
  const { addToCart } = useContext(CartContext);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchProduct() {
      try {
        const res = await axios.get(`https://fakestoreapi.com/products/${id}`)
        setProduct(res.data);
        // console.log(res.data);
      } catch (error) {
        console.log(error);
      }
    }

    fetchProduct();
  }, [id])


  // function addToCart({product}) {
  //   setCart(product)
  //   window.alert('Product Added Successfully')
  //   console.log(Cart)
  // }

  return (
    <div className='productDetails-layout'>
      <div className='header'>
        <span onClick={() => navigate('/')}>🔙</span>
        <h1>Product Details</h1>
      </div>
      <div className="single-product">
        <div className="image">
          <img src={product.image} alt={product.title} />
        </div>
        <div className="text-container">
          <h2>{product.title}</h2>
          <p>{product.description}</p>
          <div className="shape-container">
            <p style={{ backgroundColor: '#3E5F44', color: 'white' }}>Category : {product.category}</p>
            <p style={{ color: 'red' }}>${product.price}</p>
          </div>
          <div className="cart-button">
            <Link onClick={() => addToCart(product)}>
              <ButtonUsage value={'Add To Cart 🛒'}></ButtonUsage>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProductDetails
