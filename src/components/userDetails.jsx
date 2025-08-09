import React from 'react'
import { useSelector } from 'react-redux'
import './userDetails.css'


const userDetails = () => {
    const { email, password } = useSelector((state) => state.user);
    return (
        <div className='layout'>
            <div className='background'>
                <h1>My Profile</h1>
                <p>Email : {email}</p>
                <p>Password : {password}</p>
            </div>
        </div>
    )
}

export default userDetails