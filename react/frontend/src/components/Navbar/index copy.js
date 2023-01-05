import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

function NavScroll() {
  return (
    <Navbar bg="light" expand="sm">
      <Container fluid>
        <Navbar.Brand href="/">swtpc</Navbar.Brand>
        <Navbar.Toggle aria-controls="navbarScroll" />
        <Navbar.Collapse id="navbarScroll">
          <Nav
            className="me-auto my-2 my-lg-0"
            style={{ maxHeight: '100px' }}
          >
            <NavDropdown title="Treatment Methods" id="navbarScrollingDropdown-tmethods">
              <NavDropdown.Item href="floc">Flocculation Analyzer</NavDropdown.Item>
              <NavDropdown.Item href="bsf">BSF Conceptualizer</NavDropdown.Item>
              <NavDropdown.Item href="bsf">SODIS Forecaster</NavDropdown.Item>
              <NavDropdown.Item href="bsf">Flouride Terminator</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="Knowledge Base" id="navbarScrollingDropdown-kbase">
              <NavDropdown.Item href="faq">FAQ</NavDropdown.Item>
              <NavDropdown.Item href="wiki">Wiki</NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavScroll;