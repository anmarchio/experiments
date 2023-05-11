import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime

from database import Database
from models import Experiment, Run, Dataset, Analyzer, AvgOffspringFit, AvgPopulationFit, BestIndividualFit, \
    Individual, Pipeline, Item, Parameter, Node, Grid, Configuration, EvolutionStrategy, HalconFitnessConfiguration, \
    ExceptionLog, Vector, Element, ActiveGridNodes, InputGridNodes, OutputGridNodes, GridNode, GridNodeValue, \
    ConfusionMatrix, Image

# initialize database
DB = Database()


def exception_case(path):
    date_txt_path = os.path.join(path, "date.txt")
    overview_json_path = os.path.join(path, "overview.json")
    seed_txt_path = os.path.join(path, "seed.txt")
    source_json_path = os.path.join(path, "source.json")

    existing_files = [os.path.exists(x) for x in [date_txt_path, overview_json_path, seed_txt_path, source_json_path]]
    if [False, False, False, True] == existing_files or [False, False, False, False] == existing_files :

        for exc in os.listdir(os.path.join(path, "exceptions")):
            dataset = Dataset.create_from_json(
                source_json=source_json_path
            )
            DB.get_session().add(dataset)
            DB.get_session().commit()

            experiment = Experiment(
                created_at=datetime.strptime(os.path.split(path)[-1][0:12], '%Y%m%d%H%M'),
                dataset_id=dataset.dataset_id
            )
            DB.get_session().add(experiment)
            DB.get_session().commit()

            create_exception(path, experiment, exc)

        print("[WARNING] Exceptions found. Aborting.")
        return True


def create_experiment_and_run_metadata(path: str):
    print("\tReading metadata ...")

    date_txt_path = os.path.join(path, "date.txt")
    overview_json_path = os.path.join(path, "overview.json")
    seed_txt_path = os.path.join(path, "seed.txt")
    source_json_path = os.path.join(path, "source.json")

    dataset = Dataset.create_from_json(
        source_json=source_json_path
    )
    DB.get_session().add(dataset)
    DB.get_session().commit()

    experiment = Experiment.create_from_txt(
        date_txt=date_txt_path,
        seed_txt=seed_txt_path,
        dataset_id=dataset.dataset_id
    )
    DB.get_session().add(experiment)
    DB.get_session().commit()

    runs = Run.create_from_json(
        date_txt=date_txt_path,
        overview_json=overview_json_path,
        experiment=experiment
    )
    for r in runs:
        DB.get_session().add(r)

    DB.get_session().commit()

    return dataset, experiment, runs


def create_analyzer(path, experiment: Experiment, run_number):
    print("\tReading analyzers for run ", run_number)

    analyzer_files = {
        "AvgOffspringFit": os.path.join(path, "Analyzer", run_number, "AvgOffspringFit.json"),
        "AvgPopulationFit": os.path.join(path, "Analyzer", run_number, "AvgPopulationFit.json"),
        "BestIndividualFit": os.path.join(path, "Analyzer", run_number, "BestIndividualFit.json")
    }

    # Check if the all files exist in run_number
    if not all([os.path.exists(a[1]) for a in analyzer_files.items()]):
        # exit method if one is not present
        return 0

    run_entry = DB.get_session().query(Run).filter_by(
        experiment_id=experiment.experiment_id,
        number=int(run_number)
    ).first()
    analyzer = Analyzer(
        run_id=run_entry.run_id
    )
    DB.get_session().add(analyzer)
    DB.get_session().commit()

    run_entry.analyzer_id = analyzer.analyzer_id

    AvgOffspringFit.create_from_json(
        analyzer_files['AvgOffspringFit'],
        analyzer,
        DB.get_session()
    )
    DB.get_session().commit()

    AvgPopulationFit.create_from_json(
        analyzer_files['AvgPopulationFit'],
        analyzer,
        DB.get_session()
    )
    DB.get_session().commit()

    BestIndividualFit.create_from_json(
        analyzer_files['BestIndividualFit'],
        analyzer,
        DB.get_session()
    )
    DB.get_session().commit()


