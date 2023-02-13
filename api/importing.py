def import_one(path: str):
    """
    reads data from cgp optimization experiment
    and translates them to python model objects
    """
    print('Importing %s', path)
    # Analyzer
    #         |_0
    #            |_ AvgOffspringFit.json
    #            |_ AvgPopulationFit.json
    #            |_ AvgIndividualFit.json
    #            |_ individual_evaluation_log.json
    #            |_ loader_evaluation_log.json

    # Config
    #       |_ EvoluationStrategy.txt
    #       |_ Fitness.txt

    # Exception
    #          |_ 9917D8E0-20230202.txt

    # Grid
    #     |_0
    #        |_ append_pipeline.txt
    #        |_ grid.txt
    #        |_ pipeline.txt
    #        |_ vector.txt

    # Images
    #       |_0
    #          |_ 16.bmp
    #          |_ ...
    #          |_ ...
    #          |_ AppendPipelineConfusionMatrix.json
    #          |_ ConfusionMatrix.json
    #          |_ legend.txt
    return -1


def import_many(paths: []):
    """
    reads list of data containing
    cgp optimization experiments
    """
    for path in paths:
        print(import_one(path))
    print('Finished importing.')