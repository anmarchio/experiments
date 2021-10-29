"""! @brief Main script to start experiments."""

import sys
import subprocess
import urllib.parse
import git
from pymongo import MongoClient
from sacred.observers import MongoObserver
from experiment import ex, global_config
from util.config import MODE_MULTI, MODE_TRAIN, MODE_VALIDATION


def init_mongo(config):
    """
    Initialize mongo configuration for either local mongo db or remote mongo db.

    :param config: Configuration of system
    :return:    use_mongo: True if data should be saved to mongo
                use_remote: True if data should be saved to remote db
                mongo_url: url if local mongo db if used
                mongo_db: name of the mongo db
                client: client connection for remote mongo db
    """
    use_mongo = config["experiment"]["mongo"]["enable"]
    mongo_url = config["experiment"]["mongo"]["url"]
    mongo_db = config["experiment"]["mongo"]["db"]
    username = urllib.parse.quote_plus(config["experiment"]["mongo"]["username"])
    password = urllib.parse.quote_plus(config["experiment"]["mongo"]["password"])
    use_remote = config["experiment"]["mongo"]["use_remote"]
    ip_address = config["experiment"]["mongo"]["ip"]
    client = MongoClient(
        "mongodb://%s:%s@%s/%s?authSource=admin"
        % (username, password, ip_address, mongo_db)
    )
    return use_mongo, use_remote, mongo_url, mongo_db, client


modes = {
    "multi": MODE_MULTI,
    "train": MODE_TRAIN,
    "val": MODE_VALIDATION,
}


def main(mode: str = MODE_TRAIN):
    """
    Execute a experiment with the possibility to run multiple consecutive experiments.

    1. Called by using a make command
            make multi_exp_dirty: executes all configs in ./config/multi consecutively (order of execution can vary)
            make exp_dirty: executes train config
            make val_exp_dirty: executes val config
    2. If you want to change the experiments name, switch to experiment.py and change exp_name in line 24
    """
    # get base config and init mongo with it
    base_config = global_config.get_specific_config()
    use_mongo, use_remote, mongo_url, mongo_db, mongo_client = init_mongo(base_config)

    if use_mongo:
        if use_remote:
            ex.observers.append(
                MongoObserver.create(client=mongo_client, db_name=mongo_db)
            )
        else:
            ex.observers.append(MongoObserver.create(url=mongo_url, db_name=mongo_db))

    print(
        "======================================================================\n",
        "Running experiment with mode: ",
        mode,
        "\n======================================================================",
    )

    if mode == MODE_MULTI:
        print(
            "Running ", global_config.amount_of_configs, " Experiments consecutively!"
        )

        while global_config.get_multi_configs() is not None:
            # clear output directory
            try:
                subprocess.Popen(
                    "make clean_output", shell=True, stderr=subprocess.STDOUT
                )
            except Exception:
                print("Error while trying to clean output directory")

            # get config
            base_config = global_config.get_specific_config()
            print(
                "======================================================================\n",
                "Execution with config: ",
                base_config["config_name"],
                " Mode: ",
                base_config["mode"],
                "\n======================================================================",
            )

            # add config to experiment
            ex.add_config(base_config)

            # run experiment
            ex.run()

    elif mode == MODE_VALIDATION:
        # get validation config
        val_config = global_config.get_specific_config("validation")

        # add config to experiment
        ex.add_config(val_config)

        # run experiment
        ex.run()
    else:  # currently only mode train
        # add config to experiment
        ex.add_config(base_config)

        # run experiment
        ex.run()


if __name__ == "__main__":
    """
    Start main function and aboard if repository is dirty.

    Allowed modes: multi, train, val
    """
    exec_mode = modes[sys.argv[1]]

    # Make run reproducible. So check if all files are commited.
    repo = git.Repo("")
    if repo.is_dirty():
        if len(sys.argv) <= 2:
            raise RuntimeError(
                "EnforceClean: Uncommited changes in the current repository."
            )
        if not sys.argv[2] == "dirty":
            raise RuntimeError(
                "EnforceClean: Uncommited changes in the current repository."
            )

    # run main
    main(mode=exec_mode)
