import React, { useContext } from 'react'
import './Cart.css'
// import CartItem from '../components/CartItem/CartItem'
import { CartContext } from '../components/CartContext'
import ProductCard from '../components/ProductCard/ProductCard';
import ButtonUsage from '../components/Button/Button';
import { Link } from 'react-router-dom';
import CartItem from '../components/CartItem/CartItem';


export default function Cart() {

  // const {id} = useParams();
  // const [cartItem , setCartItem] = useState([]);

  // useEffect(() => {
  //   async function fetchItem() {
  //     try {
  //       const res = await axios.get('https://fakestoreapi.com/products')
  //       setCartItem(res.data);
  //       console.log(res.data);
  //     } catch (error) {
  //       console.log(error);
  //     }
  //   }

  //   fetchItem();
  // },[id])

  const { cart, removeFromCart } = useContext(CartContext);
  console.log(cart)

  if (cart.length === 0) {
    return <div className='empty-cart-layout'><div className='empty-cart'>Your Cart is Empty.</div></div>
  }

  return (
    <div>
      <h1>Your Cart</h1>
      <div className='cart-layout'>
        {cart.map((item) =>
          // <ProductCard product={item} key={item.id}></ProductCard>
          <CartItem cartItem={item} key={item.id} removeFromCart={removeFromCart}></CartItem>
        )}
      </div>
    </div>
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
    //            <Link to='/cart'>
    //             <ButtonUsage value={'Remove From Cart'}></ButtonUsage>
    //            </Link>
    //           </div>
    //         </div>
    //   </div>
    //   </div>
    // </div>
  )
}
