#!/bin/bash

# ==============
# TIMER
# ==============

SECONDS=3
echo "Waiting for $SECONDS sec ..."
sleep $SECONDS
echo "Continue ..."

# ==========================================================
# SETUP
# ==========================================================

echo "------------"
commandline="mono /var/local/prime/optimization/Optimization.Commandline/bin/Debug/Optimization.Commandline.exe"

# ----------------------------------------------------------
# Default parameters
# ----------------------------------------------------------
RUNS=3
GENERATIONS=150
CWDIR="D:\evias_expmts"

exmpts_train=()
expmts_val=()
expmts_res=()

# 0
expmnts_train+=("Aircarbon3\20210325_13h25_rov\training\80.jpg_dark_1")
expmnts_val+=("Aircarbon3\20210325_13h25_rov\training\81.jpg_dark")
expmnts_res+=("Aircarbon3\20210325_13h25_rov\results")

# 1
expmnts_train+=("Aircarbon3\20210325_13h25_rov\training\80.jpg_dark_2")
expmnts_val+=("Aircarbon3\20210325_13h25_rov\training\81.jpg_dark")
expmnts_res+=("Aircarbon3\20210325_13h25_rov\results")

# 2
expmnts_train+=("Aircarbon3\20210325_13h25_rov\training\80.jpg_dark_3")
expmnts_val+=("Aircarbon3\20210325_13h25_rov\training\81.jpg_dark")
expmnts_res+=("Aircarbon3\20210325_13h25_rov\results")

# 3
expmnts_train+=("Aircarbon3\20210325_13h25_rov\training\80.jpg_dark_4")
expmnts_val+=("Aircarbon3\20210325_13h25_rov\training\81.jpg_dark")
expmnts_res+=("Aircarbon3\20210325_13h25_rov\results")

# 4
expmnts_train+=("Aircarbon3\20210325_13h25_rov\training\80.jpg_dark_5")
expmnts_val+=("Aircarbon3\20210325_13h25_rov\training\81.jpg_dark")
expmnts_res+=("Aircarbon3\20210325_13h25_rov\results")

# 5
expmnts_train+=("Aircarbon3\20210325_13h25_rov\training\80.jpg_bright")
expmnts_val+=("Aircarbon3\20210325_13h25_rov\training\81.jpg_bright")
expmnts_res+=("Aircarbon3\20210325_13h25_rov\results")

# 6
expmnts_train+=("Magnetic-Tile-Defect\MT_Blowhole_train")
expmnts_val+=("Magnetic-Tile-Defect\MT_Blowhole_val")
expmnts_res+=("Magnetic-Tile-Defect\results")

# 7
expmnts_train+=("Aircarbon2\Blende5_6_1800mA_rov\training\t_8.jpg")
expmnts_val+=("Aircarbon2\Blende5_6_1800mA_rov\training\t_12.jpg")
expmnts_res+=("Aircarbon2\Blende5_6_1800mA_rov\results")

# 8
expmnts_train+=("severstal-steel\train_cgp")
expmnts_val+=("severstal-steel\val_cgp")
expmnts_res+=("severstal-steel\results_cgp")

# 9
expmnts_train+=("Pultrusion\resin_cgp\train")
expmnts_val+=("Pultrusion\resin_cgp\val")
expmnts_res+=("Pultrusion\results")

# 10
expmnts_train+=("Pultrusion\window_cgp\train")
expmnts_val+=("Pultrusion\window_cgp\val")
expmnts_res+=("Pultrusion\results")

# 11
expmnts_train+=("Pultrusion\resin_cgp_augmntd\train")
expmnts_val+=("Pultrusion\resin_cgp_augmntd\val")
expmnts_res+=("Pultrusion\results")

# 12
expmnts_train+=("KolektorSDD\kos10")
expmnts_val+=("KolektorSDD\kos25")
expmnts_res+=("KolektorSDD\results")

# 13
expmnts_train+=("FabricDefectsAITEX\train")
expmnts_val+=("FabricDefectsAITEX\val")
expmnts_res+=("FabricDefectsAITEX\results")

# 14
expmnts_train+=("MVTecAnomalyDetection\carpet_train")
expmnts_val+=("MVTecAnomalyDetection\carpet_val")
expmnts_res+=("MVTecAnomalyDetection\carpet_results")

# 15
expmnts_train+=("MVTecAnomalyDetection\leather_train")
expmnts_val+=("MVTecAnomalyDetection\leather_val")
expmnts_res+=("MVTecAnomalyDetection\leather_results")

# 16
expmnts_train+=("MVTecAnomalyDetection\capsule_crack_train")
expmnts_val+=("MVTecAnomalyDetection\capsule_crack_val")
expmnts_res+=("MVTecAnomalyDetection\results")

# 17
expmnts_train+=("MVTecAnomalyDetection\metal_nut_color_train")
expmnts_val+=("MVTecAnomalyDetection\metal_nut_color_val")
expmnts_res+=("MVTecAnomalyDetection\results")

# 18
expmnts_train+=("MVTecAnomalyDetection\pill_crack_train")
expmnts_val+=("MVTecAnomalyDetection\pill_crack_val")
expmnts_res+=("MVTecAnomalyDetection\results")

# 19
expmnts_train+=("MVTecAnomalyDetection\grid_thread_train")
expmnts_val+=("MVTecAnomalyDetection\grid_thread_val")
expmnts_res+=("MVTecAnomalyDetection\results")

