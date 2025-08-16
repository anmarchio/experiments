import os

import numpy as np

from param_tuning.hdev_manual_best.run_hdev_manual_best import MANUAL_HDEV_PIPELINES_BEST
from param_tuning.hdev_manual_mean.AirCarbon2_t_8_jpg_mean import AirCarbon2_t_8_jpg_training_source_path
from param_tuning.hdev_manual_mean.AirCarbon3_80_jpg_bright_mean import AirCarbon3_80_jpg_bright_training_source_path
from param_tuning.hdev_manual_mean.AirCarbon3_80_jpg_dark_1_mean import AirCarbon3_80_jpg_dark_1_training_source_path
from param_tuning.hdev_manual_mean.AirCarbon3_80_jpg_dark_2_mean import AirCarbon3_80_jpg_dark_2_training_source_path
from param_tuning.hdev_manual_mean.AirCarbon3_80_jpg_dark_3_mean import AirCarbon3_80_jpg_dark_3_training_source_path
from param_tuning.hdev_manual_mean.AirCarbon3_80_jpg_dark_4_mean import AirCarbon3_80_jpg_dark_4_training_source_path
from param_tuning.hdev_manual_mean.AirCarbon3_80_jpg_dark_5_mean import AirCarbon3_80_jpg_dark_5_training_source_path
from param_tuning.hdev_manual_mean.CF_ReferenceSet_Small_Dark_mean_pipeline import \
    CF_ReferenceSet_Small_Dark_training_source_path
from param_tuning.hdev_manual_mean.CF_ReferenceSet_Small_Light_mean_pipeline import \
    CF_ReferenceSet_Small_Light_training_source_path
from param_tuning.hdev_manual_mean.CF_ReferenceSet_mean_pipeline import CF_ReferenceSet_training_source_path
from param_tuning.hdev_manual_mean.CrackForest_mean import CrackForest_training_source_path
from param_tuning.hdev_manual_mean.FabricDefectsAITEX_mean import FabricDefectsAITEX_training_source_path
from param_tuning.hdev_manual_mean.MAIPreform2_Spule0_0315_Upside_Thread_256_mean_pipeline import \
    MAIPreform2_Spule0_0315_Upside_Thread_256_training_source_path
from param_tuning.hdev_manual_mean.MAIPreform2_Spule0_0315_Upside_Thread_mean_pipeline import \
    MAIPreform2_Spule0_0315_Upside_Thread_training_source_path
from param_tuning.hdev_manual_mean.MAIPreform2_Spule0_0315_Upside_mean_pipeline import \
    MAIPreform2_Spule0_0315_Upside_training_source_path
from param_tuning.hdev_manual_mean.MAIPreform2_Spule0_0816_Upside_mean_pipeline import \
    MAIPreform2_Spule0_0816_Upside_training_source_path
from param_tuning.hdev_manual_mean.MT_Blowhole_train_mean import MT_Blowhole_train_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Bottle_Broken_Lg_mean import MVTec_AD_Bottle_Broken_Lg_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Bottle_Broken_Sm_mean import MVTec_AD_Bottle_Broken_Sm_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Cable_Missing_mean import MVTec_AD_Cable_Missing_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Capsule_mean import MVTec_AD_Capsule_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Carpet_mean import MVTec_AD_Carpet_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Grid_Thread_mean import MVTec_AD_Grid_Thread_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Hazelnut_Crack_mean import MVTec_AD_Hazelnut_Crack_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Leather_mean import MVTec_AD_Leather_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Metal_Nut_mean import MVTec_AD_Metal_Nut_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Pill_Crack_mean import MVTec_AD_Pill_Crack_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Screw_Scratch_mean import MVTec_AD_Screw_Scratch_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Tile_Crack_mean import MVTec_AD_Tile_Crack_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Toothbrush_Sm_mean import MVTec_AD_Toothbrush_Sm_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Transistor_mean import MVTec_AD_Transistor_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Wood_Scratch_mean_pipeline import MVTec_AD_Wood_Scratch_training_source_path
from param_tuning.hdev_manual_mean.MVTec_AD_Zipper_Rough_mean_pipeline import MVTec_AD_Zipper_Rough_training_source_path
from param_tuning.hdev_manual_mean.Pultrusion_Resin_Augmtd_mean_pipeline import \
    Pultrusion_Resin_Augmtd_training_source_path
