@ECHO OFF

REM ==============
REM TIMER
REM ==============

set SECONDS=3
ECHO Waiting for %SECONDS% sec ...
TIMEOUT %SECONDS%
ECHO Continue ...

REM ==========================================================
REM SETUP
REM ==========================================================

ECHO ------------
call SET COMMANDLINE=D:\dev\optimization\Optimization.Commandline\bin\Debug\Optimization.Commandline.exe

REM ----------------------------------------------------------
REM Default parameters
REM ----------------------------------------------------------
call SET RUNS=5
call SET GENERATIONS=30
call SET CWDIR=D:\evias_expmts

setlocal EnableDelayedExpansion 

set expmnts_train[0]=Aircarbon3\20210325_13h25_rov\training\80.jpg_dark_1
set expmnts_val[0]=Aircarbon3\20210325_13h25_rov\training\81.jpg_dark
set expmnts_res[0]=Aircarbon3\20210325_13h25_rov\results

set expmnts_train[1]=Aircarbon3\20210325_13h25_rov\training\80.jpg_dark_2
set expmnts_val[1]=Aircarbon3\20210325_13h25_rov\training\81.jpg_dark
set expmnts_res[1]=Aircarbon3\20210325_13h25_rov\results

set expmnts_train[2]=Aircarbon3\20210325_13h25_rov\training\80.jpg_dark_3
set expmnts_val[2]=Aircarbon3\20210325_13h25_rov\training\81.jpg_dark
set expmnts_res[2]=Aircarbon3\20210325_13h25_rov\results

set expmnts_train[3]=Aircarbon3\20210325_13h25_rov\training\80.jpg_dark_4
set expmnts_val[3]=Aircarbon3\20210325_13h25_rov\training\81.jpg_dark
set expmnts_res[3]=Aircarbon3\20210325_13h25_rov\results

set expmnts_train[4]=Aircarbon3\20210325_13h25_rov\training\80.jpg_dark_5
set expmnts_val[4]=Aircarbon3\20210325_13h25_rov\training\81.jpg_dark
set expmnts_res[4]=Aircarbon3\20210325_13h25_rov\results

set expmnts_train[5]=Aircarbon3\20210325_13h25_rov\training\80.jpg_bright
set expmnts_val[5]=Aircarbon3\20210325_13h25_rov\training\81.jpg_bright
set expmnts_res[5]=Aircarbon3\20210325_13h25_rov\results

set expmnts_train[6]=Magnetic-Tile-Defect\MT_Blowhole_train
set expmnts_val[6]=Magnetic-Tile-Defect\MT_Blowhole_val
set expmnts_res[6]=Magnetic-Tile-Defect\results

set expmnts_train[7]=severstal-steel\train_cgp
set expmnts_val[7]=severstal-steel\val_cgp 
set expmnts_res[7]=severstal-steel\results_cgp

set expmnts_train[8]=Aircarbon2\Blende5_6_1800mA_rov\training\t_8.jpg
set expmnts_val[8]=Aircarbon2\Blende5_6_1800mA_rov\training\t_12.jpg
set expmnts_res[8]=Aircarbon2\Blende5_6_1800mA_rov\results

set expmnts_train[9]=Pultrusion\resin_cgp\train
set expmnts_val[9]=Pultrusion\resin_cgp\val
set expmnts_res[9]=Pultrusion\results

set expmnts_train[10]=Pultrusion\window_cgp\train
set expmnts_val[10]=Pultrusion\window_cgp\val
set expmnts_res[10]=Pultrusion\results

set expmnts_train[11]=Pultrusion\resin_cgp_augmntd\train
set expmnts_val[11]=Pultrusion\resin_cgp_augmntd\val
set expmnts_res[11]=Pultrusion\results

set expmnts_train[12]=KolektorSDD\kos10
set expmnts_val[12]=KolektorSDD\kos25
set expmnts_res[12]=KolektorSDD\results

set expmnts_train[13]=FabricDefectsAITEX\train
set expmnts_val[13]=FabricDefectsAITEX\val
set expmnts_res[13]=FabricDefectsAITEX\results

set expmnts_train[14]=MVTecAnomalyDetection\carpet_train
set expmnts_val[14]=MVTecAnomalyDetection\carpet_val
set expmnts_res[14]=MVTecAnomalyDetection\carpet_results

set expmnts_train[15]=MVTecAnomalyDetection\leather_train
set expmnts_val[15]=MVTecAnomalyDetection\leather_val
set expmnts_res[15]=MVTecAnomalyDetection\leather_results

set expmnts_train[16]=MVTecAnomalyDetection\capsule_crack_train
set expmnts_val[16]=MVTecAnomalyDetection\capsule_crack_val
set expmnts_res[16]=MVTecAnomalyDetection\results

set expmnts_train[17]=MVTecAnomalyDetection\metal_nut_color_train
set expmnts_val[17]=MVTecAnomalyDetection\metal_nut_color_val
set expmnts_res[17]=MVTecAnomalyDetection\results

set expmnts_train[18]=MVTecAnomalyDetection\pill_crack_train
set expmnts_val[18]=MVTecAnomalyDetection\pill_crack_val
set expmnts_res[18]=MVTecAnomalyDetection\results

set expmnts_train[19]=MVTecAnomalyDetection\grid_thread_train
set expmnts_val[19]=MVTecAnomalyDetection\grid_thread_val
set expmnts_res[19]=MVTecAnomalyDetection\results

