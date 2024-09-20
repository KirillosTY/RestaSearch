import SuccessStyles from '.././styles/successPopup.css'
import { Alert } from 'react-bootstrap'

const SuccessMessage = ({ successMessage }) => {
  if (successMessage) {
    return (
    <div className="container">
    {(successMessage &&
      <Alert variant="success">
        {successMessage}
      </Alert>
      
    )}
    </div>
  )}
  
}

export default SuccessMessage
