# Experiment Overview

Experiments on image datasets using optimization

| Experiment | Dataset | Problem | Hypothesis | Goal |
| ---------- | ------- | ------- | ---------- | ---- |
| CGP Classic | Carbon Fibres | Object Detection: fitness on bounding boxes | worst results compared to CGP-SSR, CGP with parameter tuning, U-Net | based on settings used for ICMLA 2017 |
| CGP with Parameter Optimisation | Carbon Fibres | Object Detection: fitness on bounding boxes | fitness \textit{significantly} superior to CGP Classic; inferior to CGP-SSR, to U-Net | based on settings from ICMLA 2017 |
| CGP Classic | Carbon Fibres | Semantic Segmentation with free evolution | \textit{significantly} inferior results compared to CGP-SSR, CGP with parameter tuning, U-Net | Reproduce results from traditional approach (e. g. ICMLA 2017), set a reference |
| CGP with Parameter Optimisation | Carbon Fibres | Semantic Segmentation using only parameter mutation | fitness \textit{significantly} superior to CGP Classic; inferior to CGP-SSR, to U-Net | Reproduce results from traditional approach (e. g. ICMLA 2017), set a reference |
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
| Random Search | Carbon Fibres | Semantic Segmentation | Fitness results around 0.0 | Establish a low level, default reference to all other experiments |
