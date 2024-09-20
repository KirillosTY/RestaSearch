import { createStore, combineReducers } from 'redux'
import { Provider } from 'react-redux'

import notificationRedu from './reducers/notificationRedu'
import { configureStore } from '@reduxjs/toolkit'
import userReducer from './reducers/userReducer'


const store = configureStore({
    reducer: {
     notification: notificationRedu,
     user: userReducer,
  
    }
  })


export default store