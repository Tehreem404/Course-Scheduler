import React, { useState, useEffect } from 'react';
import './components.css';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Badge from 'react-bootstrap/Badge';

function SearchCourse({ handleClick, data, resetBtn }) {
  const [courseName, setCourseName] = useState('');

  useEffect(() => {
    setCourseName(data);
  }, [data]);

  return (
    <div>
      <Form>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Enter Course Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="example: CIS*1300"
            required
            className="w-50"
            value={courseName}
            onChange={(e) => setCourseName(e.target.value)}
          />
        </Form.Group>
        <Button style={{ float: 'left' }} id="reg-button" type="submit" onClick={() => handleClick(courseName)}>
          Submit
        </Button>
        <Button style={{ float: 'left' }} id="ghost-button" type="submit" onClick={() => resetBtn()}> Reset </Button>
        <h2 style={{ float: 'right' }}>
          <Badge pill bg="light" style={{ color: 'darkslateblue' }}>
            {' '}
            {data}
          </Badge>
        </h2>
      </Form>
      <br />
    </div>
  );
}
// change
export default SearchCourse;
