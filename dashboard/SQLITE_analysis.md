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
```
