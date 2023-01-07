import './App.css';
import React, {
// useState, useEffect, useRef, useContext,
} from 'react';
import Header from './components/Header';
// import CoursesTable from './components/CoursesTable';
import Footer from './components/Footer';
import Semester from './components/Semester';

function App() {
  return (
    <div className="App">
      <Header />
      <body className="App-Body">
        <Semester />
        {/* <CoursesTable /> */}
      </body>
      <Footer />
    </div>
  );
}

export default App;
