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

1. Set up a python environment using `python -m venv <PATH>\venv`, then activate environment by `venv\Scripts\activate.bat`
1. Install requirements: `python -m pip install -r requirements.txt`
1. Execute `main.py` by `python main.py`

### Run Scripts

The repository contains the following function to process experimental data:

#### API

* `experiments\api` contains a database wrapper for SQLite written with `SQLAlquemy`
* it can be used to **import** data from `CGP optimization` and analyze them as follows
  * `python api\main.py --importmany "<PATH>\test_api\many_results_dir"`
  * `python api\main.py --importone "<PATH>\test_api\one_result_dir"`
* database is stored (or created if it doesn not exist) in: `<PATH>\api\experiments.db`
* For more details on how to use the database api, see: [api/Readme.md](api/Readme.md)

#### Dashboard

* **TBD**

#### Plotting Data

* **TBD**

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

In general, the following formula allows to compute the entropy or information density of an image:

`$- \sum_{i=0}^{n=1} p_{i} log_{b} p_{i}$`

`where n is the number of gray levels (256 for 8-bit images), p_{i} is the probability of a pixel having gray level i, and b is the base of the logarithm function.`

Also see: https://stackoverflow.com/questions/50313114/what-is-the-entropy-of-an-image-and-how-is-it-calculated

Metrics selected for complexity analysis:
* Entropy: as defined by the shannon entropy
* Blurriness
* Brightness
* Img Size: size of the image in pixels `W x H`
* lbl Size: size of the label's contained pixels
* label_count_per_image: no. of labels per image
* relative_label_size: size of label in px compared to image
* hist_entropy: ?
* jpeg_complexity
* fractal_dimension
* texture_features
* edge_density
* laplacian_variance
* num_superpixels

![entropy_per_dataset](out/plots/20230425-210730Entropy_bplot.png "Entropy per Dataset")
![scatterplot_entropy_fitness](out/plots/20230425-210731Entropy_scatterplot.png "Scatterplot Entropy To Fitness")

Detailed numbers of entropy and fitness analysis for 32 datasets in the following table.
* 15 material surface types
* from 6 institutions
* Most promising Metric: hist_entropy

