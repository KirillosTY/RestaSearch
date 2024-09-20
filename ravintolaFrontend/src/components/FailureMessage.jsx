import failureStyles from '.././styles/failurePopup.css'
import { Alert } from 'react-bootstrap'

const FailureMessage = ({ failureMessage }) => {
  if (failureMessage) {
    return <div className="container">
    {(failureMessage &&
      <Alert variant="danger">
        {failureMessage}
      </Alert>
    )}
    
  </div>
  }
}

export default FailureMessage
