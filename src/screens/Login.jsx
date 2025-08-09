import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import './Login.css'
import Checkbox from '@mui/material/Checkbox';
import ButtonUsage from '../components/Button/Button';
import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { useDispatch } from 'react-redux'
import { login } from '../store/Slices/userSlice';
import { useEffect } from 'react';

const Login = () => {

  const label = { inputProps: { 'aria-label': 'Checkbox demo' } };
  const [Email, setEmail] = useState('');
  const [Password, setPassword] = useState('');

  const navigate = useNavigate();

  const dispatch = useDispatch();

  function handleLogin(ev) {
    ev.preventDefault();
    dispatch(login({ Email, Password }));
    console.log(ev.target.value);
    navigate('/Profile-Page');
  }


  return (
    <div className='background'>
      <div className='login-layout'>
        <h1>Login</h1>
        <form onSubmit={handleLogin}>
          <div className='input-container'>
            {/* <div className='row'>
                <label htmlFor="email">Email</label>
                <input type="email"
                  name='email'
                  id='email'
                  className='email-input'
                  placeholder='email address...'
                  value={Email}
                  onChange={(ev) => {
                    setEmail(ev.target.value);
                  }}
                //  ref={emailRef}
                />
              </div> */}
            {/* <div className='row'>
                <label htmlFor="password">Password</label>
                <input type="password"
                  name='password'
                  id='password'
                  className='password-input'
                  value={Password}
                  onChange={(ev) => {
                    setPassword(ev.target.value);
                  }}
                //  ref={passwordRef}
                />
              </div> */}

            <TextField
              required
              id="standard-required"
              label="Email"
              variant="standard"
              type='email'
              value={Email}
              onChange={ ev => setEmail(ev.target.value)}
            />
            <TextField
              id="standard-password-input"
              label="Password"
              type="password"
              autoComplete="current-password"
              variant="standard"
              value={Password}
              onChange={ev => setPassword(ev.target.value) }
            />
          </div>
          <div className='checkbox-contianer'>
            <div>
              <Checkbox {...label} id='checkbox' />
              <label htmlFor="checkbox">Remember Me</label>
            </div>
            <p>Forgot Password?</p>
          </div>
          <div className='custom-btn'>
            {/* <ButtonUsage value='Login'></ButtonUsage> */}
            <button type='submit'>Login</button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default Login
