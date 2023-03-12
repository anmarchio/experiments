# Experiment Data Analysis

We recommend to use the DB Browser for SQLITE: https://sqlitebrowser.org/

## SQL Queries

* Get datasets for a specific name

```
SELECT dataset.dataset_id, dataset.source_directory FROM dataset WHERE dataset.source_directory="/mnt/sdc1/MVTecAnomalyDetection/bottle_broken_large_train"
```

Sample output:
```
95	/mnt/sdc1/MVTecAnomalyDetection/bottle_broken_large_train
96	/mnt/sdc1/MVTecAnomalyDetection/bottle_broken_large_train
97	/mnt/sdc1/MVTecAnomalyDetection/bottle_broken_large_train
114	/mnt/sdc1/MVTecAnomalyDetection/bottle_broken_large_train
```

* Get dataset and experiment details for specific ds name
```
SELECT dataset.dataset_id, dataset.source_directory, experiment.experiment_id, experiment.created_at FROM dataset, experiment WHERE dataset.source_directory="/mnt/sdc1/MVTecAnomalyDetection/bottle_broken_large_train" AND experiment.dataset_id=dataset.dataset_id
```

Sample output:
```
114	/mnt/sdc1/MVTecAnomalyDetection/bottle_broken_large_train	91	2023-02-19 15:48:22.525509
```
* Get all datasets and associated experiments

```
SELECT dataset.dataset_id, dataset.source_directory, experiment.experiment_id, experiment.created_at FROM dataset LEFT JOIN experiment ON experiment.dataset_id=dataset.dataset_id
```

* Show datasets for which no experiment exists (NULL)
```
SELECT dataset.dataset_id, dataset.source_directory, experiment.experiment_id, experiment.created_at FROM dataset LEFT JOIN experiment ON experiment.dataset_id=dataset.dataset_id WHERE experiment_id IS NULL
SELECT experiment.dataset_id, dataset.source_directory, experiment.experiment_id, experiment.created_at FROM experiment LEFT JOIN run ON experiment.dataset_id=dataset.dataset_id WHERE experiment_id IS NULL
SELECT run.run_id, run.started_at, experiment.experiment_id, experiment.created_at FROM run LEFT JOIN experiment ON run.experiment_id=experiment.experiment_id WHERE experiment.experiment_id<45
```

* Count datasets by name or source directory

```
SELECT count(name), * FROM dataset GROUP BY name
SELECT count(source_directory), * FROM dataset GROUP BY source_directory
```

* analyzer runs

```
SELECT * FROM run ORDER BY run.analyzer_id
```
or
```
SELECT * FROM best_individual_fit ORDER BY analyzer_id
```

*Exception ID:*
```
SELECT * FROM exception ORDER BY experiment_id
SELECT * FROM exception WHERE experiment_id IS NULL
```