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
SELECT * FROM dataset WHERE name="unknown"
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

### Look into a pipeline

* Get Best Fit for experiment ID:
```
SELECT * FROM run where experiment_id=52;
```

* Get Best Individual Fitness for given runs
```
SELECT * FROM analyzer LEFT JOIN best_individual_fitness where run_id > 125 AND run_id < 131;
```

* Best Fitness per Analyzer:
```
SELECT * FROM analyzer LEFT JOIN best_individual_fit ON analyzer.analyzer_id=best_individual_fit.analyzer_id WHERE run_id > 125 AND run_id < 131 ORDER BY best_individual_fitness DESC;
```

* Get Pipeline for best individual by generation number
```
SELECT * FROM individual WHERE analyzer_id=128 ORDER BY fitness DESC;
SELECT * FROM pipeline WHERE pipeline_id=128;
```

* Get dataset from Pipeline
SELECT * FROM run WHERE run_id=154
SELECT * FROM experiment WHERE experiment_id=61;
SELECT * FROM dataset WHERE dataset_id=61;


digraph Pipeline { 
rankdir = "RL";36 [label="Union1\n"];
20 [label="Threshold\nMin=35\n Max=220"];
6 [label="MedianWeighted\nMaskType=gauss\n MaskSize=3"];
_1 [label="HalconInputNode\nProgramInputIdentifier=-1"];
36 -> 20 [];
20 -> 6 [];
6 -> _1 [];
}

dataset_id=67 => D:\evias_expmts\MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone\training

experiment_id=67
run_id=174
grid_id=174
pipeline_id=174

digraph Pipeline { 
rankdir = "RL";76 [label="Connection\nNeighborhood=4"];
60 [label="Closing\nA=4\n B=15\n C=0,392699\n StructElementType=Rectangle"];
36 [label="SelectShape\nMin=45\n Max=99999\n Features=dist_mean"];
22 [label="BinaryThreshold\nMethod=smooth_histo\n LightDark=dark"];
3 [label="MedianImage\nMaskType=circle\n Radius=54\n Margin=Ninety"];
_1 [label="HalconInputNode\nProgramInputIdentifier=-1"];
76 -> 60 [];
60 -> 36 [];
36 -> 22 [];
22 -> 3 [];
3 -> _1 [];
}

dataset_id=82 => C:\Users\Public\evias_expmts\\MVTecAnomalyDetection\cable_missing_train
experiment_id=82
run_id=227
grid_id=227
best_individual_fitness: 0.948242487360214
