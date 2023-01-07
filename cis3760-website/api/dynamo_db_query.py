# disable certain warnings
# pylint: disable-all
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=broad-except
# pylint: disable=too-many-arguments

# mega quick change

import json

# import threading
# from datetime import datetime
# from decimal import Decimal
# from pprint import pprint
import boto3  # pylint: disable=import-error

# from boto3.dynamodb.conditions import Key # pylint: disable=import-error
from botocore.exceptions import ClientError  # pylint: disable=import-error


# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/example_dynamodb_Scenario_PartiQLSingle_section.html
class PartiQLWrapper:  # pylint: disable=too-few-public-methods
    def __init__(self, dyn_resource):
        self.dyn_resource = dyn_resource

    def run_partiql(self, statement, params):
        try:
            output = self.dyn_resource.meta.client.execute_statement(
                Statement=statement, Parameters=params
            )
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                print(
                    "Couldn't execute PartiQL '%s' because the table does not exist.",
                    statement,
                )
            else:
                print(
                    "Couldn't execute PartiQL '%s'. Here's why: %s: %s",
                    statement,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
            raise
        else:
            return output


class DynamoQuery:
    table_n = None

    def __init__(self):
        self.table_n = None

    dyn_client = boto3.client(
        "dynamodb",
        aws_access_key_id="AKIAZBTCUBUO6RIJI6OW",
        aws_secret_access_key="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",
        region_name="us-east-2",
    )

    dyn_res = boto3.resource(
        "dynamodb",
        aws_access_key_id="AKIAZBTCUBUO6RIJI6OW",
        aws_secret_access_key="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",
        region_name="us-east-2",
    )
    ddb_exceptions = dyn_client.exceptions

    allCourses = PartiQLWrapper(dyn_res)

    def get_all_courses(self, wrapper):
        output = wrapper.run_partiql(f'SELECT* FROM "{self.table_n}" WHERE 1=?', [1])
        return output

    def run_get_all_courses(self, semester):
        try:
            if semester == "W23":
                self.table_n = "sprint-8-table-w23"
            elif semester == "F22":
                self.table_n = "sprint-5-table"
            return self.get_all_courses(self.allCourses)
        except Exception as err:
            empty = []
            print(f"Something went wrong with the demo! Here's what: {err}")
            return empty

    def course_search(self, wrapper, table_n, selected_course):
        output = wrapper.run_partiql(
            f'SELECT* FROM "{table_n}" WHERE courseType=?', [selected_course]
        )
        return output

    def run_course_search(self, name, semester):
        try:
            if semester == "W23":
                self.table_n = "sprint-8-table-w23"
            elif semester == "F22":
                self.table_n = "sprint-5-table"
            return self.course_search(self.allCourses, self.table_n, name)
        except Exception as err:
            empty = []
            print(f"Something went wrong with the demo! Here's what: {err}")
            return empty

    def course_code_search(self, wrapper, table_n, selected_course):
        if selected_course != None:
            selected_course = selected_course.replace("*", "")
        course_type = selected_course.rstrip("0123456789")
        course_number = selected_course[len(course_type) :]
        print(f"Getting data for all '{course_type}, {course_number}' sections")
        output = wrapper.run_partiql(
            f'SELECT* FROM "{table_n}" WHERE courseType=? AND courseNumber=?',
            [course_type, course_number],
        )
        return output

    def run_course_code_search(self, name, semester):
        try:
            if semester == "W23":
                self.table_n = "sprint-8-table-w23"
            elif semester == "F22":
                self.table_n = "sprint-5-table"
            return self.course_code_search(self.allCourses, self.table_n, name)
        except Exception as err:
            empty = []
            print(f"Something went wrong with the demo! Here's what: {err}")
            return empty

    def full_course_name_search(self, wrapper, table_n, selected_course):
        selected_course = selected_course.replace("*", "")
        course_type = selected_course.rstrip("0123456789")
        course_number = selected_course[len(course_type) : len(course_type) + 4]
        course_section = selected_course[len(course_type) + len(course_number) :]
        output = wrapper.run_partiql(
            f'SELECT* FROM "{table_n}" WHERE courseType=? AND courseNumber=? AND courseSection=?',
            [course_type, course_number, course_section],
        )
        return output

    def run_full_course_name(self, name, semester):
        try:
            if semester == "W23":
                self.table_n = "sprint-8-table-w23"
            elif semester == "F22":
                self.table_n = "sprint-5-table"
            return self.full_course_name_search(self.allCourses, self.table_n, name)
        except Exception as err:
            empty = []
            print(f"Something went wrong with the demo! Here's what: {err}")
            return empty

    def create_course_array(self, coursesJSON):
        tmp = ScheduleConflict()
        course_dict_array = []
        for course in coursesJSON:
            holder = [course]
            course_dict_array.append(tmp.initialize_schedule(holder))
        return course_dict_array

    def MWF_filter(self, coursesJSON, semester):
        course_array = self.create_course_array(coursesJSON)
        filtered_array = []
        # print("course array is",course_array)
        for course in course_array:
            is_valid = True
            for item in course:
                if item["day"] == "Tue" or item["day"] == "Thu":
                    is_valid = False
                    break
            if is_valid == True and course:
                tmp = course[0]
                name = tmp["title"]
                filtered_array.append(name)
        return (
            self.get_filtered_courses(filtered_array, "sprint-8-table-w23")
            if semester == "W23"
            else self.get_filtered_courses(filtered_array, "sprint-5-table")
        )

    def TT_filter(self, coursesJSON, semester):
        course_array = self.create_course_array(coursesJSON)
        filtered_array = []
        for course in course_array:
            is_valid = True
            for item in course:
                if item["day"] == "Mon" or item["day"] == "Wed" or item["day"] == "Fri":
                    is_valid = False
                    break
            if is_valid == True and course:
                tmp = course[0]
                name = tmp["title"]
                filtered_array.append(name)
        return (
            self.get_filtered_courses(filtered_array, "sprint-8-table-w23")
            if semester == "W23"
            else self.get_filtered_courses(filtered_array, "sprint-5-table")
        )

    def get_filtered_courses(self, courseList, tableName):
        dynamoTableRows = []
        # courseList = ['AGR1110*0104', 'AGR4450*01']
        dyn_res = boto3.resource(
            "dynamodb",
            aws_access_key_id="AKIAZBTCUBUO6RIJI6OW",
            aws_secret_access_key="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",
            region_name="us-east-2",
        )

        wrapper = PartiQLWrapper(dyn_res)

        for i in range(0, len(courseList)):
            try:
                response = wrapper.run_partiql(
                    f'SELECT* FROM "{tableName}" WHERE courseNameSection=?',
                    [courseList[i]],
                )
            except:
                print(
                    "An error occurred while trying to query the table for "
                    + courseList[i]
                )

            if response != None:
                dynamoTableRows.append(response["Items"][0])

        return dynamoTableRows


class ScheduleConflict:
    def conflict_verifier(self, to_be_added, course_list):
        to_be_added_time_map = self.initialize_schedule(to_be_added)
        course_time_map = self.initialize_schedule(course_list)
        conflicting_courses = []
        for tb_course_times in to_be_added_time_map:
            conflict_statements = []
            for times in course_time_map:
                if self.check_days(times, tb_course_times):
                    statement = (
                        "Warning: "
                        + tb_course_times["title"]
                        + " "
                        + tb_course_times["type"]
                        + " "
                        + "conflicts with "
                        + times["title"]
                        + " "
                        + times["type"]
                        + " "
                        + "on "
                        + times["day"]
                    )
                    conflict_statements.append(statement)
                    tb_course_times["conflict"] = conflict_statements
                    conflicting_courses.append(tb_course_times)
        return conflicting_courses

    def check_days(self, list_times, tb_times):
        result = False
        if (
            tb_times["day"] == list_times["day"]
            and tb_times["type"] != "EXA"
            and list_times["type"] != "EXA"
        ):
            if self.time_to_integer(tb_times["startTime"]) <= self.time_to_integer(
                list_times["startTime"]
            ) and self.time_to_integer(tb_times["endTime"]) >= self.time_to_integer(
                list_times["startTime"]
            ):
                result = True
            elif self.time_to_integer(tb_times["startTime"]) <= self.time_to_integer(
                list_times["startTime"]
            ) and self.time_to_integer(tb_times["endTime"]) >= self.time_to_integer(
                list_times["endTime"]
            ):
                result = True
            elif self.time_to_integer(tb_times["startTime"]) >= self.time_to_integer(
                list_times["startTime"]
            ) and self.time_to_integer(tb_times["endTime"]) <= self.time_to_integer(
                list_times["endTime"]
            ):
                result = True
            elif (
                self.time_to_integer(tb_times["startTime"])
                >= self.time_to_integer(list_times["startTime"])
                and self.time_to_integer(tb_times["startTime"])
                < self.time_to_integer(list_times["endTime"])
                and self.time_to_integer(tb_times["endTime"])
                >= self.time_to_integer(list_times["endTime"])
            ):
                result = True
        return result

    def time_to_integer(self, string_time):
        tmp = string_time.split(":")
        integer_time = 0
        integer_time += 100 * int(tmp[0])
        integer_time += int(tmp[1])
        return integer_time

    def initialize_schedule(self, course_list):
        formatted_list = []
        for course in course_list:
            self.do_all_info(course, formatted_list)
        return formatted_list

    def do_all_info(self, course, formatted_list):
        self.parse_schedule("LectureInfo", course, formatted_list, "LEC")
        self.parse_schedule("SeminarInfo", course, formatted_list, "SEM")
        self.parse_schedule("LabInfo", course, formatted_list, "LAB")
        self.parse_schedule("ExamInfo", course, formatted_list, "EXA")

    def parse_schedule(self, info_type, course, formatted_list, course_type):
        tmp_string = course[info_type]
        if course_type in ("LAB", "SEM"):
            check_multiple = tmp_string.split(course_type)
            for string in check_multiple:
                tmp_map = self.initializa_map()
                self.get_days_and_times(string, tmp_map)
                self.parse_week(formatted_list, course, tmp_map, course_type)
        else:
            full_string = course[info_type]
            tmp_map = self.initializa_map()
            self.get_days_and_times(full_string, tmp_map)
            self.parse_week(formatted_list, course, tmp_map, course_type)

    def parse_week(self, formatted_list, course, week, s_type):
        self.parse_days(formatted_list, s_type, course, "mon", week)
        self.parse_days(formatted_list, s_type, course, "tue", week)
        self.parse_days(formatted_list, s_type, course, "wed", week)
        self.parse_days(formatted_list, s_type, course, "thu", week)
        self.parse_days(formatted_list, s_type, course, "fri", week)

    def parse_days(self, formatted_list, s_type, course, day, week):
        tmp_list = {}
        for item in week[day]:
            self.initialize_data(tmp_list, item, day.capitalize(), s_type, course)
            formatted_list.append(tmp_list)

    def initialize_data(self, new_data, item, day, classification, course):
        item_split = item.split(" ")
        new_data["title"] = course["courseNameSection"]
        new_data["startTime"] = self.format_time(item_split[0])
        new_data["endTime"] = self.format_time(item_split[1])
        new_data["type"] = classification
        new_data["conflict"] = "N/A"
        new_data["location"] = course["Location"]
        new_data["day"] = day

    def format_time(self, time):
        frmtd_time = ""
        if "AM" in time:
            frmtd_time = time[0:-2]
        if "PM" in time:
            frmtd_time = time[0:-2]
            tmp = frmtd_time.split(":")
            num = int(tmp[0])
            num = (num % 12) + 12
            frmtd_time = str(num) + ":" + tmp[1]
        return frmtd_time

    def initializa_map(self):
        mon_times = []
        tue_times = []
        wed_times = []
        thu_times = []
        fri_times = []
        tmp_map = {
            "mon": mon_times,
            "tue": tue_times,
            "wed": wed_times,
            "thu": thu_times,
            "fri": fri_times,
        }
        return tmp_map

    def get_days_and_times(self, info, course_map):
        tmp = info.split(" ")
        time = ""
        for item in tmp:
            if ("AM" in item or "PM" in item) and item != "EXAM":
                time = time + item + " "
        if "Mon" in info:
            course_map["mon"].append(time)
        if "Tues" in info:
            course_map["tue"].append(time)
        if "Wed" in info:
            course_map["wed"].append(time)
        if "Thur" in info:
            course_map["thu"].append(time)
        if "Fri" in info:
            course_map["fri"].append(time)


if __name__ == "__main__":
    schedule = json.load(open("tests/schedule.json", "r"))
    conflict = json.load(open("tests/no_conflict.json", "r"))
    query = DynamoQuery()
    tmp = ScheduleConflict()

    print(query.MWF_filter(schedule, "F22"))