def create_individuals(path, experiment: Experiment, run_number):
    print("\tReading individuals for run ", run_number)

    individual_pipeline_files = {
        "individual_evaluation_log": os.path.join(path, "Analyzer", run_number, "individual_evaluation_log.json"),
        "loader_evaluation_log": os.path.join(path, "Analyzer", run_number, "loader_evaluation_log.json"),
        "append_pipeline": os.path.join(path, "Grid", run_number, "append_pipeline.txt")
    }

    # Check if the all files exist in run_number
    if not all([os.path.exists(a[1]) for a in individual_pipeline_files.items()]):
        # exit method if one is not present
        return 0

    run = DB.get_session().query(Run).filter_by(
        experiment_id=experiment.experiment_id,
        number=run_number
    ).first()

    grid = DB.get_session().query(Grid).filter_by(run_id=run.run_id).first()
    if grid is None:
        grid = Grid(
            run_id=run.run_id
        )
        DB.get_session().add(grid)
        DB.get_session().commit()

    f_appd_pipeline = open(individual_pipeline_files['append_pipeline'], "r")
    pipeline = Pipeline(
        digraph=f_appd_pipeline.read(),
        grid_id=grid.grid_id
    )
    DB.get_session().add(pipeline)
    DB.get_session().commit()

    f_evaluation = open(individual_pipeline_files['loader_evaluation_log'], "r")
    evaluation_loader_json = json.load(f_evaluation)
    for i in range(len(evaluation_loader_json)):
        run_element = evaluation_loader_json[str(i)]

        analyzer = DB.get_session().query(Analyzer).filter_by(
                run_id=run.run_id
            ).first()
        individual = Individual.create_from_json(run_element, analyzer, pipeline)
        DB.get_session().add(individual)
        DB.get_session().commit()

        pipeline_nodes = run_element[0]['Pipeline']
        for p_node in pipeline_nodes:
            node = Node(
                cgp_node_id=float(p_node['NodeID']),
                name=p_node['Name'],
                children=str(p_node['Children']),
                pipeline_id=pipeline.pipeline_id
            )
            DB.get_session().add(node)
            parameters = p_node['Parameters']
            for p in parameters:
                parameter = Parameter(
                    name=p['Name'],
                    value=p['Value'],
                    node_id=node.node_id
                )
                DB.get_session().add(parameter)
        DB.get_session().commit()

    print("\tReading ", individual_pipeline_files['individual_evaluation_log'])
    print("\t this might take a while ...")
    f_individual = open(individual_pipeline_files['individual_evaluation_log'], "r")
    individual_evaluation_json = json.load(f_individual)
    for j in range(len(individual_evaluation_json)):
        if str(j) not in individual_evaluation_json.keys():
            print("[ERROR] " + str(j) + " not in individual_evaluation_json.keys")
            continue
        items = individual_evaluation_json[str(j)]

        print("\t Reading items in run ", str(run_number), " for individual ", str(j)," of ", len(individual_evaluation_json), " ...")
        for ind_item in items:
            individual = DB.get_session().query(Individual).filter_by(
                analyzer_id=analyzer.analyzer_id,
                pipeline_id=pipeline.pipeline_id,
                individual_object_id=int(ind_item['IndividualId'])
            ).first()
            if individual is None:
                individual = Individual(
                    analyzer_id=analyzer.analyzer_id,
                    pipeline_id=pipeline.pipeline_id,
                    individual_object_id=int(ind_item['IndividualId'])
                    )
            item = Item(
                MCC=ind_item['FitnessValues']['MCC'],
                name=ind_item['Item'],
                individual_id=individual.individual_id
            )
            DB.get_session().add(item)
        DB.get_session().commit()
    print("\tDone reading ", individual_pipeline_files['loader_evaluation_log'])
    print("\t...")