| Index | Material | Publisher |Dataset    | Avg. Fit. | Entropy | # Images |
| ---------| ---------| --------- | ---------- | --------- | ------- | ---------- |
| 1 | Textile (CF) | Fraunhofer | AirCarbon2_t_8.jpg | 0.028007573720837224 | 0.0 | 24 |
| 2 | Textile (CF) | Fraunhofer | None | 0.11639334005129832 | 0.0 | 120 |
| 3 | Textile | AITEX | FabricDefectsAITEX | 0.12925214267501545 | 0.08898475129502198 | 20 |
| 4 | Electrical Isolators | Kolektor | KolektorSDD | 0.06565332278979708 | 0.1854995622470775 | 8 |
| 5 | Textile (CF) | Fraunhofer | MAIPreform2_Spule0-0315_Upside | 0.3162098588409003 | 0.07637775804258891 | 0 |
| 6 | Textile (CF) | Fraunhofer | MAIPreform2_Spule1_0117_Upside | 0.05651153345646755 | 0.07540744696603166 | 0 |
| 7 | Bottle | MVTec | MVTec_AD_Bottle_Broken_Lg | 0.26225513731343236 | 0.24739057555342808 | 10 |
| 8 | Bottle | MVTec | MVTec_AD_Bottle_Broken_Sm | 0.28464968029224386 | 0.20974516945485644 | 11 |
| 9 | Cable | MVTec | MVTec_AD_Cable_Missing | 0.7171056969044834 | 0.006219981210434028 | 6 |
| 10 | Plastic | MVTec | MVTec_AD_Capsule | 0.15132567662349938 | 0.23862904045319938 | 10 |
| 11 | Textile | MVTec | MVTec_AD_Carpet | 0.21769846447384691 | 0.24625022158438528 | 10 |
| 12 | Textile | MVTec | MVTec_AD_Grid_Thread | 0.31599391828086065 | 0.18638536582071882 | 5 |
| 13 | Food | MVTec | MVTec_AD_Hazelnut_Crack | 0.24522991041826714 | 0.28874295314587556 | 9 |
| 14 | Leather | MVTec | MVTec_D_Leather | 0.3542320590261696 | 0.22254874510981257 | 10 |
| 15 | Metal | MVTec | MVTec_AD_Metal_Nut | 0.11186050396653803 | 0.21342241164492512 | 11 |
| 16 | Plastic | MVTec | MVTec_AD_Pill_Crack | 0.14955956290744649 | 0.212558998235946 | 13 |
| 17 | Metal | MVTec | MVTec_AD_Screw_Scratch | 0.1228070613385369 | 0.194833379388579 | 12 |
| 18 | Tile | MVTec | MVTec_AD_Tile_Crack | 0.3972601328978305 | 0.27402751836689565 | 8 |
| 19 | Electronics | MVTec | MVTec_AD_Transistor_Case | 0.05139396346164535 | 0.004769530039571607 | 5 |
| 20 | Wood | MVTec | MVTec_AD_Wood_Scratch | 0.375791355016471 | 0.2981424586359251 | 9 |
| 21 | Clothing | MVTec | MVTec_AD_Zipper_Rough | 0.28612142322204837 | 0.24371921336595997 | 8 |
| 22 | Magnetic Tile | Chinese Academy of Sciences, Beijing | MT_Blowhole_train | 0.2929250686247117 | 0.08759798879800851 | 57 |
| 23 | Fluid resin | Fraunhofer | Pultrusion_Resin | 0.49831744566300235 | 0.23080805473192298 | 20 |
| 24 | Fluid resin | Fraunhofer | Pultrusion_Resin_Augmtd | 0.2771436150817633 | 0.23112276440949117 | 20 |
| 25 | Fluid resin | Fraunhofer | Pultrusion_Window | 0.4796498058298121 | 0.22871400226162347 | 20 |
| 26 | Metal | Severstal | severstal-steel | 0.17722965975016708 | 0.0 | 15 |
| 27 | Textile (CF) | Fraunhofer | MAIPreform2_Spule2-0816_Upside | 0.2561302994819138 | 0.08064016914079145 | 0 |
| 28 | Textile (CF) | Fraunhofer | AirCarbon3_80.jpg_dark_1 | 0.07822264997999262 | 0.0526113017372107 | 16 |
| 29 | Textile (CF) | Fraunhofer | AirCarbon3_80.jpg_dark_2 | 0.1519621493143124 | 0.17829923905605988 | 16 |
| 30 | Textile (CF) | Fraunhofer | AirCarbon3_80.jpg_dark_3 | 0.1650572882182899 | 0.16056480354069902 | 16 |
| 31 | Textile (CF) | Fraunhofer | MAIPreform2_Spule0-0315_Upside Thread | 0.17135897128539657 | 0.14445421392625396 | 30 |
| 32 | Textile (CF) | Fraunhofer | MAIPreform2_Spule0-0315_Upside Thread 256 | 0.20414281389085984 | 0.13529143814053632 | 29 |

Correlation between different complexity metrics **of the full image frame** and achieved fitness:

| Metric | Cor(fit, v) |
| ------ | ----------- |
| entropy_arr | 0.2412421767996174|
| blurriness_arr | 0.2762887926996353|
| brightness_arr | 0.2708873690090166|
| image_size | 0.2568331938079588|
| hist_entropy | **0.43440727765649656**|
| jpeg_complexity | **0.3812743862992159** |
| fractal_dimension | 0.22649332946167774|
| texture_features | 0.28321464597815343|
| edge_density | 0.1244109910153665|
| laplacian_variance | 0.05243821001731175|
| num_superpixels | 0.09958786261625971|

Estimation for the whole image:

* `max r_{fit, hist_entropy} = 0.0.434` actual "best" choice, histogram_entropy of the image;
* `max r_{fit, jpeg_complexity} = 0.333` shows a positive correlation between JPEG complexity and fitness.
* `min r_{fit, laplacian_variance} = 0.0524` worst choice, indicating no correlation at all.

Correlation between the same complexity metrics **of the each label** and achieved fitness:

| Metric | Cor(fit, v) |
| ------ | ----------- |
| label_count_per_image | 0.1808766400116384|
| label_size | 0.15095686543906062|
| relative_label_size | 0.053125526798248744|
| lbl_hist_entropy | 0.17735363985009658|
| lbl_fractal_dimension | 0.14932066630947147|
| lbl_texture_features | **0.4111840109022833**|
| lbl_edge_density | **0.32382825397606485**|
| lbl_laplacian_variance | 0.2990078843142231|
| lbl_num_superpixels | **0.36620833983254**|

Estimation for the whole image:

* `max r_{fit, lbl_texture_features} = 0.0.434` actual "best" choice, texture_feature of the labels;
* `max r_{fit, lbl_edge_density} = 0.324` shows a positive correlation between edge density of labels and fitness.
* `max r_{fit, lbl_num_superpixels} = 0.366` shows a positive correlation between number of superpixels in the label and fitness.
* `min r_{fit, relative_label_size} = 0.0531` worst choice, indicating no correlation at all.

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
