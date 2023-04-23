# Experiments

This repository contains all scripts that were designed to analyze data from image processing using the cartesian genetic programming implementation in https://gitlab.cc-asp.fraunhofer.de/opm/evias/optimization.

### Repository Overview
* identify_rovings_aircarbon: `datapreparation\python\identify_roving.py`
* json_to_binary: `datapreparation\python\json_to_binary.py`
* import_many: `api\main.py`
* crop_to_tiles: `datapreparation\python\crop_to_tiles.py`
* crop_to_tile Blende5: `datapreparation\python\crop_to_tiles.py C:\Users\mara_c10\Desktop\2022_CGP_Experimente\Owncloud_AirCarbon3\Annotation\AirCarbon2\160919_SGL\Blende5_6_1800mA C:\Users\mara_c10\Desktop\2022_CGP_Experimente\Owncloud_AirCarbon3\Annotation\AirCarbon2\160919_SGL\Blende5_6_1800mA_rov 140`
* Dashboard: `dashboard\dashboard.py`


### Research Questions

#### Image Entropy Analysis

* Entropie der Bilder (einfach vs komplex)
* Entropie der Daten allgemein
* Auswahl der Operatoren: wie misst man die algorithmische Komplexität?
* Welche Fälle sind besser geeignet?
* kann man im Voraus - ohne Daten- abschätzen, ob CGP geeignet ist?


#### Fragen an die Anwender:


- Dimensionsreduktion: welche Algorithmen kommen in Frage?
- Umfang der Fragen: was sind ihre wichtigsten Kriterien?
- nachträgliche Anlagendigitalisierung: Relevanz und Vorgehen?
- Data driven und intransparent vs. lesbarer code (als Graph)
- wie hoch ist der Annotationsaufwand? Wie stabil funktionieren Systeme?
- Auflösung und Menge der Daten? Größenordnung?
- Aufwände von Systemauslegung: Umfang? Wo sind größte Hürden?

# Experiment Overview

Experiments on image datasets using optimization

| Experiment | Dataset | Problem | Hypothesis | Goal |
| ---------- | ------- | ------- | ---------- | ---- |
| CGP with Edge Mutation | Carbon Fibres | Object Detection: fitness on bounding boxes | worst results compared to CGP-SSR, CGP with fixed edges, U-Net | based on settings used for ICMLA 2017 |
| CGP with fixed Edges | Carbon Fibres | Object Detection: fitness on bounding boxes | fitness **significantly** superior to CGP with Edge Mutation; inferior to CGP-SSR, to U-Net | based on settings from ICMLA 2017 |
| CGP with Edge Mutation | Carbon Fibres | Semantic Segmentation with free evolution | **significantly** inferior results compared to CGP-SSR, CGP with parameter tuning, U-Net | Reproduce results from traditional approach (e. g. ICMLA 2017), set a reference |
| CGP with fixed Edges | Carbon Fibres | Semantic Segmentation using only parameter mutation | fitness **significantly** superior to CGP Classic; inferior to CGP-SSR, to U-Net | Reproduce results from traditional approach (e. g. ICMLA 2017), set a reference |
| CGP-SSR | Carbon Fibres | Semantic Segmentation with Search Space Reduction (i. e. the differentiation between image filter types) | superior to free evolution without restrictions; equal to evolution with only parameter adjustments; inferior to U-Net and Identify statistically signficance (performance/fitness) for the benefit of search space reduction | show that limitations to the grid improve evolutionary development and overall results; Show superor to results by Harding et al. |
| CGP Classic | Knitted CF | - | - | - |
| CGP with Parameter Optimisation | Knitted CF | - | - | - |
| CGP-SSR | Knitted CF | - | - | - |
| CGP Classic | CGP Classic | - | - | - |
| CGP with Parameter Optimisation | Pultrusion Resin | - | - | - |
| CGP-SSR | Pultrusion Resin | - | - | - |
| CGP Classic | Severstal Steel | - | - | - |
| CGP with Parameter Optimisation | Severstal Steel | - | - | - |
| CGP-SSR | Severstal Steel | - | - | - |
| CGP-SSR | Kaggle Ships, Asphalt Core, Non-Woven Fabrics | - | - | - |
| CGP-SSR | MVTec Anomaly Detection | - | - | - |
| Random Search | Carbon Fibres | Semantic Segmentation | Fitness results around 0.0 | Establish a low level, default reference to all other experiments |

## Hyperparameter Studies

- [ ] Effect of no. generations & runs
- [ ] Influence of number of columns / rows on fitness evolution
- [ ] Is levels back relevant?
- [ ] Study on dependency tree design: smaller trees vs. complex large trees

## Comments

- [ ] Label MVTec Anomaly Test Data
- [ ] Adapt C# bat scripting to run experiments automatically

## Define Experiment

Experiment details are defined in `def run(_config):` in file `experiments.py`:

```
@ex.main
def run(_config):
    """Register signal handler."""
    signal.signal(signal.SIGINT, signal_handler)

    # Implement machine learning things here.
```

## Modifying Script and Config Files

We need to set a path to the compiled executable for CGP optimization and the related arguments.
Therefore modify the method in `experiment.py` according to your local environment and needs.
An example is given below:

Modify the config file `config\base.yml` to include all relevant parameters, e. g.:

```
model_executable_path = os.path.join(
    "C:\\",
    "dev",
    "optimization",
    "Optimization.Commandline",
    "bin",
    "Debug",
    "Optimization.Commandline.exe"
)

train_data_parent_dir = r"Q:\5 Fachbereiche\03 OPM\ReferenzSet\EXIST\out"
val_data_parent_dir = r"Q:\5 Fachbereiche\03 OPM\ReferenzSet\EXIST\out_lbl"

arguments = "Optimization.Commandline.exe " \
            "batch --backend=halcon " \
            "--runs=5 " \
            "--train-data-dir=" \
            + train_data_parent_dir + \
            "--val-data-dir= " \
            + val_data_parent_dir + \
            "--generations=200"
```

Change the following method in `experiment.py` to run your experiment as needed:
```
@ex.main
def run(_config):
```

## Omniboard frontend for Experiment Tracking and Data Vizualization

The project `sacred` lists several frontend projects for data visualization ((https://github.com/IDSIA/sacred#frontends).
We suggest to use `omniboard` () according to its tutorial:

1. Install `Node.js > v12`
1. Install omniboard: `npm install -g omniboard`
1. To run omniboard type: `npx omniboard localhost:27017:sacred`
1. Open `localhost:9000`
