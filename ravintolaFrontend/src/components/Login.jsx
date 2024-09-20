import PropTypes from 'prop-types'
import React from 'react'
import { Table, Form, Button, FormGroup } from 'react-bootstrap'

const Login = ({ username, password, setUsername, setPassword, submit }) => {
  return (
    <Form onSubmit={submit}>
      <Form.Group>
      <Form.Label>username:</Form.Label>
      <Form.Control
          data-testid="username"
          type="text"
          value={username}
          name="username"
          onChange={setUsername}
        />
      </Form.Group>

      <Form.Group>
      <Form.Label>password:</Form.Label>
        <Form.Control
          data-testid="password"
          type="password"
          value={password}
          name="password"
          onChange={setPassword}
        />
      </Form.Group>
      <Button data-testid="login" variant="primary" type="submit">
        login
      </Button>
    </Form>
  )
}

Login.propTypes = {
  submit: PropTypes.func.isRequired,
  setUsername: PropTypes.func.isRequired,
  setPassword: PropTypes.func.isRequired,
  username: PropTypes.string.isRequired,
  password: PropTypes.string.isRequired,
}

export default Login
