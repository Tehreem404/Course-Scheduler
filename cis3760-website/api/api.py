# disable certain warnings
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=broad-except
# pylint: disable=too-many-arguments


import json
from flask import Flask
from flask import request
from dynamo_db_query import DynamoQuery, ScheduleConflict


app = Flask(__name__)

# @app.route("/api/first")
# def get_first_endpoint():
# return  {'api_data': var}

# @app.route("/api/second")
# def change_end_point_sring():
# return {'api_data': "this is now different"}


@app.route("/api/byname/<name>/<semester>")
def filter_by_name(name, semester):
    query = DynamoQuery()
    counter = name.count("*")
    if counter == 0:
        courses = query.run_course_search(name, semester)
    elif counter == 1:
        courses = query.run_course_code_search(name, semester)
    elif counter == 2:
        courses = query.run_full_course_name(name, semester)

    print(courses)
    return courses


@app.route("/api/getAllCourses/<semester>")
def get_all(semester):
    query = DynamoQuery()
    courses = query.run_get_all_courses(semester)
    return courses


# @app.route("/api/byfullname/<name>")
# def filter_by_fullname(name):
#     query = DynamoQuery()
#     courses = query.run_full_course_name(name)
#     return courses


@app.route("/api/checkconflict/<courselist>/<semester>")
def check_conflicts(courselist, semester):
    query = DynamoQuery()
    courses_json = json.loads(courselist)
    courses = []

    for cee in courses_json["courses"]:
        dee = query.run_full_course_name(cee, semester)
        print(dee)
        if dee and len(dee["Items"]) > 0:
            courses.append(dee["Items"][0])

    print(courses)

    scheduler = ScheduleConflict()
    confliciting_courses = scheduler.initialize_schedule(courses)

    return {"api_data": confliciting_courses}


@app.route("/api/isConflict/<to_be_added>/<courselist>/<semester>")
def is_conflict(to_be_added, courselist, semester):
    # print(to_be_added)
    # print(courselist)
    list_c = courselist.split(",")
    query = DynamoQuery()

    new_course = []
    old_courses = []

    new = query.run_full_course_name(to_be_added, semester)
    # print("run full course name query returned ", new)
    if new and len(new["Items"]) > 0:
        new_course.append(new["Items"][0])

    if to_be_added == courselist:
        old_courses = new_course
    else:
        for cee in list_c:
            # print("c in courselist is ", cee)
            dee = query.run_full_course_name(cee, semester)
            # print("run full course name query returned ", dee)
            # print("the d items is: ", d)
            if dee and len(dee["Items"]) > 0:
                old_courses.append(dee["Items"][0])

    scheduler = ScheduleConflict()
    print("new course", new_course)
    print("old courses", old_courses)
    confliciting_courses = scheduler.conflict_verifier(new_course, old_courses)

    return {"api_data": confliciting_courses}


@app.route("/api/getFilteredCourses/<semester>/<day>", methods=["POST"])
def get_courses_from_semester(semester, day):
    query = DynamoQuery()
    print(semester, day)
    courses_json = json.loads(request.data)
    # courses_json = json.dumps(courses_dict)
    jsoncourses = []

    # print(json.dumps(courses_json))
    for cee in courses_json:
        course = cee["courseNameSection"]
        # print(course)
        dee = query.run_full_course_name(course, semester)
        print(dee)
        if dee and len(dee["Items"]) > 0:
            jsoncourses.append(dee["Items"][0])

    print(jsoncourses[0])

    if day == "Tues":
        return_values = query.TT_filter(jsoncourses, semester)
    elif day == "Mon":
        return_values = query.MWF_filter(jsoncourses, semester)

    print("return values are ", return_values)

    return {"api_data": return_values}
    # return return_values[0]


if __name__ == "__main__":
    app.run(host="0.0.0.0")
