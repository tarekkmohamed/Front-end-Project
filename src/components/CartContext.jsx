import React from 'react'
import { createContext, useState } from 'react'


export const CartContext = createContext();

export function CartProvider({ children }) {

    const [cart, setCart] = useState([]);

    const addToCart =  (product) => {
        
        const exist = cart.find(item => item.id == product.id)
        if (exist){
            {window.alert('This Product is Already in Your Cart')}
            return
        }
        setCart((prev) => [...prev,product])
        window.alert('The Product Added To Your Cart!')
    }

    const removeFromCart = (id) => {
        setCart((prev) => prev.filter(item => item.id !== id))
    }

    return (
        <CartContext.Provider value={{ cart , addToCart , removeFromCart }}>
            {children}
        </CartContext.Provider>
    )
}

