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
REM call SET COMMANDLINE=D:\dev\optimization\Optimization.Commandline\bin\Debug\Optimization.Commandline.exe
call SET COMMANDLINE=D:\dev\github\optimization\Optimization.Commandline\bin\Debug\Optimization.Commandline.exe

REM ----------------------------------------------------------
REM Default parameters
REM ----------------------------------------------------------
call SET RUNS=5
call SET GENERATIONS=50
call SET CWDIR=D:\evias_expmts

setlocal EnableDelayedExpansion 

set expmnts_train[0]=Aircarbon3\20210325_13h25_rov\training\80.jpg_dark_1
set expmnts_val[0]=Aircarbon3\20210325_13h25_rov\training\81.jpg_dark
set expmnts_res[0]=Aircarbon3\20210325_13h25_rov\results

set expmnts_train[1]=MVTecAnomalyDetection\cable_missing_train
set expmnts_val[1]=MVTecAnomalyDetection\cable_missing_val
set expmnts_res[1]=MVTecAnomalyDetection\results

set expmnts_train[2]=Pultrusion\resin_cgp_augmntd\train
set expmnts_val[2]=Pultrusion\resin_cgp_augmntd\val
set expmnts_res[2]=Pultrusion\results

set expmnts_train[3]=severstal-steel\train_cgp
set expmnts_val[3]=severstal-steel\val_cgp 
set expmnts_res[3]=severstal-steel\results_cgp

REM ==========================================================
REM Run Experiments
REM ==========================================================
REM for %%e in (%expmnts%) do (

for /l %%i in (0 1 1) do (
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