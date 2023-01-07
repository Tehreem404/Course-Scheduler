import Table from 'react-bootstrap/Table';
import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import CourseCard from './CourseCard';
import Schedule from './Schedule';
import './components.css';
import SearchCourse from './SearchCourse';
import CoursesDropdown from './CoursesDropdown';

let selectedCourses = [];
let conflictMessage = '';

function CoursesTable(semester) {
  const sem = semester.trim();
  const [loading, setLoading] = React.useState([]);
  const [courses, setCourses] = React.useState([]);
  const [courseID, setCourseID] = useState(null);
  const [schedCourses, setSched] = React.useState([]);
  const [courseName, setCourseName] = useState(null);
  const [loadSchedule, setLoadSchedule] = useState(false);
  const [chosenCourses, setChosenCourses] = useState(true);
  const [conflict, setConflict] = useState(false);
  const [recc, setRecc] = useState(false);
  const [dday, setDDay] = useState('Mon/Wed/Fri');

  // loads all courses in table when page loads
  useEffect(() => {
    console.log('the current semester is ', sem);
    selectedCourses = [];
    setCourseID(null);
    setCourseName('');
    setRecc(false);

    setLoadSchedule(true);
    setSched([]);
    setLoadSchedule(false);

    setLoading(true);
    fetch(`/api/getAllCourses/${sem}`).then((res) => res.json()).then((data) => {
      setCourses(data.Items);
      setLoading(false);
    })
      .catch((error) => {
        console.error(error);
        setLoading(false);
      });
  }, [sem]);

  // takes a string day ("Mon", "Tue", etc.) and returns the calender day (12, 13, etc.) of the first day of classes in F22 semester
  function weekDayToCalDayF22(day) {
    if (day == 'Mon') {
      return 12;
    } if (day == 'Tue') {
      return 13;
    } if (day == 'Wed') {
      return 14;
    } if (day == 'Thu') {
      return 8;
    } if (day == 'Fri') {
      return 9;
    }
    return null;
  }

  // takes a string day ("Mon", "Tue", etc.) and returns the calender day (12, 13, etc.) of the first day of classes in W23 semester
  function weekDayToCalDayW23(day) {
    if (day == 'Mon') {
      return 9;
    } if (day == 'Tue') {
      return 10;
    } if (day == 'Wed') {
      return 11;
    } if (day == 'Thu') {
      return 12;
    } if (day == 'Fri') {
      return 13;
    }
    return null;
  }

  function AlertConflict() {
    if (conflict) {
      return (
        <>
          <br />
          <Alert variant="danger" onClose={() => setConflict(false)} dismissible>
            <Alert.Heading>Course Conflict</Alert.Heading>
            <p>{conflictMessage}</p>
          </Alert>
        </>

      );
    }
    return <></>;
  }

  function createSchedule() {
    event.preventDefault();

    const coursesINFO = { courses: [] };

    for (let i = 0; i < (courseID.courses).length; i++) {
      const c = JSON.parse(courseID.courses[i]);
      coursesINFO.courses.push(c.courseNameSection);
    }

    setLoadSchedule(true);
    fetch(`/api/checkconflict/${JSON.stringify(coursesINFO)}/${sem}`).then((res) => res.json()).then((data) => {
      const scheduledMeetings = [];
      const meetingsArr = data.api_data;

      for (let i = 0; i < meetingsArr.length; i++) { // go through every meeting time
        const meeting = meetingsArr[i];
        const startTime = meeting.startTime.split(':');
        const endTime = meeting.endTime.split(':');

        if (meeting.type == 'LEC' || meeting.type == 'LAB' || meeting.type == 'SEM') {
          let day = null;
          let month = null;
          let year = null;

          if (sem == 'F22') { // date variables for Fall 2022 semester
            day = weekDayToCalDayF22(meeting.day);
            month = 8;
            year = 2022;
          } else { // date variables for Winter 2023 semester
            day = weekDayToCalDayW23(meeting.day);
            month = 0;
            year = 2023;
          }

          scheduledMeetings.push({ // add meeting in AppointmentModel format
            title: `${meeting.title} (${meeting.type})`,
            startDate: new Date(year, month, day, parseInt(startTime[0]), parseInt(startTime[1])),
            endDate: new Date(year, month, day, parseInt(endTime[0]), parseInt(endTime[1])),
            id: i,
            type: meeting.type,
            location: meeting.location,
            conflict: meeting.conflict,
            rRule: 'FREQ=WEEKLY;COUNT=12',
          });
        } else { // if type == "EXA" (for exam times, gonna have different rRule):

          // implement in future sprint

        }
      }

      setSched(scheduledMeetings);
      console.log('scheduled meetings: ', scheduledMeetings);
      setLoadSchedule(false);
    })
      .catch((error) => {
        console.error(error);
        setLoadSchedule(false);
      });
  }

  const alertClicked = () => {
    const activeItemValue = document.activeElement.value;

    const tobeadded = JSON.parse(activeItemValue).courseNameSection;
    const coursesInSch = [];

    if (selectedCourses.length > 0) {
      for (let i = 0; i < (selectedCourses).length; i++) {
        const c = JSON.parse(selectedCourses[i]);
        coursesInSch.push(c.courseNameSection);
      }

      setChosenCourses(false);
      fetch(`/api/isConflict/${tobeadded}/${coursesInSch}/${sem}`).then((res) => res.json()).then((data) => {
        if ((data.api_data).length > 0) {
          let message = '';
          console.log('conflict is : ', data.api_data);
          for (let i = 0; i < (data.api_data).length; i++) {
            const text = data.api_data[i].conflict;
            message = message.concat(text);
            message = message.concat('\n');
            console.log(message);
          }
          conflictMessage = message;
          setConflict(true);
        }
        setChosenCourses(true);
      })
        .catch((error) => {
          console.error(error);
          setChosenCourses(true);
        });
    }

    selectedCourses.push(activeItemValue);
    setCourseID({ courses: selectedCourses });
  };

  const handleClick = (childdata) => {
    event.preventDefault();
    setCourseName(childdata);

    setLoading(true);
    fetch(`/api/byname/${childdata}/${sem}`).then((res) => res.json()).then((data) => {
      setCourses(data.Items);
      console.log(data.Items);
      setLoading(false);
    })
      .catch((error) => {
        console.error(error);
        setLoading(false);
      });
  };

  const resetBtn = () => {
    event.preventDefault();
    setLoading(true);
    fetch(`/api/getAllCourses/${sem}`).then((res) => res.json()).then((data) => {
      setCourses(data.Items);
      setLoading(false);
      setRecc(false);
    })
      .catch((error) => {
        console.error(error);
        setLoading(false);
      });
    setCourseName('');
  };

  const reccomend = () => {
    const activeItemValue = document.activeElement.id;
    console.log('clicked reccomendation', activeItemValue);
    if (activeItemValue === 'Tues') {
      setDDay('Tues/Thurs');
    } else {
      setDDay('Mon/Wed/Friday');
    }

    // a fecth call we have to be made here
    setLoading(true);
    fetch(`/api/getFilteredCourses/${sem}/${activeItemValue}`, { method: 'POST', body: JSON.stringify(courses) })
      .then((res) => res.json()).then((data) => {
        console.log(data.api_data);
        if (data.api_data.length == 0) {
          alert('No classes found :(');
        }
        // setCourses(data.api_data);
        // alert(courses);
        let coursesText = '\n';
        for (let i = 0; i < data.api_data.length; i++) {
          coursesText += data.api_data[i];
          coursesText += ' ';
        }
        setCourses(data.api_data);
        setRecc(coursesText);
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setLoading(false);
      });
  };

  function ReccAlert() {
    if (recc) {
      return (
        <>
          <br />
          <Alert variant="light" onClose={() => setRecc(false)} dismissible>
            {/* eslint-disable */}
            <Alert.Heading>Your {dday} Recommonded courses are Loaded in the table below</Alert.Heading>
            {/* eslint-enable */}
          </Alert>
        </>

      );
    }
    return <></>;
  }

  const courseTable = () => (
    <div className="tableFixHead">
      <Table striped hover size="sm">
        <thead>
          <tr>
            <th>Add</th>
            <th>Course Name</th>
            <th>Meeting Info</th>
          </tr>
        </thead>
        <tbody>
          {courses.map((item) => (
            <tr id={item.courseNameSection} key={item.courseNameSection}>
              <th id="table-button">
                <Button onClick={alertClicked} id="reg-button" value={JSON.stringify(item)}> Add </Button>
              </th>
              <th>{item.courseNameSection}</th>
              <th>{item.meetingInfo}</th>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );

  return (
    <>
      <br />
      <SearchCourse handleClick={handleClick} data={courseName} resetBtn={resetBtn} />
      <CoursesDropdown reccomend={reccomend} />
      {/* eslint-disable */}
      {/* {recc ? <h4> Your reccomoneded Courses are: <br /> {recc} </h4> : <p />} */}
      {recc ? ReccAlert() : <p />}
      {/* eslint-enable */}
      <br />
      {loading ? <p>Loading... </p> : courseTable()}
      {conflict ? AlertConflict() : <br />}
      {chosenCourses ? courseID && <CourseCard {... courseID} /> : <p>Searching for conflicts ... </p>}
      <br />
      <Button size="lg" id="ghost-button" onClick={createSchedule}>Create Schedule</Button>
      {' '}
      {/* maybe try to get this to show up only when there are cards? (idk how) */}
      <br />
      <br />
      {loadSchedule ? <p>Loading Course Schedule... </p> : Schedule(schedCourses, sem)}
    </>

  );
}

export default CoursesTable;
