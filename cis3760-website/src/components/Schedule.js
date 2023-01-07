import * as React from 'react';
import { styled, alpha } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import { ViewState } from '@devexpress/dx-react-scheduler';
import {
  Scheduler,
  WeekView,
  Appointments,
  Toolbar,
  DateNavigator,
  TodayButton,
  AppointmentTooltip,
} from '@devexpress/dx-react-scheduler-material-ui';

const PREFIX = 'Demo';

const classes = {
  todayCell: `${PREFIX}-todayCell`,
  weekendCell: `${PREFIX}-weekendCell`,
  today: `${PREFIX}-today`,
  weekend: `${PREFIX}-weekend`,
};

const StyledWeekViewTimeTableCell = styled(WeekView.TimeTableCell)(({ theme }) => ({
  [`&.${classes.todayCell}`]: {
    backgroundColor: alpha(theme.palette.primary.main, 0.1),
    '&:hover': {
      backgroundColor: alpha(theme.palette.primary.main, 0.14),
    },
    '&:focus': {
      backgroundColor: alpha(theme.palette.primary.main, 0.16),
    },
  },
  [`&.${classes.weekendCell}`]: {
    backgroundColor: alpha(theme.palette.action.disabledBackground, 0.04),
    '&:hover': {
      backgroundColor: alpha(theme.palette.action.disabledBackground, 0.04),
    },
    '&:focus': {
      backgroundColor: alpha(theme.palette.action.disabledBackground, 0.04),
    },
  },
}));

const StyledWeekViewDayScaleCell = styled(WeekView.DayScaleCell)(({ theme }) => ({
  [`&.${classes.today}`]: {
    backgroundColor: alpha(theme.palette.primary.main, 0.16),
  },
  [`&.${classes.weekend}`]: {
    backgroundColor: alpha(theme.palette.action.disabledBackground, 0.06),
  },
}));

function TimeTableCell(props) {
  const { startDate } = props;
  const date = new Date(startDate);

  if (date.toDateString() === new Date().toDateString()) {
    return <StyledWeekViewTimeTableCell {...props} className={classes.todayCell} />;
  } if (date.getDay() === 0 || date.getDay() === 6) {
    return <StyledWeekViewTimeTableCell {...props} className={classes.weekendCell} />;
  } return <StyledWeekViewTimeTableCell {...props} />;
}

function DayScaleCell(props) {
  const { startDate, today } = props;

  if (today) {
    return <StyledWeekViewDayScaleCell {...props} className={classes.today} />;
  } if (startDate.getDay() === 0 || startDate.getDay() === 6) {
    return <StyledWeekViewDayScaleCell {...props} className={classes.weekend} />;
  } return <StyledWeekViewDayScaleCell {...props} />;
}

function ToolTipContent({
  children, appointmentData, ...restProps
}) {
  return (
    <AppointmentTooltip.Content {...restProps} appointmentData={appointmentData}>
      <span>
        {' '}
        <b>Location:</b>
        {' '}
        {appointmentData.location}
        {' '}
      </span>
      <br />
      <span>
        {' '}
        <b>Conflict:</b>
        {' '}
        {appointmentData.conflict}
        {' '}
      </span>
    </AppointmentTooltip.Content>
  );
}

function AppointmentStyle({
  children, style, ...restProps
}) {
  return (
    <Appointments.Appointment
      {...restProps}
      style={{
        ...style,
        backgroundColor: '#483d8b',
        borderRadius: '6px',
      }}
    >
      {children}
    </Appointments.Appointment>
  );
}

function Schedule(appointments, semester) {
  return (
    <Paper>
      <Scheduler
        data={appointments}
        height={660}
      >
        <ViewState
          defaultCurrentDate={(semester == 'F22') ? '2022-09-05' : '2023-01-09'}
        />
        <WeekView
          startDayHour={8}
          endDayHour={22}
          timeTableCellComponent={TimeTableCell}
          dayScaleCellComponent={DayScaleCell}
        />
        <Toolbar />
        <DateNavigator />
        <TodayButton />
        <Appointments
          appointmentComponent={AppointmentStyle}
        />
        <AppointmentTooltip
          contentComponent={ToolTipContent}
          showCloseButton
        />
      </Scheduler>
    </Paper>
  );
}

export default Schedule;
