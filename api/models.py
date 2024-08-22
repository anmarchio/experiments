import enum
import json
import os
import re
from datetime import datetime

import numpy as np
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class Experiment(Base):
    __tablename__ = "experiment"
    experiment_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    seed = Column(Integer)
    dataset_id = Column(
        Integer,
        ForeignKey("dataset.dataset_id")
    )

    @staticmethod
    def create_from_txt(
            date_txt: str,
            seed_txt: str,
            dataset_id: int):
        date = None
        with open(date_txt, "r") as f_date:
            tmp = f_date.readline()[7:-1]
            try:
                date = datetime.strptime(tmp, '%m/%d/%Y %I:%M:%S %p')
            except:
                print("date not us standard")
                try:
                    date = datetime.strptime(tmp, '%d.%m.%Y %H:%M:%S')
                except:
                    print("date not european")
                    try:
                        date_path = os.path.normpath(date_txt).split(os.path.sep)
                        date = datetime.strptime(date_path[-2], '%Y%m%d%H%M')
                    except:
                        print("folder not working")
                    finally:
                        date = datetime.utcnow()
        seed_value = 0
        with open(seed_txt, "r") as f_seed:
            seed_value = int(f_seed.read())
        experiment = Experiment(
            created_at=date,
            seed=seed_value,
            dataset_id=dataset_id
        )
        return experiment


class Run(Base):
    __tablename__ = "run"
    run_id = Column(Integer, primary_key=True)
    experiment_id = Column(
        Integer,
        ForeignKey("experiment.experiment_id")
    )
    analyzer_id = Column(
        Integer,
        ForeignKey("analyzer.analyzer_id")
    )
    started_at = Column(DateTime, default=datetime.utcnow())
    number = Column(Integer)
    legend = Column(String)

    @staticmethod
    def create_from_json(date_txt,
                         overview_json,
                         experiment):
        run_number = 0
        date = None
        runs = []
        with open(date_txt, "r") as f_date:
            for line in f_date.readlines():
                if "Iteration" in line:
                    run_number = int(line[10:13])
                    tmp = f_date.readline()[7:-1]
                    try:
                        date = datetime.strptime(tmp, '%m/%d/%Y %I:%M:%S %p')
                    except:
                        print("date not us standard")
                        try:
                            date = datetime.strptime(tmp, '%d.%m.%Y %H:%M:%S')
                        except:
                            print("date not european")
                            try:
                                date_path = os.path.normpath(date_txt).split(os.path.sep)
                                date = datetime.strptime(date_path[-2], '%Y%m%d%H%M')
                            except:
                                print("folder not working")
                            finally:
                                date = datetime.utcnow()
                    run = Run(
                        experiment_id=experiment.experiment_id,
                        started_at=date,
                        number=run_number,
                        legend=""
                    )
                    runs.append(run)
        return runs


class Configuration(Base):
    __tablename__ = "configuration"
    configuration_id = Column(Integer, primary_key=True)
    experiment_id = Column(
        Integer,
        ForeignKey("experiment.experiment_id")
    )
    evolution_strategy_id = Column(
        Integer,
        ForeignKey("evolution_strategy.evolution_strategy_id")
    )
    halcon_fitness_configuration_id = Column(
        Integer,
        ForeignKey("halcon_fitness_configuration.halcon_fitness_configuration_id")
    )


