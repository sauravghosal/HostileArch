import React from "react";
import "./App.css";
import Description from "./components/Description";
import Email from "./components/Email";
import Picture from "./components/Picture";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

function App() {
  return (
    <div className="App">
      <Container>
        <Picture />
        <Description />
        <Email />
      </Container>
    </div>
  );
}

export default App;