set expmnts_train[20]=MVTecAnomalyDetection\tile_crack_train
set expmnts_val[20]=MVTecAnomalyDetection\tile_crack_val
set expmnts_res[20]=MVTecAnomalyDetection\results

set expmnts_train[21]=MVTecAnomalyDetection\wood_scratch_train
set expmnts_val[21]=MVTecAnomalyDetection\wood_scratch_val
set expmnts_res[21]=MVTecAnomalyDetection\results

set expmnts_train[22]=MVTecAnomalyDetection\zipper_rough_train
set expmnts_val[22]=MVTecAnomalyDetection\zipper_rough_val
set expmnts_res[22]=MVTecAnomalyDetection\results

set expmnts_train[23]=MVTecAnomalyDetection\bottle_broken_large_train
set expmnts_val[23]=MVTecAnomalyDetection\bottle_broken_large_val
set expmnts_res[23]=MVTecAnomalyDetection\results

set expmnts_train[24]=MVTecAnomalyDetection\bottle_broken_small_train
set expmnts_val[24]=MVTecAnomalyDetection\bottle_broken_small_val
set expmnts_res[24]=MVTecAnomalyDetection\results

set expmnts_train[25]=MVTecAnomalyDetection\cable_missing_train
set expmnts_val[25]=MVTecAnomalyDetection\cable_missing_val
set expmnts_res[25]=MVTecAnomalyDetection\results

set expmnts_train[26]=MVTecAnomalyDetection\hazelnut_crack_train
set expmnts_val[26]=MVTecAnomalyDetection\hazelnut_crack_val
set expmnts_res[26]=MVTecAnomalyDetection\results

set expmnts_train[27]=MVTecAnomalyDetection\hazelnut_crack_train
set expmnts_val[27]=MVTecAnomalyDetection\hazelnut_crack_val
set expmnts_res[27]=MVTecAnomalyDetection\results

set expmnts_train[28]=MVTecAnomalyDetection\screw_scratch_neck_train
set expmnts_val[28]=MVTecAnomalyDetection\screw_scratch_neck_val
set expmnts_res[28]=MVTecAnomalyDetection\results

set expmnts_train[29]=MVTecAnomalyDetection\transistor_damaged_case_train
set expmnts_val[29]=MVTecAnomalyDetection\transistor_damaged_case_val
set expmnts_res[29]=MVTecAnomalyDetection\results

REM damaged roving with gap

set expmnts_train[30]=MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone\training
set expmnts_val[30]=MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone\training
set expmnts_res[30]=MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone\results

set expmnts_train[31]=MAIPreform2.0\20170502_Compositence\Spule1_0117_Upside\undone\training
set expmnts_val[31]=MAIPreform2.0\20170502_Compositence\Spule1_0117_Upside\undone\training
set expmnts_res[31]=MAIPreform2.0\20170502_Compositence\Spule1_0117_Upside\undone\results

set expmnts_train[32]=MAIPreform2.0\20170502_Compositence\Spule2-0816_Upside\undone\durchlauf2\training
set expmnts_val[32]=MAIPreform2.0\20170502_Compositence\Spule2-0816_Upside\undone\durchlauf2\training
set expmnts_res[32]=MAIPreform2.0\20170502_Compositence\Spule2-0816_Upside\undone\durchlauf2\results

set expmnts_train[33]=MAIPreform2.0\20170502_Compositence\Spule2-0816_Upside\undone\durchlauf1\training
set expmnts_val[33]=MAIPreform2.0\20170502_Compositence\Spule2-0816_Upside\undone\durchlauf1\training
set expmnts_res[33]=MAIPreform2.0\20170502_Compositence\Spule2-0816_Upside\undone\durchlauf1\results

set expmnts_train[34]=MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone_thread_hole\training
set expmnts_val[34]=MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone_thread_hole\training
set expmnts_res[34]=MAIPreform2.0\20170502_Compositence\Spule0-0315_Upside\undone_thread_hole\results

REM ==========================================================
REM Run Experiments
REM ==========================================================
REM for %%e in (%expmnts%) do (
for /l %%i in (34 1 34) do (
	call echo RUNS: %RUNS%
	call echo GENERATIONS: %GENERATIONS%
	
	call SET TRAIN_DIR=%%CWDIR%%\%%expmnts_train[%%i]%%
	call SET VAL_DIR=%%CWDIR%%\%%expmnts_val[%%i]%%
	call SET RESULTS_DIR=%%CWDIR%%\%%expmnts_res[%%i]%%
	
	REM call echo TRAIN_DIR: %CWDIR%\%%expmnts_train[%%i]%%
	REM call echo VAL_DIR: %CWDIR%\%%expmnts_val[%%i]%%
	REM call echo RESULTS_DIR: %CWDIR%\%%expmnts_res[%%i]%%
	call echo train-data-dir: %%TRAIN_DIR%%
	call echo val-data-dir: %%VAL_DIR%%
	call echo results-dir: %%RESULTS_DIR%%
		
	echo --------
	echo Start evolution
	echo ....................
		
	call %COMMANDLINE% batch --backend=halcon --runs=%RUNS% --train-data-dir=%%TRAIN_DIR%% --val-data-dir=%%VAL_DIR%% --generations=%GENERATIONS%
	REM  --results-dir=%%RESULTS_DIR%%
	
	echo ....................
	echo Finished
	echo --------
)