def create_config(path, experiment: Experiment):
    print("\tReading config ...")

    config_files = {
        "EvolutionStrategy": os.path.join(path, "Config", "EvolutionStrategy.txt"),
        "Fitness": os.path.join(path, "Config", "Fitness.txt")
    }

    # Check if the all files exist in run_number
    if not all([os.path.exists(a[1]) for a in config_files.items()]):
        # exit method if one is not present
        return 0

    f_es = open(config_files['EvolutionStrategy'], "r")
    f_fit = open(config_files['Fitness'], "r")

    configuration = Configuration(
        experiment_id=experiment.experiment_id
    )

    evolution_strategy_xml = ET.fromstring(f_es.read())
    evolution_strategy = EvolutionStrategy(
        configuration_id=configuration.configuration_id,
        rho=int(evolution_strategy_xml.findall('Rho')[0].text),
        lambda_value=int(evolution_strategy_xml.findall('Lambda')[0].text),
        plus_selection=bool(evolution_strategy_xml.findall('PlusSelection')[0].text),
        mu=int(evolution_strategy_xml.findall('Mu')[0].text)
    )

    fitness_xml = ET.fromstring(f_fit.read())
    weights_xml = fitness_xml.findall('Weights')[0]
    weights = []
    for w in weights_xml:
        weights.append(float(w.text))
    fitness_functions_xml = fitness_xml.findall('FitnessFunctions')[0]
    fitness_function = []
    for ff in fitness_functions_xml:
        fitness_function.append(ff.text)

    halcon_fitness_config = HalconFitnessConfiguration(
        configuration_id=configuration.configuration_id,
        region_score_weight=int(fitness_xml.findall('RegionScoreWeight')[0].text),
        artifact_score_weight=int(fitness_xml.findall('ArtifactScoreWeight')[0].text),
        fitness_score_weight=int(fitness_xml.findall('FitnessScoreWeight')[0].text),
        maximization=bool(fitness_xml.findall('Maximization')[0].text),
        excess_region_handling=fitness_xml.findall('ExcessRegionHandling')[0].text,
        region_count_threshold=bool(fitness_xml.findall('RegionCountThreshold')[0].attrib),
        execution_time_threshold=bool(fitness_xml.findall('ExecutionTimeThreshold')[0].attrib),
        use_execution_time_fitness_penalty=bool(fitness_xml.findall('UseExecutionTimeFitnessPenalty')[0].text),
        execution_time_function_time_scale_factor=int(
            fitness_xml.findall('ExecutionTimeFunctionScaleFactor')[0].text),
        pixel_percentage_threshold=float(fitness_xml.findall('PixelPercentageThreshold')[0].text),
        filename=fitness_xml.findall('Filename')[0].text
    )

    DB.get_session().add(configuration)
    DB.get_session().add(evolution_strategy)
    DB.get_session().add(halcon_fitness_config)
    # Commit entries
    DB.get_session().commit()


def create_exception(path, experiment, exception):
    print("\tReading exception ", exception)

    if not os.path.exists(os.path.join(path, "exceptions", exception)):
        return 0

    f = open(os.path.join(path, "exceptions", exception), "r")
    exception_log = ExceptionLog(
        experiment_id=experiment.experiment_id,
        identifier=exception.split(".")[0],
        content=f.read()
    )
    DB.get_session().add(exception_log)
    DB.get_session().commit()


