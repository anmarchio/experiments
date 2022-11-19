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
call SET CWDIR=D:\evias_expmts

setlocal EnableDelayedExpansion 

REM AirCarbon
REM D:\evias_expmts\Aircarbon3\20210325_13h25_rov\training\images\t_80.jpg
REM D:\evias_expmts\Aircarbon3\20210325_13h25_rov\training\labels\t_80.jpg
REM D:\evias_expmts\Aircarbon3\20210325_13h25_rov\results
REM Severstal Steel
REM D:\evias_expmts\severstal-steel\train_images
REM D:\evias_expmts\severstal-steel\train_binary
REM D:\evias_expmts\severstal-steel\results
REM Magnetic-Tile-Defect\MT_Blowhole
REM D:\evias_expmts\Magnetic-Tile-Defect\MT_Blowhole\Imgs
REM D:\evias_expmts\Magnetic-Tile-Defect\MT_Blowhole\Labels
REM D:\evias_expmts\Magnetic-Tile-Defect\MT_Blowhole\Results

set expmnts_train[0]=Aircarbon3\20210325_13h25_rov\training\images\t_80.jpg 
set expmnts_val[0]=Aircarbon3\20210325_13h25_rov\training\labels\t_80.jpg 
set expmnts_res[0]=Aircarbon3\20210325_13h25_rov\results 
set expmnts_train[1]=severstal-steel\train_images 
set expmnts_val[1]=severstal-steel\train_binary 
set expmnts_res[1]=severstal-steel\results
set expmnts_train[2]=Magnetic-Tile-Defect\MT_Blowhole\Imgs
set expmnts_val[2]=Magnetic-Tile-Defect\MT_Blowhole\labels
set expmnts_res[2]=Magnetic-Tile-Defect\MT_Blowhole\results

REM ==========================================================
REM Run Experiments
REM ==========================================================
REM for %%e in (%expmnts%) do (
for /l %%i in (0 1 2) do (
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
		
	%COMMANDLINE% batch --backend=halcon --runs=%RUNS% --train-data-dir=%%TRAIN_DIR%% --val-data-dir=%%VAL_DIR%% --generations=%GENERATIONS% --results-dir=%%RESULTS_DIR%%
	
	echo ....................
	echo Finished
	echo --------
)