class Dataset(Base):
    __tablename__ = "dataset"
    dataset_id = Column(Integer, primary_key=True)
    name = Column(String)
    source_directory = Column(String)
    validation_directory = Column(String)
    description = Column(String)
    url = Column(String)

    @staticmethod
    def create_from_json(source_json: str):
        name_str = "unknown"
        src_dir = "unknown"
        val_dir = "unknown"
        if os.path.exists(source_json):
            with open(source_json) as f:
                try:
                    jsondata = json.load(f)
                    name_str = jsondata[0]['trainingDataDirectory'].split("\\")[-1]
                    src_dir = jsondata[0]['trainingDataDirectory']
                    val_dir = jsondata[0]['validationDataDirectory']
                except Exception:
                    print("Bad json format. Try regex ...")
                    f2 = open(source_json, "r")
                    txt = f2.read()
                    src_val_path = re.findall(r'"[A-Z]:\\[a-zA-Z0-9-_\\:.]*"', txt)
                    if src_val_path is None:
                        print("Regex failed. Set to unknown ...")
                    else:
                        name_str = src_val_path[0].split("\\")[-1]
                        src_dir = src_val_path[0]
                        val_dir = src_val_path[1]

        dataset = Dataset(
            name=name_str,
            source_directory=src_dir,
            validation_directory=val_dir,
            description="",
            url=""
        )
        return dataset

    @staticmethod
    def _get_experiment_runs(session, experiments):
        exp_runs = []

        for exp in experiments:
            tmp_runs = session.query(Run).filter_by(experiment_id=exp.experiment_id).all()
            if len(tmp_runs) > 0:
                exp_runs.append(tmp_runs)

        return exp_runs

    @staticmethod
    def _get_best_ind_fit(session, exp_runs):
        best_ind_fit = []
        for expr in exp_runs:
            for r in expr:
                if r is not None:
                    analyzer = session.query(Analyzer).filter_by(run_id=r.run_id).first()
                    best_ind_fit.append(
                        session.query(BestIndividualFit).filter_by(analyzer_id=analyzer.analyzer_id).all())
        return best_ind_fit

    @staticmethod
    def _get_mean_pipelines(session, exp_runs, min_generations: int = None, max_generations: int = None):
        best_ind_fit = []
        for expr in exp_runs:
            for r in expr:
                if r is not None:
                    analyzer = session.query(Analyzer).filter_by(run_id=r.run_id).first()

                    if min_generations is None or \
                            max_generations is None or \
                            min_generations < \
                            session.query(BestIndividualFit).filter_by(analyzer_id=analyzer.analyzer_id).count() \
                            < max_generations:
                        best_ind_fit.append(
                            session.query(BestIndividualFit).filter_by(analyzer_id=analyzer.analyzer_id).all())

        best_pipelines = []
        if len(best_ind_fit) > 0:
            # Find pipeline closes to mean MCC fitness
            mcc_mean = np.mean([fit.best_individual_fitness for fit in best_ind_fit[0]])

            dist = abs(best_ind_fit[0][0].best_individual_fitness - mcc_mean)
            dist_index = 0
            for i in range(1, len(best_ind_fit[0])):
                if abs(best_ind_fit[0][i].best_individual_fitness - mcc_mean) < dist:
                    dist_index = i
                    dist = abs(best_ind_fit[0][i].best_individual_fitness - mcc_mean)

            i = 0
            for expr in exp_runs:
                for r in expr:
                    if r is not None:
                        if i == dist_index:
                            grid = session.query(Grid).filter_by(run_id=r.run_id).first()
                            best_pipelines.append(
                                session.query(Pipeline).filter_by(grid_id=grid.grid_id).all())
                        i += 1

        return best_pipelines

    @staticmethod
    def _get_best_pipelines(session, exp_runs):
        best_pipelines = []
        for expr in exp_runs:
            for r in expr:
                if r is not None:
                    grid = session.query(Grid).filter_by(run_id=r.run_id).first()
                    best_pipelines.append(
                        session.query(Pipeline).filter_by(grid_id=grid.grid_id).all())

        return best_pipelines

    @staticmethod
    def _get_datasets_pipelines_lists(session: Session, datasets: [], min_generations: int = None,
                                      max_generations: int = None):
        datasets_pipeline_lists = {}
        for ds in datasets:
            experiments = session.query(Experiment).filter_by(dataset_id=ds.dataset_id).all()

            exp_runs = Dataset._get_experiment_runs(session, experiments)

            runs_created_at = []
            if len(exp_runs) > 0:
                runs_created_at = [r.started_at for r in exp_runs[0]]

            # Get pipelines of mean fitness individuals
            best_pipelines = []
            if min_generations is not None and max_generations is not None:
                best_pipelines = Dataset._get_mean_pipelines(session, exp_runs, min_generations, max_generations)

            datasets_pipeline_lists[ds.dataset_id] = {
                "id": ds.dataset_id,
                "name": ds.name,
                "source": ds.source_directory,
                "runs_created_at": runs_created_at,
                "best_pipelines": best_pipelines
            }

        return datasets_pipeline_lists

    @staticmethod
    def get_runs_fitness_by_each_dataset(session: Session):
        # Experiments by dataset
        datasets = session.query(Dataset).all()
        datasets_fitness_lists = {}

        for ds in datasets:
            experiments = session.query(Experiment).filter_by(dataset_id=ds.dataset_id).all()

            exp_runs = Dataset._get_experiment_runs(session, experiments)

            best_ind_fit = Dataset._get_best_ind_fit(session, exp_runs)

            # Line Header
            # Dataset   | Experiment date   | list(run)
            datasets_fitness_lists[ds.dataset_id] = {
                "id": ds.dataset_id,
                "name": ds.name,
                "source": ds.source_directory,
                "values": best_ind_fit
            }
        return datasets_fitness_lists

    @staticmethod
    def get_pipeline_by_each_dataset(session: Session):
        # Experiments by dataset
        datasets = session.query(Dataset).all()

        return Dataset._get_datasets_pipelines_lists(session, datasets)

    @staticmethod
    def get_runs_fitness_by_grouped_dataset(session: Session, min_generations: int = None,
                                            max_generations: int = None):
        # Experiments by dataset
        datasets = session.query(Dataset).group_by(Dataset.source_directory).all()
        datasets_fitness_lists = {}

        for ds in datasets:
            same_source_directory = session.query(Dataset).filter_by(source_directory=ds.source_directory).all()
            experiments = session.query(Experiment).filter(
                Experiment.dataset_id.in_(([x.dataset_id for x in same_source_directory]))).all()

            exp_runs = Dataset._get_experiment_runs(session, experiments)

            best_ind_fit = []
            for expr in exp_runs:
                for r in expr:
                    if r is not None:
                        analyzer = session.query(Analyzer).filter_by(run_id=r.run_id).first()
                        """
                        Check here whether the number of individual fitness values (= generations) 
                        is either
                        * min_generations OR max_generations is None
                        * or is within min_generations & max_generations
                        """
                        if min_generations is None or \
                                max_generations is None or \
                                min_generations < \
                                session.query(BestIndividualFit).filter_by(analyzer_id=analyzer.analyzer_id).count() \
                                < max_generations:
                            best_ind_fit.append(
                                session.query(BestIndividualFit).filter_by(analyzer_id=analyzer.analyzer_id).all())
            number_of_images = 0
            if len(exp_runs) > 0 and exp_runs[0][0] is not None:
                number_of_images = session.query(Image).filter_by(run_id=exp_runs[0][0].run_id).count()
            # Line Header
            # Dataset   | Experiment date   | list(run)

            datasets_fitness_lists[ds.dataset_id] = {
                "id": ds.dataset_id,
                "name": ds.name,
                "source": ds.source_directory,
                "values": best_ind_fit,
                "number_of_images": number_of_images
            }
        return datasets_fitness_lists

    """
    @staticmethod
    def get_pipeline_fitness_by_grouped_dataset(
            session: Session,
            min_generations: int = None,
            max_generations: int = None):
        # Experiments by dataset

        =>
        => Here we want to get pipelines by runs ...
        =>

        datasets = session.query(Dataset).group_by(Dataset.source_directory).all()
        datasets_pipelines_lists = {}

        datasets_pipelines_lists = Dataset._get_datasets_pipelines_lists(
            session,
            datasets,
            min_generations,
            max_generations)

        return datasets_pipelines_lists
    """