def create_grid_nodes(grid, lines):
    """
    Read and create all grid nodes
    from grid.txt
    """
    print("\tReading grid and grid_nodes ")

    active_grid_nodes = ActiveGridNodes(
        grid_id=grid.grid_id
    )
    DB.get_session().add(active_grid_nodes)
    DB.get_session().commit()

    input_grid_nodes = InputGridNodes(
        grid_id=grid.grid_id
    )
    DB.get_session().add(input_grid_nodes)
    DB.get_session().commit()

    output_grid_nodes = OutputGridNodes(
        grid_id=grid.grid_id
    )
    DB.get_session().add(output_grid_nodes)
    DB.get_session().commit()

    # Inputs:
    inputs = lines[4].split(" ")[1:-1]
    # Outputs:
    outputs = lines[15].split(" ")[1:-1]
    # active Nodes:
    active_nodes = lines[16].split(" ")[3:-1]

    # grid nodes:
    grid_nodes = []
    for i in range(4, 14):
        grid_nodes = grid_nodes + lines[i].split("|")

    for node in grid_nodes:
        if len(node) < 2:
            continue

        if node[0:3] == " {{" or node[0:2] == "{{":
            node = re.search(r"{{([A-Za-z0-9,():.\s-]+)}}", node).group(1)

        node_id_index = int(node.split(":")[0])
        input_node_index = int(node.split(":")[2].split(" ")[1])

        operator_name = re.search(r"(\s[A-Za-z0-9]+\()", node.split(":")[2]).group(1)
        operator_name = operator_name[1:-1]

        grid_node = GridNode(
            grid_id=grid.grid_id,
            node_id=node_id_index,
            input=input_node_index,
            name=operator_name
        )
        if node_id_index in inputs:
            grid_node.input_grid_nodes_id = input_grid_nodes.input_grid_nodes_id
        if node_id_index in active_nodes:
            grid_node.active_grid_nodes_id = active_grid_nodes.active_grid_nodes_id
        if node_id_index in outputs:
            grid_node.output_grid_nodes_id = output_grid_nodes.output_grid_nodes_id
        DB.get_session().add(grid_node)
        DB.get_session().commit()

        # Add node values
        values = re.findall(r"\([0-9.,-E]+\)", node.split(":")[2])[0]
        for v in values[1:-1].split(","):
            grid_node_value = GridNodeValue(
                grid_node_id=grid_node.grid_node_id,
                value=float(v),
            )
            DB.get_session().add(grid_node_value)

    DB.get_session().commit()


def create_grid_vector(grid, grid_files):
    print("\tReading grid vector ...")

    vector = Vector(
        grid_id=grid.grid_id
    )
    DB.get_session().add(vector)
    DB.get_session().commit()

    f_vector = open(grid_files['vector'], "r")
    vector_values = f_vector.read().split(",")
    for val in vector_values:
        element = Element(
            vector_id=vector.vector_id,
            value=float(val)
        )
        DB.get_session().add(element)
    DB.get_session().commit()


def create_grid(path, experiment: Experiment, run_number):
    print("\tReading grid for run ", run_number)

    grid_files = {
        "append_pipeline": os.path.join(path, "Grid", run_number, "append_pipeline.txt"),
        "grid": os.path.join(path, "Grid", run_number, "grid.txt"),
        "pipeline": os.path.join(path, "Grid", run_number, "pipeline.txt"),
        "vector": os.path.join(path, "Grid", run_number, "vector.txt")
    }

    # Check if the all files exist in run_number
    if not all([os.path.exists(g[1]) for g in grid_files.items()]):
        # exit method if one is not present
        return 0

    run = DB.get_session().query(Run).filter_by(
        experiment_id = experiment.experiment_id,
        number=int(run_number)).first()

    f_grid = open(grid_files['grid'], "r")
    lines = f_grid.read().splitlines()
    # check whether grid has been created before
    grid = DB.get_session().query(Grid).filter_by(
        run_id=run.run_id).first()

    if grid is None:
        grid = Grid(
            hash_code=int(lines[0][10:19]),
            time=datetime.strptime(lines[1][6:27], '%m/%d/%Y %I:%M:%S %p'),
            number_of_inputs=int(lines[3][7:-1]),
            run_id=run.run_id
        )
        DB.get_session().add(grid)
        DB.get_session().commit()
    create_grid_nodes(grid, lines)
    create_grid_vector(grid, grid_files)


