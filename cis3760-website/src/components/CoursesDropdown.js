import Dropdown from 'react-bootstrap/Dropdown';
/* eslint-disable */
import React from 'react';
/* eslint-enable */
import './components.css';

function CoursesDropdown({ reccomend }) {
  return (
    <div>
      <Dropdown>
        <Dropdown.Toggle id="nav-dropdown" title="Dropdown button">
          Get Recommonded Courses
        </Dropdown.Toggle>
        <Dropdown.Menu>
          <Dropdown.Item id="Mon" onClick={reccomend}>Only Mon/Wed/Fri Courses</Dropdown.Item>
          <Dropdown.Item id="Tues" onClick={reccomend}>Only Tues/Thurs Courses</Dropdown.Item>
        </Dropdown.Menu>
      </Dropdown>
    </div>
  );
}

export default CoursesDropdown;
// random