class Analyzer(Base):
    __tablename__ = "analyzer"
    analyzer_id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("run.run_id"))


class BestIndividualFit(Base):
    __tablename__ = "best_individual_fit"
    best_individual_fit_id = Column(Integer, primary_key=True)
    analyzer_id = Column(Integer, ForeignKey("analyzer.analyzer_id"))
    generation = Column(Integer)
    best_individual_fitness = Column(Float)

    @staticmethod
    def create_from_json(
            path,
            analyzer,
            session):
        with open(path) as f:
            fit_json = json.load(f)
            for entry in fit_json:
                best_individual_fit = BestIndividualFit(
                    generation=int(entry['Generation']),
                    best_individual_fitness=float(entry['BestIndividualFitness'])
                )
                best_individual_fit.analyzer_id = analyzer.analyzer_id
                session.add(best_individual_fit)


class AvgPopulationFit(Base):
    __tablename__ = "avg_population_fit"
    avg_population_fit_id = Column(Integer, primary_key=True)
    analyzer_id = Column(Integer, ForeignKey("analyzer.analyzer_id"))
    generation = Column(Integer)
    average_population_fitness = Column(Float)

    @staticmethod
    def create_from_json(
            path,
            analyzer,
            session):
        with open(path) as f:
            fit_json = json.load(f)
            for entry in fit_json:
                avg_population_fit = AvgPopulationFit(
                    generation=int(entry['Generation']),
                    average_population_fitness=float(entry['AveragePopulationFitness'])
                )
                avg_population_fit.analyzer_id = analyzer.analyzer_id
                session.add(avg_population_fit)


