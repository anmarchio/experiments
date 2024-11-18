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

set expmnts_train[0]=CrackForest
set expmnts_val[0]=CrackForest
set expmnts_res[0]=results

set expmnts_train[1]=MVTecAnomalyDetection\transistor_damaged_case_train
set expmnts_val[1]=MVTecAnomalyDetection\transistor_damaged_case_train
set expmnts_res[1]=results
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