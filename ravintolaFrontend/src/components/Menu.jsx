import { Link } from "react-router-dom";
import { Navbar,Nav } from "react-bootstrap";
const Menu = ({user, handleLogout}) => {

    

    return (
    
    <div>

    <Navbar collapseOnSelect expand="lg" bg="light-green" variant="light   ">
    <Navbar.Toggle aria-controls="responsive-navbar-nav" />
    <Navbar.Collapse id="responsive-navbar-nav">
    <Nav className="mr-auto">
      <Nav.Link href="#" as="span">
        <Link to='/'>Start</Link>
      </Nav.Link>
      <Nav.Link href="#" as="span">
      <Link to='/users' >Restaurants</Link>   
       </Nav.Link>
       <Nav.Link href="#" as="span">
       <em >
        {user.name} logged in <button onClick={handleLogout}>logout</button>
        </em>

      </Nav.Link>
     
    </Nav>
  </Navbar.Collapse>
</Navbar>

      
    </div>)
}

export default Menu

// <Link to='/'>Blogs</Link>
        //<Link to='/users'>IUsers</Link>{user.name} logged in <button onClick={handleLogout}>logout</button>{' '}
      