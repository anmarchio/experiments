from api.database import Database
from api.models import Dataset
from param_tuning.dataset_pipeline_analysis import read_db_and_apply_algorithms_to_hdev
from pipeline_retrieval.cross_application_on_all_datasets import read_db_and_cross_apply_hdev_pipelines


def selection_cross_apply_pipelines_on_all_datasets(db):
    """
    4 -- Cross-apply cgp pipelines on all datasets (ca. 900 runs)
    """
    print("!!! ATTENTION: This part has not been tested properly !!!")

    print("Do you want to continue? y/n")
    print("\n")
    yesno = input("Selection: ")
    if yesno == "y":
        experiment_datasets = Dataset.get_pipeline_by_each_dataset(db.get_session())

        read_db_and_cross_apply_hdev_pipelines(experiment_datasets)
    else:
        print("Aborted.")


def main():
    print("CGP Pipeline Cross Application")
    print("-" * 30)

    selection = input("Start the CGP pipeline cross application? (1 = yes)")

    # Exit program
    if selection == "0":
        print("Exiting ...")
        return 0

    # Get database object from api.database
    db = Database()

    # 4 -- Cross-apply cgp pipelines on all datasets (ca. 900 runs)
    if selection == "1":
        selection_cross_apply_pipelines_on_all_datasets(db)


if __name__ == "__main__":
    main()
