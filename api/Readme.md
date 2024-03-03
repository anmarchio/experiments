# Experiments API

This is the database API for the experiments performed on the `optimization` project designed 
to run cartesian genetic programming on images.
It uses `sqlalchemy` to establish a communication between python models and a `SQLite` database.
* SQLAlchemy: https://www.geeksforgeeks.org/sqlalchemy-core-creating-table/
* Python SQLAlchemy with SQLite: https://realpython.com/python-sqlite-sqlalchemy/#working-with-sqlalchemy-and-python-objects

All results created by `optimization` are ususally stores in a `results` directory, organized by a date string. 
This project allows to import all results data encoded as `json`, `xml` and `txt` 
to a database model stored in `SQLite SQL` abstractions. 

## Quick Setup

* Install a working python instance using `python 3.8+`
* Create a virtual environment: `python -m venv venv`  
* Then install requirements: `python -m pip install -r requirements.txt`

## Running the project

* Activate venv: `<YOUR_PROJECT_PATH>\venv\Scripts\activate.bat`
* Run project: `python <YOUR_PROJECT_PATH>\api\main.py`  
* Running the tests: `python -m unittest discover -s "<YOUR_PROJECT_PATH>/api/test" -v`

## Import Data from Json

```
chcp 1252
SET PATH1="P:\99 Austausch_TVöD\mara\Dissertation\20220111results"
REM experiments\venv\Scripts\activate.bat
REM cd experiments\api\
python experiments\api\main.py --importmany %PATH1%

SET PATH2="P:\99 Austausch_TVöD\mara\Dissertation\20230118results_adminc"
python experiments\api\main.py --importmany %PATH2%

SET PATH3="P:\99 Austausch_TVöD\mara\Dissertation\20230120results_dl2"
python experiments\api\main.py --importmany %PATH3%

ROBOCOPY "." "P:\99 Austausch_TVöD\mara\Dissertation" "experiments.db" /MIR /LOG+:log.txt
```