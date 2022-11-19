@ECHO OFF

REM ==========================================================
REM SETUP
REM ==========================================================

call SET COMMANDLINE=D:\dev\optimization\Optimization.Commandline\bin\Debug\Optimization.Commandline.exe

REM ----------------------------------------------------------
REM Default parameters
REM ----------------------------------------------------------
call SET RUNS=15
call SET GENERATIONS=150
call SET CWDIR=D:/dev/evias_expmnts

setlocal EnableDelayedExpansion 

REM AirCarbon
REM D:\evias_expmts\Aircarbon3\20210325_13h25_rov\training\images\t_80.jpg
REM D:\evias_expmts\Aircarbon3\20210325_13h25_rov\training\labels\t_80.jpg
REM Severstal Steel
REM D:\evias_expmts\severstal-steel\train_images
REM D:\evias_expmts\severstal-steel\train_binary

set expmnts=Aircarbon3\20210325_13h25_rov\training\images\t_80.jpg Aircarbon3\20210325_13h25_rov\training\labels\t_80.jpg D:\evias_expmts\severstal-steel\train_images D:\evias_expmts\severstal-steel\train_binary

REM ==========================================================
REM Run Experiments
REM ==========================================================
for %%e in (%expmnts%) do (
	call echo RUNS: %RUNS%
	call echo GENERATIONS: %GENERATIONS%
	
	REM t_2.jpg -- t_21.jpg
	call echo TRAIN_DIR: %CWDIR%\%%e
	call echo VAL_DIR: %CWDIR%\%%e
	call echo RESULTS_DIR: %CWDIR%\%%e\results
	
	echo --------
	echo Start evolution
	echo ....................
	
	call SET TRAIN_DIR=%CWDIR%\%%e
	call SET VAL_DIR=%CWDIR%\%%e
	call SET RESULTS_DIR=%CWDIR%\%%e\results
	
	REM %COMMANDLINE% batch --backend=halcon --runs=%RUNS% --train-data-dir=%TRAIN_DIR% --val-data-dir=%VAL_DIR% --generations=%GENERATIONS% --results-dir=%RESULTS_DIR%
	
	echo ....................
	echo Finished
	echo --------
)