# 20
expmnts_train+=("MVTecAnomalyDetection\tile_crack_train")
expmnts_val+=("MVTecAnomalyDetection\tile_crack_val")
expmnts_res+=("MVTecAnomalyDetection\results")

# 21
expmnts_train+=("MVTecAnomalyDetection\wood_scratch_train")
expmnts_val+=("MVTecAnomalyDetection\wood_scratch_val")
expmnts_res+=("MVTecAnomalyDetection\results")

# 22
expmnts_train+=("MVTecAnomalyDetection\zipper_rough_train")
expmnts_val+=("MVTecAnomalyDetection\zipper_rough_val")
expmnts_res+=("MVTecAnomalyDetection\results")

# 23
expmnts_train+=("MVTecAnomalyDetection\bottle_broken_large_train")
expmnts_val+=("MVTecAnomalyDetection\bottle_broken_large_val")
expmnts_res+=("MVTecAnomalyDetection\results")

# 24
expmnts_train+=("MVTecAnomalyDetection\bottle_broken_small_train")
expmnts_val+=("MVTecAnomalyDetection\bottle_broken_small_val")
expmnts_res+=("MVTecAnomalyDetection\results")

# 25
expmnts_train+=("MVTecAnomalyDetection\cable_missing_train")
expmnts_val+=("MVTecAnomalyDetection\cable_missing_val")
expmnts_res+=("MVTecAnomalyDetection\results")
# 26
expmnts_train+=("MVTecAnomalyDetection\hazelnut_crack_train")
expmnts_val+=("MVTecAnomalyDetection\hazelnut_crack_val")
expmnts_res+=("MVTecAnomalyDetection\results")

# 27
expmnts_train+=("MVTecAnomalyDetection\hazelnut_crack_train")
expmnts_val+=("MVTecAnomalyDetection\hazelnut_crack_val")
expmnts_res+=("MVTecAnomalyDetection\results")

# 28
expmnts_train+=("MVTecAnomalyDetection\screw_scratch_neck_train")
expmnts_val+=("MVTecAnomalyDetection\screw_scratch_neck_val")
expmnts_res+=("MVTecAnomalyDetection\results")

# 29
expmnts_train+=("MVTecAnomalyDetection\transistor_damaged_case_train")
expmnts_val+=("MVTecAnomalyDetection\transistor_damaged_case_val")
expmnts_res+=("MVTecAnomalyDetection\results")

# 30
# REM damaged roving with gap
expmnts_train+=("MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone\training")
expmnts_val+=("MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone\training")
expmnts_res+=("MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone\results")

# 31
expmnts_train+=("MAIPreform2.0\20170502_Compositence\Spule1_0117_Upside\undone\training")
expmnts_val+=("MAIPreform2.0\20170502_Compositence\Spule1_0117_Upside\undone\training")
expmnts_res+=("MAIPreform2.0\20170502_Compositence\Spule1_0117_Upside\undone\results")

# 32
expmnts_train+=("MAIPreform2.0\20170502_Compositence\Spule2-0816_Upside\undone\durchlauf2\training")
expmnts_val+=("MAIPreform2.0\20170502_Compositence\Spule2-0816_Upside\undone\durchlauf2\training")
expmnts_res+=("MAIPreform2.0\20170502_Compositence\Spule2-0816_Upside\undone\durchlauf2\results")

# 33
expmnts_train+=("MAIPreform2.0\20170502_Compositence\Spule2-0816_Upside\undone\durchlauf1\training")
expmnts_val+=("MAIPreform2.0\20170502_Compositence\Spule2-0816_Upside\undone\durchlauf1\training")
expmnts_res+=("MAIPreform2.0\20170502_Compositence\Spule2-0816_Upside\undone\durchlauf1\results")

# 34
expmnts_train+=("MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone_thread_hole\training")
expmnts_val+=("MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone_thread_hole\training")
expmnts_res+=("MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone_thread_hole\results")

# 35
expmnts_train+=("MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone_thread_hole_256\training")
expmnts_val+=("MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone_thread_hole_256\training")
expmnts_res+=("MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone_thread_hole_256\results")

# ==========================================================
# Run Experiments
# ==========================================================
# for exp in ${expmnts_train[@]}; do

for i in {21..29}; do
	echo "RUNS: $RUNS"
	echo "GENERATIONS: $GENERATIONS"
	
	TRAIN_DIR="$CWDIR\\${expmnts_train[$i]}"
	VAL_DIR="$CWDIR\\${expmnts_val[$i]}"
	RESULTS_DIR="$CWDIR\\${expmnts_res[$i]}"
	
	# echo "TRAIN_DIR: $CWDIR\${expmnts_train[$i]}"
	# echo "VAL_DIR: $CWDIR\${expmnts_val[$i]}"
	# echo "RESULTS_DIR: $CWDIR\${expmnts_res[$i]}"
	echo "train-data-dir: $TRAIN_DIR"
	echo "val-data-dir: $VAL_DIR"
	echo "results-dir: $RESULTS_DIR"
		
	echo "--------"
	echo "Start evolution"
	echo "...................."
		
	$commandline batch --backend=halcon --runs=$RUNS --train-data-dir=$TRAIN_DIR --val-data-dir=$VAL_DIR --generations=$GENERATIONS
	# --results-dir=$RESULTS_DIR
	
	echo "...................."
	echo "Finished"
	echo "--------"
done