from param_tuning.hdev_manual_mean.Pultrusion_Resin_mean_pipeline import Pultrusion_Resin_training_source_path
from param_tuning.hdev_manual_mean.Pultrusion_Window_mean_pipeline import Pultrusion_Window_training_source_path
from param_tuning.hdev_manual_mean.run_hdev_manual_mean import MANUAL_HDEV_PIPELINES_MEAN, pipelines_mean, bounds_mean, \
    initial_params_mean
from param_tuning.hdev_manual_mean.severstal_steel_mean import severstal_steel_training_source_path
from settings import PARAM_TUNING_HDEV_MANUAL


def get_manual_hdev_pipeline(pipeline_name: str, params: np.array, cross_dataset=None):
    pipelines = pipelines_mean + pipelines_best
    pipeline_function = pipelines.get(pipeline_name)

    if pipeline_function:
        # Call the specific function with the 'params' argument
        return pipeline_function(params, cross_dataset)
    else:
        return None


def get_manual_hdev_pipeline_bounds(pipeline_name: str) -> []:
    bounds = bounds_mean + bounds_best
    return bounds.get(pipeline_name, None)


def get_initial_state_by_pipeline_name(pipeline_name: str) -> []:
    initial_params = initial_params_mean + initial_params_best
    return initial_params.get(pipeline_name, None)


def get_dataset_by_pipeline_name(pipeline_name: str) -> str:
    return dataset_paths.get(pipeline_name, None)


def get_manual_hdev_pipeline_path(pipeline_name: str):
    for name in MANUAL_HDEV_PIPELINES_MEAN + MANUAL_HDEV_PIPELINES_BEST:
        if name == pipeline_name:
            return os.path.join(PARAM_TUNING_HDEV_MANUAL, name)
    return None


