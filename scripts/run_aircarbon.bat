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
set expmnts=AirCarbon2\160919_SGL\Blende5_6_1800mA_rov AirCarbon2\160919_SGL\Blende5_6_1800mA_rov\t_2.jpg AirCarbon3\training AirCarbon3

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