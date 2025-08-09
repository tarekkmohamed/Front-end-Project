import React, { useEffect, useState } from 'react'
import axios from 'axios'
import ProductCard from '../components/ProductCard/ProductCard';

const Home = () => {
  const [products , setProducts] = useState([]);

  useEffect(() => {
    async function fetchProducts() {
        try {
            const res = await axios.get('https://fakestoreapi.com/products');
            setProducts(res.data);
            // console.log(res.data)
        } catch (error) {
            console.log(error);
        }
    }
    fetchProducts();
  },[])
  return (
    <div className='home-container'>
      <h1>Our Products</h1>
      <div className="products-container">
        {products.map((item) =>
           <ProductCard product={item} key={item.id}></ProductCard>
         )}
      </div>
    </div>
  )
}

export default Home
