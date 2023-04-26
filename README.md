# Experiments

This repository contains all scripts that were designed to analyze data from image processing using the cartesian genetic programming implementation in https://gitlab.cc-asp.fraunhofer.de/opm/evias/optimization.

## Repository Overview
* identify_rovings_aircarbon: `datapreparation\python\identify_roving.py`
* json_to_binary: `datapreparation\python\json_to_binary.py`
* import_many: `api\main.py`
* crop_to_tiles: `datapreparation\python\crop_to_tiles.py`
* crop_to_tile Blende5: `datapreparation\python\crop_to_tiles.py C:\Users\mara_c10\Desktop\2022_CGP_Experimente\Owncloud_AirCarbon3\Annotation\AirCarbon2\160919_SGL\Blende5_6_1800mA C:\Users\mara_c10\Desktop\2022_CGP_Experimente\Owncloud_AirCarbon3\Annotation\AirCarbon2\160919_SGL\Blende5_6_1800mA_rov 140`
* Dashboard: `dashboard\dashboard.py`

## Setup and Usage

### Quick Start
tbd

### Run Scripts
tbd

## Research Questions

### Evaluation of context and data for the use of CGP

* Computing (information) entropy of images (easy vs. difficult segmentation)
* Determine the `general complexity` of a segmentation / data analysis task
* Selection of operators based on complexity / difficulty of a task
* Which scenarios can be best solved with CGP or a different model?
* Prediction of CGP on a given task / or a (small) dataset

### Open Questions for Data-driven Applications

- Reduction of dimension & search space: 
  * Howto? 
  * Recommended algorithms
- What are your preferred / most important criteria?
- Ex-post digitalization of systems: 
  * How relevant is it?
  * Goto approach
- Interpretability:
  * Relevance of data driven applications
  * Intransparent (complex) vs. readable models (graph-based)
- Data Preperation Effort:
  * Annotation effort of a task / model
  * Accuracy and reproducability of systems
- Effects of Data Quality:
  * resolution
  * amount (Magnitudes?) of available data (or necessary data)
  * problem size (i.e. no. of categories/features, criticality, real-time)  
- Complexity of (algorithm-based) system design:
  * Size and complexity of the task
  * What are the challenges?

## Hyperparameter Studies
### CGP configuration

- ES(1 + 4) recommended as the most efficient configuration, therefore will not be changed
- input and output is usually 1 image
- levels back `l` usually 1, but not as much applicable due to the dependency graph
- termination reached at 150 generations

| Parameter         | Value           |
|-------------------|-----------------|
| ES(`\mu + \lambda`)| ES(1 + 4)      |
| Mutation rate     | ?               |
| Termination       | 150 generations |
| `n_{c}`           | ?               |
| `n_{i}`           | 1               |
| `n_{o}`           | 1               |
| `l`               | 1               |
| `n_{f}`           | ?               |

### Effects of Number of Generations and Repetitions
- [ ] Impact of number of columns / rows on fitness evolution
- [ ] Is levels back relevant?
- [ ] Study on dependency tree design: smaller trees vs. complex large trees

#### Conclusions from Experimental Runs

- convergence reached mostly between 50 and 130 generations
- unlikely that improvement occurs for longer runs
- for more complex datasets, evolution tends to converge early 

![cable_missing_train](scripts/report/84.png "Dataset 84, cable_missing_train")

![hazelnut_crack_train](scripts/report/85.png "Dataset 85, hazelnut_crack_train")

![carpet_traing](scripts/report/95.png "Dataset 95, carpet_traing")

## Complexity Analysis

Metrics selected for complexity analysis:
* Entropy
* Blurriness
* Brightness
* Img Size
* lbl Size
* label_count_per_image
* relative_label_size
* hist_entropy
* jpeg_complexity
* fractal_dimension
* texture_features
* edge_density
* laplacian_variance
* num_superpixels

![entropy_per_dataset](out/plots/20230425-210730Entropy_bplot.png "Entropy per Dataset")
![scatterplot_entropy_fitness](out/plots/20230425-210731Entropy_scatterplot.png "Scatterplot Entropy To Fitness")

Detailed numbers of entropy and fitness analysis:

