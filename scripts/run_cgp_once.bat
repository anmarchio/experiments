call SET COMMANDLINE=D:\dev\github\optimization\Optimization.Commandline\bin\Debug\Optimization.Commandline.exe

call SET RUNS=1
call SET GENERATIONS=5
call SET CWDIR=D:\evias_expmts

call echo RUNS: %RUNS%
call echo GENERATIONS: %GENERATIONS%
	
call SET TRAIN_DIR=%%CWDIR%%\MVTecAnomalyDetection\cable_missing_train
call SET VAL_DIR=%%CWDIR%%\MVTecAnomalyDetection\cable_missing_val
call SET RESULTS_DIR=%%CWDIR%%\MVTecAnomalyDetection\results
	
REM call echo TRAIN_DIR: %CWDIR%\%%expmnts_train[%%i]%%
REM call echo VAL_DIR: %CWDIR%\%%expmnts_val[%%i]%%
REM call echo RESULTS_DIR: %CWDIR%\%%expmnts_res[%%i]%%
call echo train-data-dir: %%TRAIN_DIR%%
call echo val-data-dir: %%VAL_DIR%%
call echo results-dir: %%RESULTS_DIR%%
		
echo --------
echo Start evolution
echo ....................

echo %TRAIN_DIR%
echo %VAL_DIR%
echo %COMMANDLINE% batch --backend=halcon --runs=%RUNS% --train-data-dir=%TRAIN_DIR% --val-data-dir=%VAL_DIR% --generations=%GENERATIONS%
REM call %COMMANDLINE% batch --backend=halcon --runs=%RUNS% --train-data-dir=%%TRAIN_DIR%% --val-data-dir=%%VAL_DIR%% --generations=%GENERATIONS%
REM  --results-dir=%%RESULTS_DIR%%
	
echo ....................
echo Finished
echo --------