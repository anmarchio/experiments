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
call SET COMMANDLINE=C:\Users\Public\dev_mara\optimization\Optimization.Commandline\bin\Debug\Optimization.Commandline.exe

REM ----------------------------------------------------------
REM Default parameters
REM ----------------------------------------------------------
call SET RUNS=3
call SET GENERATIONS=250
call SET CWDIR=C:\Users\Public\evias_expmts\

setlocal EnableDelayedExpansion 

set expmnts_train[0]=waterbreak_cgp\20230719_Halogen_Pola
set expmnts_val[0]=waterbreak_cgp\20230719_Halogen_Pola
set expmnts_res[0]=C:\Users\Public\dev_mara\optimization\IO\results

set expmnts_train[1]=waterbreak_cgp\20230717_White_Darkfield
set expmnts_val[1]=waterbreak_cgp\20230717_White_Darkfield
set expmnts_res[1]=C:\Users\Public\dev_mara\optimization\IO\results

set expmnts_train[2]=waterbreak_cgp\202307719_Infrared_2
set expmnts_val[2]=waterbreak_cgp\202307719_Infrared_2
set expmnts_res[2]=C:\Users\Public\dev_mara\optimization\IO\results


REM ==========================================================
REM Run Experiments
REM ==========================================================
REM for %%e in (%expmnts%) do (

for /l %%i in (1 1 1) do (
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