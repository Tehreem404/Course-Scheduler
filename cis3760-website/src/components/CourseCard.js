import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/esm/Button';
import React, { useState, useCallback } from 'react';
import './components.css';

function CourseCard(props) {
  const [reload, setReload] = useState(1);

  const handleClick = useCallback(async () => {
    const courseIndex = document.activeElement.value;
    props.courses.splice(courseIndex, 1); // gets rid of course in the selected courses array
    setReload((p) => p + 1); // reloads only the card components
  }, []);

  const courseCards = props.courses.map((item, index) => {
    const coursejson = JSON.parse(item); // props is sent as a string,
    // so you need to parse it as JSON

    return (
      <div className="col-auto" key={coursejson.courseNameSection}>
        <Card style={{ width: '18rem' }}>
          <Card.Header id="card-header">{coursejson.courseNameSection}</Card.Header>
          <Card.Body id="card-body">
            <Card.Title className="mb-1">{coursejson.courseTitle}</Card.Title>
            <Card.Subtitle className="mb-1 text-muted">
              Prof:
              {coursejson.Prof}
            </Card.Subtitle>
            <Card.Subtitle className="mb-1 text-muted">
              Status:
              {coursejson.Status}
            </Card.Subtitle>
            <Card.Subtitle className="mb-1 text-muted">
              Term:
              {coursejson.Term}
            </Card.Subtitle>
            <Card.Subtitle className="mb-1 text-muted">
              Academic Level:
              {coursejson.academicLevel}
            </Card.Subtitle>
            <Card.Subtitle className="mb-1 text-muted">
              Capacity:
              {coursejson.capacity}
            </Card.Subtitle>
            <Card.Subtitle className="mb-1 text-muted">
              Credit:
              {coursejson.credit}
            </Card.Subtitle>
            <Card.Subtitle className="mb-1 text-muted">
              Location:
              {coursejson.Location}
            </Card.Subtitle>
            <Card.Text className="mb-1">
              Lecture Info:
              {coursejson.LectureInfo}
            </Card.Text>
            <Card.Text className="mb-1">
              Lab Info:
              {coursejson.LabInfo}
            </Card.Text>
            <Card.Text className="mb-1">
              Seminar Info:
              {coursejson.SeminarInfo}
            </Card.Text>
            <Card.Text className="mb-1">
              Exam Info:
              {coursejson.ExamInfo}
            </Card.Text>
            <Button style={{ marginLeft: '0px' }} id="reg-button" value={index} onClick={handleClick}>Remove Course</Button>
          </Card.Body>
        </Card>
      </div>
    );
  });

  return (
    <div className="row p-3">
      <br />
      {Boolean(reload) && courseCards}
    </div>
  );
}

export default CourseCard;
// small change