class AvgOffspringFit(Base):
    __tablename__ = "avg_offspring_fit"
    avg_offspring_fit_id = Column(Integer, primary_key=True)
    analyzer_id = Column(Integer, ForeignKey("analyzer.analyzer_id"))
    generation = Column(Integer)
    average_offspring_fitness = Column(Float)

    @staticmethod
    def create_from_json(
            path,
            analyzer,
            session):
        with open(path) as f:
            fit_json = json.load(f)
            for entry in fit_json:
                avg_offspring_fit = AvgOffspringFit(
                    generation=int(entry['Generation']),
                    average_offspring_fitness=float(entry['AverageOffspringFitness'])
                )
                avg_offspring_fit.analyzer_id = analyzer.analyzer_id
                session.add(avg_offspring_fit)


class Pipeline(Base):
    __tablename__ = "pipeline"
    pipeline_id = Column(Integer, primary_key=True)
    digraph = Column(String)
    grid_id = Column(Integer, ForeignKey("grid.grid_id"))

    def get_digraph(self):
        raise NotImplementedError

    def to_hdev(self):
        raise NotImplementedError

    @staticmethod
    def get_pipeline_by_analyzer(session, analyzer_id):
        analyzer = session.query(Analyzer).filter_by(analyzer_id=analyzer_id).first()
        run = session.query(Run).filter_by(run_id=analyzer.run_id).first()
        grid = session.query(Grid).filter_by(run_id=analyzer.run_id).first()
        pipeline = session.query(Pipeline).filter_by(grid_id=grid.grid_id).first()

        experiment_id = run.experiment_id
        run_id = run.experiment_id
        pipeline_id = pipeline.pipeline_id
        digraph = pipeline.digraph
        return experiment_id, run_id, pipeline_id, digraph

class Individual(Base):
    __tablename__ = "individual"
    individual_id = Column(Integer, primary_key=True)
    analyzer_id = Column(Integer, ForeignKey("analyzer.analyzer_id"))
    pipeline_id = Column(Integer, ForeignKey("pipeline.pipeline_id"))
    individual_object_id = Column(Integer)
    fitness = Column(Float)

    @staticmethod
    def create_from_json(
            run_element,
            analyzer: Analyzer,
            pipeline: Pipeline):
        if run_element[0]['Fitness']['MCC'] is not None:
            return Individual(
                analyzer_id=analyzer.analyzer_id,
                pipeline_id=pipeline.pipeline_id,
                individual_object_id=int(run_element[0]['IndividualId']),
                fitness=float(run_element[0]['Fitness']['MCC'])
            )
        else:
            return Individual(
                analyzer_id=analyzer.analyzer_id,
                pipeline_id=pipeline.pipeline_id,
                individual_object_id=int(run_element[0]['IndividualId'])
            )


class Item(Base):
    __tablename__ = "item"
    item_id = Column(Integer, primary_key=True)
    name = Column(String)
    MCC = Column(Float)
    individual_id = Column(Integer, ForeignKey("individual.individual_id"))


class Grid(Base):
    __tablename__ = "grid"
    grid_id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("run.run_id"))
    hash_code = Column(Integer)
    time = Column(DateTime, default=datetime.utcnow)
    number_of_inputs = Column(Integer)

    pipeline_id = Column(
        Integer,
        ForeignKey("pipeline.pipeline_id")
    )
    vector_id = Column(
        Integer,
        ForeignKey("vector.vector_id")
    )


class InputGridNodes(Base):
    __tablename__ = "input_grid_nodes"
    input_grid_nodes_id = Column(Integer, primary_key=True)
    grid_id = Column(Integer, ForeignKey("grid.grid_id"))


class ActiveGridNodes(Base):
    __tablename__ = "active_grid_nodes"
    active_grid_nodes_id = Column(Integer, primary_key=True)
    grid_id = Column(Integer, ForeignKey("grid.grid_id"))


class OutputGridNodes(Base):
    __tablename__ = "output_grid_nodes"
    output_grid_nodes_id = Column(Integer, primary_key=True)
    grid_id = Column(Integer, ForeignKey("grid.grid_id"))