def get_manual_hdev_pipeline_training_source_path(pipeline_name: str) -> str:
    if (pipeline_name == "AirCarbon2_t_8.jpg_mean_pipeline" or
            pipeline_name == "AirCarbon2_t_8.jpg_best_pipeline"):
        return AirCarbon2_t_8_jpg_training_source_path
    elif (pipeline_name == "AirCarbon3_80.jpg_bright_mean_pipeline" or
          "AirCarbon3_80.jpg_bright_best_pipeline"):
        return AirCarbon3_80_jpg_bright_training_source_path
    elif (pipeline_name == "AirCarbon3_80.jpg_dark_1_mean_pipeline" or
          "AirCarbon3_80.jpg_dark_1_best_pipeline"):
        return AirCarbon3_80_jpg_dark_1_training_source_path
    elif (pipeline_name == "AirCarbon3_80.jpg_dark_2_mean_pipeline" or
          "AirCarbon3_80.jpg_dark_2_best_pipeline"):
        return AirCarbon3_80_jpg_dark_2_training_source_path
    elif (pipeline_name == "AirCarbon3_80.jpg_dark_2_mean_pipeline" or
          "AirCarbon3_80.jpg_dark_2_best_pipeline"):
        return AirCarbon3_80_jpg_dark_3_training_source_path
    elif (pipeline_name == "AirCarbon3_80.jpg_dark_3_mean_pipeline" or
          "AirCarbon3_80.jpg_dark_3_best_pipeline"):
        return AirCarbon3_80_jpg_dark_3_training_source_path
    elif (pipeline_name == "AirCarbon3_80.jpg_dark_4_mean_pipeline" or
          "AirCarbon3_80.jpg_dark_4_best_pipeline"):
        return AirCarbon3_80_jpg_dark_4_training_source_path
    elif (pipeline_name == "AirCarbon3_80.jpg_dark_5_mean_pipeline"
          or "AirCarbon3_80.jpg_dark_5_best_pipeline"):
        return AirCarbon3_80_jpg_dark_5_training_source_path
    elif (pipeline_name == "MAIPreform2_Spule0_0315_Upside_Thread_256_mean_pipeline" or
          "MAIPreform2_Spule0_0315_Upside_Thread_256_best_pipeline"):
        return MAIPreform2_Spule0_0315_Upside_Thread_256_training_source_path
    elif (pipeline_name == "MAIPreform2_Spule0_0315_Upside_Thread_mean_pipeline" or
          "MAIPreform2_Spule0_0315_Upside_Thread_best_pipeline"):
        return MAIPreform2_Spule0_0315_Upside_Thread_training_source_path
    elif (pipeline_name == "MAIPreform2_Spule0_0315_Upside_mean_pipeline" or
          "MAIPreform2_Spule0_0315_Upside_best_pipeline"):
        return MAIPreform2_Spule0_0315_Upside_training_source_path
    elif (pipeline_name == "MAIPreform2_Spule0_0816_Upside_mean_pipeline" or
          "MAIPreform2_Spule0_0816_Upside_best_pipeline"):
        return MAIPreform2_Spule0_0816_Upside_training_source_path
    elif (pipeline_name == "CF_ReferenceSet_mean_pipeline" or
          "CF_ReferenceSet_best_pipeline"):
        return CF_ReferenceSet_training_source_path
    elif (pipeline_name == "CF_ReferenceSet_Small_Dark_mean_pipeline" or
          "CF_ReferenceSet_Small_Dark_best_pipeline"):
        return CF_ReferenceSet_Small_Dark_training_source_path
    elif (pipeline_name == "CF_ReferenceSet_Small_Light_mean_pipeline" or
          "CF_ReferenceSet_Small_Light_best_pipeline"):
        return CF_ReferenceSet_Small_Light_training_source_path
    elif (pipeline_name == "FabricDefectsAITEX_mean_pipeline" or
          "FabricDefectsAITEX_best_pipeline"):
        return FabricDefectsAITEX_training_source_path
    elif (pipeline_name == "MT_Blowhole_train_mean_pipeline" or
          "MT_Blowhole_train_best_pipeline"):
        return MT_Blowhole_train_training_source_path
    elif (pipeline_name == "MVTec_AD_Bottle_Broken_Lg_mean_pipeline" or
          "MVTec_AD_Bottle_Broken_Lg_best_pipeline"):
        return MVTec_AD_Bottle_Broken_Lg_training_source_path
    elif (pipeline_name == "MVTec_AD_Bottle_Broken_Sm_mean_pipeline" or
          "MVTec_AD_Bottle_Broken_Sm_best_pipeline"):
        return MVTec_AD_Bottle_Broken_Sm_training_source_path
    elif (pipeline_name == "MVTec_AD_Cable_Missing_mean_pipeline" or
          "MVTec_AD_Cable_Missing_best_pipeline"):
        return MVTec_AD_Cable_Missing_training_source_path
    elif (pipeline_name == "MVTec_AD_Capsule_mean_pipeline" or
          "MVTec_AD_Capsule_best_pipeline"):
        return MVTec_AD_Capsule_training_source_path
    elif (pipeline_name == "MVTec_AD_Carpet_mean_pipeline" or
          "MVTec_AD_Carpet_best_pipeline"):
        return MVTec_AD_Carpet_training_source_path
    elif (pipeline_name == "MVTec_AD_Grid_Thread_mean_pipeline" or
          "MVTec_AD_Grid_Thread_best_pipeline"):
        return MVTec_AD_Grid_Thread_training_source_path
    elif (pipeline_name == "MVTec_AD_Hazelnut_Crack_mean_pipeline" or
          "MVTec_AD_Hazelnut_Crack_best_pipeline"):
        return MVTec_AD_Hazelnut_Crack_training_source_path
    elif (pipeline_name == "MVTec_AD_Leather_mean_pipeline" or
          "MVTec_AD_Leather_best_pipeline"):
        return MVTec_AD_Leather_training_source_path
    elif (pipeline_name == "MVTec_AD_Metal_Nut_mean_pipeline" or
          "MVTec_AD_Metal_Nut_best_pipeline"):
        return MVTec_AD_Metal_Nut_training_source_path
    elif (pipeline_name == "MVTec_AD_Pill_Crack_mean_pipeline" or
          "MVTec_AD_Pill_Crack_best_pipeline"):
        return MVTec_AD_Pill_Crack_training_source_path
    elif (pipeline_name == "MVTec_AD_Screw_Scratch_mean_pipeline" or
        "MVTec_AD_Screw_Scratch_best_pipeline"):
        return MVTec_AD_Screw_Scratch_training_source_path
    elif (pipeline_name == "MVTec_AD_Tile_Crack_mean_pipeline" or
          "MVTec_AD_Tile_Crack_best_pipeline"):
        return MVTec_AD_Tile_Crack_training_source_path
    elif (pipeline_name == "MVTec_AD_Toothbrush_Sm_mean_pipeline" or
          "MVTec_AD_Toothbrush_Sm_best_pipeline"):
        return MVTec_AD_Toothbrush_Sm_training_source_path
    elif (pipeline_name == "MVTec_AD_Wood_Scratch_mean_pipeline" or
          "MVTec_AD_Wood_Scratch_best_pipeline"):
        return MVTec_AD_Wood_Scratch_training_source_path
    elif (pipeline_name == "MVTec_AD_Zipper_Rough_mean_pipeline" or
          "MVTec_AD_Zipper_Rough_best_pipeline"):
        return MVTec_AD_Zipper_Rough_training_source_path
    elif (pipeline_name == "Pultrusion_Resin_Augmtd_mean_pipeline" or
          "Pultrusion_Resin_Augmtd_best_pipeline"):
        return Pultrusion_Resin_Augmtd_training_source_path
    elif (pipeline_name == "Pultrusion_Resin_mean_pipeline" or
          "Pultrusion_Resin_best_pipeline"):
        return Pultrusion_Resin_training_source_path
    elif (pipeline_name == "Pultrusion_Window_mean_pipeline" or
          "Pultrusion_Window_best_pipeline"):
        return Pultrusion_Window_training_source_path
    elif (pipeline_name == "severstal-steel_mean_pipeline" or
          "severstal-steel_best_pipeline"):
        return severstal_steel_training_source_path
    elif (pipeline_name == "MVTec_AD_Transistor_mean_pipeline" or
          "MVTec_AD_Transistor_best_pipeline"):
        return MVTec_AD_Transistor_training_source_path
    elif (pipeline_name == "CrackForest_mean_pipeline" or
          "CrackForest_best_pipeline"):
        return CrackForest_training_source_path

    return None


