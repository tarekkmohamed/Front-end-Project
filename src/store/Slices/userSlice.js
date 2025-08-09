import {createSlice} from '@reduxjs/toolkit'

const userSlice = createSlice({
    initialState : {
        email : '' ,
        password : '' ,
    },
    name : 'user' ,
    reducers :{
        login : (state , action) => {
            state.email = action.payload.Email ;
            state.password = action.payload.Password ;
        } ,
        logout : (state) => {
            state.email = '' ;
            state.password = '' ;
        } 
    }
})

export const {login , logout} = userSlice.actions;

export default userSlice.reducer;