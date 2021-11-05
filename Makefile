PY=python3 -u 
PY3=$(PY)

#HOSTNAME=$(shell hostname)
HOSTNAME=localhost
MONGO_PORT=27017
MONGO_DB=opm


clean_output:
	rm -r output/* || true
	pip freeze > output/requirements.txt
	git log -1 > output/git_log.txt

exp: experiment
experiment: clean_output
	# before running an experiment
	# you'll have to make a git commit
	$(PY) main.py train 

multi_experiment: clean_output
	# before running an experiment
	# you'll have to make a git commit
	$(PY) main.py multi

exp_dirty: clean_output
	$(PY) main.py train dirty

unittest:
	cd tests/unit && pytest

integration:
	cd tests/integration && pytest

# code documentation
doc:
	doxygen Doxyfile


###
# visualization & dashboards & GUIs
###

omni: omniboard
omniboard:
	@echo -ne "\n\n>\n> Open your browser: http://$(HOSTNAME):9000 \n>\n"
	omniboard -m $(HOSTNAME):$(MONGO_PORT):$(MONGO_DB)

tb: tensorboard
tensorboard:
	@echo -ne "\n\n>\n> Open your browser: http://$(HOSTNAME):6006 \n>\n"
	$(PY) -m tensorboard.main --logdir=~/ml_results --reload_interval 10