dataset_paths = {
    "AirCarbon2_t_8.jpg_mean_pipeline": "/Aircarbon2/Blende5_6_1800mA_rov/training/t_8.jpg/images",
    "AirCarbon3_80.jpg_bright_mean_pipeline": "/Aircarbon3/20210325_13h25_rov/training/80.jpg_bright/images",
    "AirCarbon3_80.jpg_dark_1_mean_pipeline": "/Aircarbon3/20210325_13h25_rov/training/80.jpg_dark_1/images",
    "AirCarbon3_80.jpg_dark_2_mean_pipeline": "/Aircarbon3/20210325_13h25_rov/training/80.jpg_dark_2/images",
    "AirCarbon3_80.jpg_dark_3_mean_pipeline": "/Aircarbon3/20210325_13h25_rov/training/80.jpg_dark_3/images",
    "AirCarbon3_80.jpg_dark_4_mean_pipeline": "/Aircarbon3/20210325_13h25_rov/training/80.jpg_dark_4/images",
    "AirCarbon3_80.jpg_dark_5_mean_pipeline": "/Aircarbon3/20210325_13h25_rov/training/80.jpg_dark_5/images",
    "MAIPreform2_Spule0_0315_Upside_Thread_256_mean_pipeline": "/MAIPreform2.0/20170502_Compositence/Spule0-0315_Upside/undone_thread_hole_256/training/images",
    "MAIPreform2_Spule0_0315_Upside_Thread_mean_pipeline": "/MAIPreform2.0/20170502_Compositence/Spule0-0315_Upside/undone_thread_hole/training/images",
    "MAIPreform2_Spule0_0315_Upside_mean_pipeline": "/MAIPreform2.0/20170502_Compositence/Spule0-0315_Upside/undone/training/images",
    "MAIPreform2_Spule0_0816_Upside_mean_pipeline": "/MAIPreform2.0/20170502_Compositence/Spule2-0816_Upside/undone/durchlauf1/training/images",
    "CF_ReferenceSet_mean_pipeline": "/Aircarbon2/CF_ReferenceSet/images",
    "CF_ReferenceSet_Small_Dark_mean_pipeline": "/Aircarbon2/CF_ReferenceSet_Small_Dark/images",
    "CF_ReferenceSet_Small_Light_mean_pipeline": "/Aircarbon2/CF_ReferenceSet_Small_Light/images",
    "FabricDefectsAITEX_mean_pipeline": "/FabricDefectsAITEX/train/images",
    "MT_Blowhole_train_mean_pipeline": "/Magnetic-Tile-Defect/MT_Blowhole_train/images",
    "MVTec_AD_Bottle_Broken_Lg_mean_pipeline": "/MVTecAnomalyDetection/bottle_broken_large_train/images",
    "MVTec_AD_Bottle_Broken_Sm_mean_pipeline": "/MVTecAnomalyDetection/bottle_broken_small_train/images",
    "MVTec_AD_Cable_Missing_mean_pipeline": "/MVTecAnomalyDetection/cable_missing_train/images",
    "MVTec_AD_Capsule_mean_pipeline": "/MVTecAnomalyDetection/capsule_crack_train/images",
    "MVTec_AD_Carpet_mean_pipeline": "/MVTecAnomalyDetection/carpet_train/images",
    "MVTec_AD_Grid_Thread_mean_pipeline": "/MVTecAnomalyDetection/grid_thread_train/images",
    "MVTec_AD_Hazelnut_Crack_mean_pipeline": "/MVTecAnomalyDetection/hazelnut_crack_train/images",
    "MVTec_AD_Leather_mean_pipeline": "/MVTecAnomalyDetection/leather_train/images",
    "MVTec_AD_Metal_Nut_mean_pipeline": "/MVTecAnomalyDetection/metal_nut_color_train/images",
    "MVTec_AD_Pill_Crack_mean_pipeline": "/MVTecAnomalyDetection/pill_crack_train/images",
    "MVTec_AD_Screw_Scratch_mean_pipeline": "/MVTecAnomalyDetection/screw_scratch_neck_train/images",
    "MVTec_AD_Tile_Crack_mean_pipeline": "/MVTecAnomalyDetection/tile_crack_train/images",
    "MVTec_AD_Toothbrush_Sm_mean_pipeline": "/MVTecAnomalyDetection/toothbrush_small_train/images",
    "MVTec_AD_Wood_Scratch_mean_pipeline": "/MVTecAnomalyDetection/wood_scratch_train/images",
    "MVTec_AD_Zipper_Rough_mean_pipeline": "/MVTecAnomalyDetection/zipper_rough_train/images",
    "Pultrusion_Resin_Augmtd_mean_pipeline": "/Pultrusion/resin_cgp_augmntd/train/images",
    "Pultrusion_Resin_mean_pipeline": "/Pultrusion/resin_cgp/train/images",
    "Pultrusion_Window_mean_pipeline": "/Pultrusion/window_cgp/train/images",
    "severstal-steel_mean_pipeline": "/severstal-steel/train_cgp/images",
    "MVTec_AD_Transistor_mean_pipeline": "/MVTecAnomalyDetection/transistor_damaged_case_train/images",
    "CrackForest_mean_pipeline": "/CrackForest/images",
}