| Dataset    | Avg. Fit. | Entropy | # Images |
| ---------- | --------- | ------- | ---------- |
| AirCarbon2_t_8.jpg | 0.028007573720837224 | 0.0 |
| None | 0.11639334005129832 | 0.0 |
| FabricDefectsAITEX | 0.12925214267501545 | 0.18115724487902538 |
| KolektorSDD | 0.06565332278979708 | 0.2607629765599094 |
| MAIPreform2_Spule0-0315_Upside | 0.3162098588409003 | 0.07732000907737828 |
| MAIPreform2_Spule1_0117_Upside | 0.05651153345646755 | 0.09592946341948642 |
| MVTec_AD_Bottle_Broken_Lg | 0.26225513731343236 | 0.27172080559406375 |
| MVTec_AD_Bottle_Broken_Sm | 0.28464968029224386 | 0.2267863767074405 |
| MVTec_AD_Cable_Missing | 0.7171056969044834 | 0.38411058037076246 |
| MVTec_AD_Capsule | 0.15132567662349938 | 0.23202616829406658 |
| MVTec_AD_Carpet | 0.21769846447384691 | 0.24669284386009335 |
| MVTec_AD_Grid_Thread | 0.31599391828086065 | 0.3041597566404906 |
| MVTec_AD_Hazelnut_Crack | 0.24522991041826714 | 0.2984493662841539 |
| MVTec_D_Leather | 0.3542320590261696 | 0.27032127158300534 |
| MVTec_AD_Metal_Nut | 0.11186050396653803 | 0.20937995460265713 |
| MVTec_AD_Pill_Crack | 0.14955956290744649 | 0.2081181417641098 |
| MVTec_AD_Screw_Scratch | 0.1228070613385369 | 0.2086407295600606 |
| MVTec_AD_Tile_Crack | 0.3972601328978305 | 0.2956153390179142 |
| MVTec_AD_Transistor_Case | 0.05139396346164535 | 0.36294296745567173 |
| MVTec_AD_Wood_Scratch | 0.375791355016471 | 0.246296433390055 |
| MVTec_AD_Zipper_Rough | 0.28612142322204837 | 0.27566764596340676 |
| MT_Blowhole_train | 0.2929250686247117 | 0.07685783331968511 |
| Pultrusion_Resin | 0.49831744566300235 | 0.1375543476918154 |
| Pultrusion_Resin_Augmtd | 0.2771436150817633 | 0.1375628748526754 |
| Pultrusion_Window | 0.4796498058298121 | 0.14266296066088133 |
| severstal-steel | 0.17722965975016708 | 0.0 |
| MAIPreform2_Spule2-0816_Upside | 0.2561302994819138 | 0.10558612754780487 |
| AirCarbon3_80.jpg_dark_1 | 0.07822264997999262 | 0.2375699870681196 |
| AirCarbon3_80.jpg_dark_2 | 0.1519621493143124 | 0.2690541107118067 |
| AirCarbon3_80.jpg_dark_3 | 0.1650572882182899 | 0.2555525203569724 |
| MAIPreform2_Spule0-0315_Upside Thread | 0.17135897128539657 | 0.1486841085239903 |
| MAIPreform2_Spule0-0315_Upside Thread 256 | 0.20414281389085984 | 0.1516273617808818 |

Correlation between different metrics and achieved fitness:

| Metric | Cor(fit, v) |
| ------ | ----------- |
| Entropy | **0.3333065705521979**|
| Blurriness | 0.25439760238103315|
| Brightness | 0.3014321222979049|
| Img Size | 0.26911331967136043|
| Lbl Size | **0.4410566759758734**|
| label_count_per_image | 0.329338014352925|
| relative_label_size | 0.2057934599847992|
| hist_entropy | 0.20465583325336342|
| jpeg_complexity | 0.13138968956377578|
| fractal_dimension | **-0.025641841230255702**|
| texture_features | 0.05000227367080492|
| edge_density | 0.19970673740901201|
| laplacian_variance | 0.161659397897984|
| num_superpixels | 0.088234929261432|

## (DRAFT) Experiment Plan

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


## MLOps Configuration

### Define Experiment

Experiment details are defined in `def run(_config):` in file `experiments.py`:

```
@ex.main
def run(_config):
    """Register signal handler."""
    signal.signal(signal.SIGINT, signal_handler)

    # Implement machine learning things here.
```

### Modifying Script and Config Files

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

### Omniboard frontend for Experiment Tracking and Data Vizualization

The project `sacred` lists several frontend projects for data visualization ((https://github.com/IDSIA/sacred#frontends).
We suggest to use `omniboard` () according to its tutorial:

1. Install `Node.js > v12`
1. Install omniboard: `npm install -g omniboard`
1. To run omniboard type: `npx omniboard localhost:27017:sacred`
1. Open `localhost:9000`
