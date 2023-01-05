import React from 'react';
import NavBar from './components/Navbar';
import './App.css';
import { Outlet } from "react-router-dom";

const App = () => (
  <div class="wrapper">
    <header class="header">
      <NavBar/>
    </header>
    <br />
    <main class="main">
      <Outlet />
    </main>
    <br />
    <footer class="footer">
        <section class="footer-section">About</section>
        <section class="footer-section">Contact</section>
        <section class="footer-section">...</section>
    </footer>
  </div>
);

export default App;