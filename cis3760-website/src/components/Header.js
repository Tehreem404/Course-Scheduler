// import Container from 'react-bootstrap/Container';
// import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import './components.css';

function Header() {
  return (
    <>
      <Navbar className="colour-nav justify-content-center" variant="dark">
        <Navbar.Brand href="#home">Course Catalog</Navbar.Brand>
      </Navbar>
    </>
  );
}
// change
export default Header;
