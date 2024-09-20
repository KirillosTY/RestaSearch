import { createSlice } from "@reduxjs/toolkit";
import { useReducer } from "react";


const user = {
    user: '',
    username: '',
    token: ''
}


const userRedcuer = createSlice({
    name: 'user',
    initialState: user,
    reducers: {
        setUserLogged(state,action){
            console.log(action.payload,'thi')
            return action.payload
        },
        setUserLoggedOut(state,action){
            state.token = ''
            console.log(state, 'useer')
            return state
        }
    }
})



export const {setUserLogged, setUserLoggedOut} = userRedcuer.actions

export default userRedcuer.reducer