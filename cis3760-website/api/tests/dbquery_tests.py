# disable certain warnings
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=broad-except
# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=import-error
# pylint: disable=wrong-import-position
# pylint: disable=super-init-not-called
# pylint: disable=attribute-defined-outside-init
# unit tests for the query class

# change for testing

import unittest
import re
import json
import sys

sys.path.append("..")  # allows us to access files in parent directory

from dynamo_db_query import DynamoQuery
from dynamo_db_query import ScheduleConflict

# from pprint import pprint


class TestDynamoQuery(unittest.TestCase):
    def setUp(self):
        with open("./gac_exp_result.txt", encoding="utf8") as self.testfilegac:
            self.testdatagac = self.testfilegac.read()

        with open("./ccs_exp_result.txt", encoding="utf8") as self.testfileccs:
            self.testdataccs = self.testfileccs.read()

        with open("./fcns_exp_result.txt", encoding="utf8") as self.testfilefcns:
            self.testdatafcns = self.testfilefcns.read()

        # self.testfilegac = open("./gac_exp_result.txt", encoding="utf8")
        # self.testfileccs = open("./ccs_exp_result.txt", encoding="utf8")
        # self.testfilefcns = open("./fcns_exp_result.txt", encoding="utf8")
        # self.testdatafcns = self.testfilefcns.read()

    def tearDown(self):
        self.testfilegac.close()
        self.testfileccs.close()
        self.testfilefcns.close()

    def test_get_all_courses(self):
        self.query = DynamoQuery()
        test = self.query.run_get_all_courses("F22")
        expected_result = str(self.testdatagac)
        test_result = str(test["Items"])
        re.sub(r"\W+", "", expected_result)
        re.sub(r"\W+", "", test_result)
        self.assertEqual(expected_result, test_result)

    def test_course_code_search(self):
        self.query = DynamoQuery()
        test = self.query.run_course_code_search("COOP*1100", "F22")
        expected_result = str(self.testdataccs)
        test_result = str(test["Items"])
        re.sub(r"\W+", "", expected_result)
        re.sub(r"\W+", "", test_result)
        self.assertEqual(expected_result, test_result)

    def test_course_code_search_empty(self):
        self.query = DynamoQuery()
        test = self.query.run_course_code_search("", "F22")
        test_result = test["Items"]
        expected_result = []
        self.assertEqual(expected_result, test_result)

    def test_course_code_search_rand(self):
        self.query = DynamoQuery()
        test = self.query.run_course_code_search("DAWG***HELLO/,.,;'l1`36520", "F22")
        test_result = test["Items"]
        expected_result = []
        self.assertEqual(expected_result, test_result)

    def test_course_code_search_null(self):
        self.query = DynamoQuery()
        test_result = self.query.run_course_code_search(None, "F22")
        expected_result = []
        self.assertEqual(expected_result, test_result)

    def test_full_course_name_search(self):
        self.query = DynamoQuery()
        test = self.query.run_full_course_name("ANSC3080*0102", "F22")
        test_result = str(test["Items"])
        expected_result = str(self.testdatafcns)
        re.sub(r"\W+", "", expected_result)
        re.sub(r"\W+", "", test_result)
        self.assertEqual(expected_result, test_result)

    def test_full_course_name_search_empty(self):
        self.query = DynamoQuery()
        test = self.query.run_full_course_name("", "F22")
        test_result = test["Items"]
        # print("printing test " + test_result)
        expected_result = []
        self.assertEqual(expected_result, test_result)

    def test_full_course_name_search_rand(self):
        self.query = DynamoQuery()
        test = self.query.run_full_course_name("YAMON-0-529082./,';1`", "F22")
        test_result = test["Items"]
        expected_result = []
        self.assertEqual(expected_result, test_result)

    def test_full_course_name_search_null(self):
        self.query = DynamoQuery()
        test_result = self.query.run_full_course_name(None, "F22")
        expected_result = []
        self.assertEqual(expected_result, test_result)


class TestScheduleConflict(unittest.TestCase):
    def setUp(self):
        with open("./conflict.json", encoding="utf8") as self.testconflict:
            self.testdataconflict = json.load(self.testconflict)

        with open("./no_conflict.json", encoding="utf8") as self.testnoconflict:
            self.testdatanoconflict = json.load(self.testnoconflict)

        with open("./schedule.json", encoding="utf8") as self.testschedule:
            self.testdataschedule = json.load(self.testschedule)

        with open("./cnflct_exp_result.txt", encoding="utf8") as self.cnflctresult:
            self.cnflctresultdata = self.cnflctresult.read()


    def tearDown(self):
        self.testconflict.close()
        self.testnoconflict.close()
        self.testschedule.close()
        self.cnflctresult.close()

    def test_conflict_verifier_conflict(self):
        self.query = ScheduleConflict()
        conflict = self.testdataconflict
        schedule = self.testdataschedule
        expected_result = str(self.cnflctresultdata)
        test_result = str(self.query.conflict_verifier(conflict, schedule))
        re.sub(r"\W+", "", expected_result)
        re.sub(r"\W+", "", test_result)
        self.assertEqual(expected_result, test_result)

    def test_conflict_verifier_no_conflict(self):
        self.query = ScheduleConflict()
        no_conflict = self.testdatanoconflict
        schedule = self.testdataschedule
        expected_result = []
        test_result = self.query.conflict_verifier(no_conflict, schedule)
        self.assertEqual(expected_result, test_result)


# this runs all the tests:
if __name__ == "__main__":
    unittest.main()
