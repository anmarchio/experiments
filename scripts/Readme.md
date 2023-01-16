
# Experiment Scripting

This folder contains scripts to manage and run the experiments around the CGP based algorithm.

## Quick start

### Ubuntu workstation

#### Configurations

Make sure all variables are set correctly:
* `export LD_LIBRARY_PATH=":/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64:/opt/halcon/lib/x64-linux"`
* tbd
* tbd

##### Start Script
In order to run the script on linux, checkout this repository and `cd` to the according loaction:

```
cd /mnt/sdc1/mara/experiments/scripts/
```

The `.sh` file is the designated linux script. It runs a docker container and loads the according files.
In order to follow the current execution state, you should run it detached from the shell (using `nohup`). We need a file to be written to the current drive, therefore execute it as follows:

```
nohup ./run_cgp_experiments_linux.sh > output.txt
```

The shell will no be written to the local file `output.txt` which you can easily access using `nano` or `vim`. 

### Windows

In order to execute the experiments on windows, you just need to checkout the repository, compile the application and make sure to put in a decent drive location.
The the `.bat` script for the correct path strings. Then execute the script in `cmd.exe` as follows:

```
run_cgp_experiments.bat
```

The bash messages will be written to the cmd windows, the results are written to a local folder `results/...`.
