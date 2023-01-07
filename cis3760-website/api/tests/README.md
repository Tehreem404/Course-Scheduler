# 'test' Folder

Folder for project test code.

## dbquery_tests.py

### How to Run

#### Entire File

```$ python dbquery_tests.py [-v]```
or
```$ python3 dbquery_tests.py [-v]```

- where ```-v``` runs unit test's verbose version (optional)

#### Individual Unit Test Class

```python -m unittest dbquery_tests.class_name```
or
```python3 -m unittest dbquery_tests.class_name```

- where 'class_name' should be replaced with the name of the class that contains the unit tests you want to run

#### Individual Unit Test

```python -m unittest dbquery_tests.class_name.method_name```
or
```python3 -m unittest dbquery_tests.class_name.method_name```

- where 'class_name' should be replaced with the name of the class that contains the unit test you want to run
- where 'method_name' should be replaced with the method name of the unit test you want to run

### Notes
- Ensure this file is ran from within the 'test' folder (there will be import issues if it isn't)
- Other unit test command line flags not mentioned in this README can be found here: https://docs.python.org/3/library/unittest.html