import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import './components.css';
import CoursesTable from './CoursesTable';

function Semester() {
  const [semester, setSemester] = useState(' F22');

  function changeSemester() {
    const sem = document.activeElement.value;

    if (sem !== semester) {
      console.log('changed the table');
      setSemester(sem);
    }
  }

  return (
    <div className="sem-body">
      <div className="row p-3 justify-content-center">
        <div className="col-auto">
          <Button id="ghost-button" size="lg" value=" F22" onClick={changeSemester}> F22 </Button>
        </div>
        <div className="col-auto">
          <Button id="ghost-button" size="lg" value=" W23" onClick={changeSemester}> W23 </Button>
        </div>
      </div>
      <h2 className="header-sem">
        The current Semester is:
        { semester }
      </h2>
      { CoursesTable(semester) }
    </div>
  );
}

export default Semester;
