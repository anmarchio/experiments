"""! @brief Module to load individual configs."""

import os
from collections import OrderedDict
import hiyapyco as hco

CONFIG_ROOT = "./config"
CONFIG_BASE = "{}/base.yml".format(CONFIG_ROOT)

MODE_TRAIN = "train"
MODE_VALIDATION = "validation"
MODE_TEST = "test"
MODE_MULTI = "multi"

MODES = [MODE_TRAIN, MODE_VALIDATION, MODE_TEST, MODE_MULTI]


class Config:
    """
    Class to create all needed configs (base, train, validation).

    Supports use of multiple different configs.
    """

    def __init__(self):
        """Initialize all configs in config folder."""
        self._conf_path_train = "{}/train.yml".format(CONFIG_ROOT)
        self._conf_path_validation = "{}/validation.yml".format(CONFIG_ROOT)
        self._conf_path_test = "{}/test.yml".format(CONFIG_ROOT)
        self._conf_path_list_multi = self._get_conf_path_multi()
        self._multi_config = self._generate_multi_configs()
        self.amount_of_configs = len(self._multi_config)
        self._configs_dict = self._generate_single_configs()

    @classmethod
    def _get_conf_path_multi(cls) -> list:
        """
        Get the path of all configurations in folder multi as a list.

        :return: list of paths of multi-configuration
        """
        conf_path_list = []
        path = os.getcwd() + "/config/multi/"
        if os.path.exists(path):
            for entry in os.listdir(path):
                conf_path_list.append("{}/multi/{}".format(CONFIG_ROOT, entry))
        return conf_path_list

    def get_multi_configs(self):
        """
        Return the next multi_config and remove it from multi config list.

        If the list is empty it return None.
        :return: dictionary of available configs
        """
        if self._multi_config:
            self._configs_dict = self._multi_config.pop()
            return self._configs_dict

        return None

    def get_specific_config(self, mode: str = "train") -> OrderedDict:
        """
        Return the config for the provided mode.

        If no mode is provided it returns the base config with mode train.
        :param mode: desired mode (train, test, validation)
        :return: config in given mode
        """
        if mode == MODE_TRAIN:
            self._configs_dict["base_config"]
        elif mode == MODE_TEST:
            return self._configs_dict["test_config"]
        elif mode == MODE_VALIDATION:
            return self._configs_dict["val_config"]

        return self._configs_dict["base_config"]

    def _generate_single_configs(self):
        """
        Generate configs for single config use.

        :return: dictionary with available configs
        """
        train_config, test_config, val_config = self._generate_all_configs(
            self._conf_path_train
        )

        # print if debug is set to True
        if train_config["debug"]["config"]:
            print("config", train_config)

        return {
            "base_config": train_config,
            "test_config": test_config,
            "val_config": val_config,
        }

    def _generate_multi_configs(self) -> list:
        """
        Generate configs for multi config use.

        :return: dictionary with available configs
        """
        config_list = []
        for conf_entry in self._conf_path_list_multi:
            train_config, test_config, val_config = self._generate_all_configs(
                conf_entry
            )

            # print if debug is set to True
            if train_config["debug"]["config"]:
                print(
                    "--------------\nConfig ",
                    train_config["config_name"],
                    ":\n",
                    train_config,
                )

            config_list.append(
                {
                    "base_config": train_config,
                    "test_config": test_config,
                    "val_config": val_config,
                }
            )

        return config_list

    def _generate_all_configs(self, additional_path):
        """
        Generate all available configs (train, test, validation).

        If base is used with GPU, it adds the GPU config.
        :param additional_path:
        :return:
        """
        train_config = hco.load(
            CONFIG_BASE,
            additional_path,
            method=hco.METHOD_MERGE,
            interpolate=True,
            failonmissingfiles=True,
        )

        test_config = hco.load(
            CONFIG_BASE,
            additional_path,
            self._conf_path_test,
            method=hco.METHOD_MERGE,
            interpolate=True,
            failonmissingfiles=True,
        )

        val_config = hco.load(
            CONFIG_BASE,
            additional_path,
            self._conf_path_validation,
            method=hco.METHOD_MERGE,
            interpolate=True,
            failonmissingfiles=True,
        )

        # patch with current absolute path
        base_path = os.getcwd()
        train_config["base_path"] = base_path
        test_config["base_path"] = base_path
        val_config["base_path"] = base_path

        # add base config name
        train_config["base_config_name"] = additional_path.split("/")[-1]

        if train_config["set_seeds"]:
            train_config["seed"] = train_config["random_seed"]

        if test_config["set_seeds"]:
            test_config["seed"] = test_config["random_seed"]

        if val_config["set_seeds"]:
            val_config["seed"] = val_config["random_seed"]

        return train_config, test_config, val_config
