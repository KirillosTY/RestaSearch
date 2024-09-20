import { useState, useEffect } from 'react'
import {BrowserRouter as Router,
  Routes,Route,Link,
  useMatch,
  useNavigate
} from 'react-router-dom'

import loginService from './services/login'
import SuccessMessage from './components/SuccessMessage'
import FailureMessage from './components/FailureMessage'
import Login from './components/Login'
import {setNotifications} from './reducers/notificationRedu'
import { useDispatch, useSelector } from 'react-redux'
import { setUserLogged, setUserLoggedOut } from './reducers/userReducer'
import Menu from './components/Menu'


function App() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const user = useSelector(state => state.user)
  const notification = useSelector(state=> state.notification)


  const navigate = useNavigate()
  const dispatch = useDispatch()


  useEffect(() => {
    const userToJSON = window.localStorage.getItem('loggedInUser')
    if (userToJSON) {
      const userLogged = JSON.parse(userToJSON)
      dispatch(setUserLogged(userLogged))
    } else {
      console.log('nullia')
      //add error feedback
    }
  }, [])


  const handleLogin = event => {
    event.preventDefault()
    console.log('Logging in, please be patient!')

    try {
      loginService
        .login({ username, password })
        .then(response => {
          const userLogged = response
          window.localStorage.setItem(
            'loggedInUser',
            JSON.stringify(userLogged)
          )
          setUsername('')
          setPassword('')
         // blogService.setToken(userLogged.token)

          dispatch(setUserLogged(userLogged))
        })
        .catch(() => {

         dispatch(setNotifications('Wrong username or password, probably',5))
        })
    } catch (exception) {
      console.log(exception.message)
      dispatch(setNotifications('Wrong username or password, probably',5))
    }
  }

  const handleLogout = event => {
    event.preventDefault()
    window.localStorage.clear()
    setUsername('')
    setPassword('')
    dispatch(setUserLoggedOut())
    navigate('/')
  }

  const updateUsername = event => {
    event.preventDefault()
    setUsername(event.target.value)
  }

  const updatePassword = event => {
    event.preventDefault()
    setPassword(event.target.value)
  }


  return (
    <>
    <div  className="container">
      {user.username ==='' || user.token ===''? <div>
        <h2>Log in to application</h2>
        <FailureMessage failureMessage={notification}></FailureMessage>
        <Login
          submit={handleLogin}
          username={username}
          password={password}
          setUsername={updateUsername}
          setPassword={updatePassword}
        />
        </div>
        
      : 

      <div>
      <Menu user={user} handleLogout={handleLogout}></Menu>
      <h1>Restaurants</h1>
     <SuccessMessage successMessage={notification}></SuccessMessage>
   
      </div>
      } 
      </div>
    </>
  )
}

export default App