def create_images(path, experiment: Experiment, run_number):
    print("\tReading images for run ", run_number)

    images_files = {
        "AppendPipelineConfusionMatrix": os.path.join(path, "Images", run_number, "AppendPipelineConfusionMatrix.json"),
        "ConfusionMatrix": os.path.join(path, "Images", run_number, "ConfusionMatrix.json"),
        "legend": os.path.join(path, "Images", run_number, "legend.txt"),
    }

    # Check if the all files exist in run_number
    if not all([os.path.exists(img[1]) for img in images_files.items()]):
        # exit method if one is not present
        return 0

    run = DB.get_session().query(Run).filter_by(
            experiment_id=experiment.experiment_id,
            number=int(run_number)
        ).first()
    f_images=open(images_files['AppendPipelineConfusionMatrix'], "r")
    images_json = json.load(f_images)
    for img in images_json:
        confusion_matrix = ConfusionMatrix(
            true_positives=int(images_json[img]['true positives']),
            true_negatives=int(images_json[img]['true negatives']),
            false_positives=int(images_json[img]['false positives']),
            false_negatives=int(images_json[img]['false negatives']),
            MCC=float(images_json[img]['MCC']),
            height=int(images_json[img]['height']),
            width=int(images_json[img]['width']),
            size_total=int(images_json[img]['size total'])
        )
        image = Image(
            run_id=run.run_id,
            confusion_matrix_id=confusion_matrix.confusion_matrix_id,
            filename=img
        )
        confusion_matrix.image_id = image.image_id
        DB.get_session().add(image)
        DB.get_session().add(confusion_matrix)

    DB.get_session().commit()


def import_one(path: str):
    """
    reads data from cgp optimization experiment
    and translates them to python model objects
    """
    print('Importing ', path)
    #
    # Exceptions only
    #
    if exception_case(path):
        return 0
    # ...
    #    |_ date.txt
    #    |_ overview.json
    #    |_ seed.txt
    #    |_ source.json
    #    |_ validation.json
    dataset, experiment, runs = create_experiment_and_run_metadata(path)
    #
    # Analyzer
    #         |_0
    #            |_ AvgOffspringFit.json
    #            |_ AvgPopulationFit.json
    #            |_ BestIndividualFit.json
    #            |_ individual_evaluation_log.json
    #            |_ loader_evaluation_log.json
    for run_number in os.listdir(os.path.join(path, "Analyzer")):
        create_analyzer(path, experiment, run_number)
        create_individuals(path, experiment, run_number)
    #
    # Config
    #       |_ EvoluationStrategy.txt
    #       |_ Fitness.txt
    create_config(path, experiment)
    #
    # Exception
    #          |_ 9917D8E0-20230202.txt
    for exception in os.listdir(os.path.join(path, "exceptions")):
        create_exception(path, experiment, exception)
    #
    # Grid
    #     |_0
    #        |_ append_pipeline.txt
    #        |_ grid.txt
    #        |_ pipeline.txt
    #        |_ vector.txt
    #
    for run_number in os.listdir(os.path.join(path, "Grid")):
        create_grid(path, experiment, run_number)
    # Images
    #       |_0
    #          |_ 16.bmp
    #          |_ ...
    #          |_ ...
    #          |_ AppendPipelineConfusionMatrix.json
    #          |_ ConfusionMatrix.json
    #          |_ legend.txt
    #
    for run_number in os.listdir(os.path.join(path, "Images")):
        create_images(path, experiment, run_number)

    print('<' * 6 + 'Done.' + '>' * 6)
    return 0


def import_many(path):
    """
    reads list of data containing
    cgp optimization experiments
    """
    i = 0
    for dirname in os.listdir(path):
        progress = int(i / 20) * 20
        print("|" + "=" * progress + "-" * (20 - progress) + "|")
        print(import_one(os.path.join(path,dirname)))
        i += 1
    print('Finished importing.')
