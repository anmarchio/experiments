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

* From command line, run the following command to import a single dataset
```bash
venv\Scripts\python.exe -m api.main --importmany "D:\MY_PATH_TO\experiments\scripts\results\MY_DATASET"
```

* Using a batch file to import multiple datasets
```bash
chcp 1252
SET PATH1="Z:\mara\Dissertation\20220111results"
REM experiments\venv\Scripts\activate.bat
REM cd experiments\api\
python experiments\api\main.py --importmany %PATH1%

SET PATH2="Z:\mara\Dissertation\20230118results_adminc"
python experiments\api\main.py --importmany %PATH2%

SET PATH3="Z:\mara\Dissertation\20230120results_dl2"
python experiments\api\main.py --importmany %PATH3%

ROBOCOPY "." "Z:\mara\Dissertation" "experiments.db" /MIR /LOG+:log.txt
```
## SQL Query for Data Analysis

* Return all Best MCC values per dataset:
```sql
SELECT 
    d.name            AS dataset_name,
    d.source_directory,
    r.run_id,
    r.number          AS run_number,
    MAX(bif.best_individual_fitness) AS best_individual_fitness
FROM dataset AS d
JOIN experiment AS e        ON e.dataset_id = d.dataset_id
JOIN run        AS r        ON r.experiment_id = e.experiment_id
JOIN analyzer   AS a        ON a.run_id = r.run_id
JOIN best_individual_fit AS bif ON bif.analyzer_id = a.analyzer_id
GROUP BY d.name, d.source_directory, r.run_id, r.number
ORDER BY d.name, r.run_id;
```

* Return mean MCC per dataset:
```sql
SELECT 
    d.name AS dataset_name,
    d.source_directory,
    AVG(bif.best_individual_fitness) AS avg_best_individual_fitness
FROM dataset AS d
JOIN experiment AS e ON e.dataset_id = d.dataset_id
JOIN run        AS r ON r.experiment_id = e.experiment_id
JOIN analyzer   AS a ON a.run_id = r.run_id
JOIN best_individual_fit AS bif ON bif.analyzer_id = a.analyzer_id
GROUP BY d.dataset_id, d.name, d.source_directory
ORDER BY avg_best_individual_fitness DESC;

```