import {createSlice} from '@reduxjs/toolkit'


const notification = ''

const notificationSetter =  createSlice({
    name: 'notification',
    initialState: notification,
    reducers: {
        setNotification(state,action){
           
            return action.payload
        
        },
        clearNotification(state,action){
           return ''
        }

    }
})

export const setNotifications =(notification, time) => {

    return (dispatch)=> {
        dispatch(setNotification(notification))
        
        setTimeout(()=> {
            dispatch(clearNotification())
    
        
          },time*1000)
        }
}


export const {setNotification, clearNotification} = notificationSetter.actions

export default notificationSetter.reducer