class Node(Base):
    __tablename__ = "node"
    node_id = Column(Integer, primary_key=True)
    pipeline_id = Column(Integer, ForeignKey("pipeline.pipeline_id"))
    cgp_node_id = Column(Float)
    name = Column(String)
    children = Column(String)
    # children = relationship(
    #    "Node",
    #    secondary=node_children,
    #    back_populates="Node"
    # )


class Parameter(Base):
    __tablename__ = "parameter"
    parameter_id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
    node_id = Column(Integer, ForeignKey("node.node_id"))


class Vector(Base):
    __tablename__ = "vector"
    vector_id = Column(Integer, primary_key=True)
    grid_id = Column(Integer, ForeignKey("grid.grid_id"))


class Element(Base):
    __tablename__ = "element"
    element_id = Column(Integer, primary_key=True)
    vector_id = Column(Integer, ForeignKey("vector.vector_id"))
    value = Column(Float)


class GridNode(Base):
    __tablename__ = "grid_node"
    grid_node_id = Column(Integer, primary_key=True)
    input = Column(Integer)
    name = Column(String)
    grid_id = Column(Integer, ForeignKey("grid.grid_id"))
    node_id = Column(Integer)
    input_grid_nodes_id = Column(Integer, ForeignKey("input_grid_nodes.input_grid_nodes_id"), default=None)
    active_grid_nodes_id = Column(Integer, ForeignKey("active_grid_nodes.active_grid_nodes_id"), default=None)
    output_grid_nodes_id = Column(Integer, ForeignKey("output_grid_nodes.output_grid_nodes_id"), default=None)


class GridNodeValue(Base):
    __tablename__ = "grid_node_value"
    grid_node_value_id = Column(Integer, primary_key=True)
    value = Column(Float)
    grid_node_id = Column(Integer, ForeignKey("grid_node.grid_node_id"))


class Image(Base):
    __tablename__ = "image"
    image_id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("run.run_id"))
    confusion_matrix_id = Column(
        Integer,
        ForeignKey("confusion_matrix.confusion_matrix_id")
    )
    filename = Column(String)


class ConfusionMatrix(Base):
    __tablename__ = "confusion_matrix"
    confusion_matrix_id = Column(Integer, primary_key=True)
    image_id = Column(
        Integer,
        ForeignKey("image.image_id")
    )
    true_positives = Column(Integer)
    true_negatives = Column(Integer)
    false_positives = Column(Integer)
    false_negatives = Column(Integer)
    MCC = Column(Float)
    height = Column(Integer)
    width = Column(Integer)
    size_total = Column(Integer)


class EvolutionStrategy(Base):
    __tablename__ = "evolution_strategy"
    evolution_strategy_id = Column(Integer, primary_key=True)
    configuration_id = Column(Integer, ForeignKey("configuration.configuration_id"))
    rho = Column(Integer)
    lambda_value = Column(Integer)
    plus_selection = Column(Boolean)
    mu = Column(Integer)


class FitnessFunction(enum.Enum):
    MCC = 1


class Weight(Base):
    __tablename__ = "weight"
    weight_id = Column(Integer, primary_key=True)
    halcon_fitness_configuration_id = Column(
        Integer,
        ForeignKey("halcon_fitness_configuration.halcon_fitness_configuration_id")
    )


class HalconFitnessConfiguration(Base):
    __tablename__ = "halcon_fitness_configuration"
    halcon_fitness_configuration_id = Column(Integer, primary_key=True)
    configuration_id = Column(
        Integer,
        ForeignKey("configuration.configuration_id")
    )
    region_score_weight = Column(Float)
    artifact_score_weight = Column(Float)
    fitness_score_weight = Column(Float)
    maximization = Column(Boolean)
    excess_region_handling = Column(String)
    region_count_threshold = Column(Boolean)
    execution_time_threshold = Column(Boolean)
    use_execution_time_fitness_penalty = Column(Boolean)
    execution_time_function_time_scale_factor = Column(Float)
    pixel_percentage_threshold = Column(Float)
    filename = Column(String)


class ExceptionLog(Base):
    __tablename__ = "exception"
    exception_id = Column(Integer, primary_key=True)
    experiment_id = Column(
        Integer,
        ForeignKey("experiment.experiment_id")
    )
    identifier = Column(String)
    content = Column(String)
