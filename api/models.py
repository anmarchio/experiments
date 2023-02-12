import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

"""
node_children = Table(
    "node_children",
    Base.metadata,
    Column(
        "node_id",
        Integer,
        ForeignKey("node.node_id")
    )
)
"""


class Experiment(Base):
    __tablename__ = "experiment"
    experiment_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    seed = Column(Integer)
    dataset_id = Column(
        Integer,
        ForeignKey("dataset.dataset_id")
    )


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
    dataset_id = Column(
        Integer,
        ForeignKey("dataset.dataset_id")
    )
    number = Column(Integer)


class Dataset(Base):
    __tablename__ = "dataset"
    dataset_id = Column(Integer, primary_key=True)
    name = Column(String)
    source_directory = Column(String)
    validation_directory = Column(String)
    description = Column(String)
    url = Column(String)


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


class AvgPopulationFit(Base):
    __tablename__ = "avg_population_fit"
    avg_population_fit_id = Column(Integer, primary_key=True)
    analyzer_id = Column(Integer, ForeignKey("analyzer.analyzer_id"))
    generation = Column(Integer)
    average_population_fitness = Column(Float)


class AvgOffspringFit(Base):
    __tablename__ = "avg_offspring_fit"
    best_individual_fit_id = Column(Integer, primary_key=True)
    analyzer_id = Column(Integer, ForeignKey("analyzer.analyzer_id"))
    generation = Column(Integer)
    average_offspring_fitness = Column(Float)


class Individual(Base):
    __tablename__ = "individual"
    individual_id = Column(Integer, primary_key=True)
    analyzer_id = Column(Integer, ForeignKey("analyzer.analyzer_id"))
    generation_number = Column(Integer)


class Item(Base):
    __tablename__ = "item"
    item_id = Column(Integer, primary_key=True)
    name = Column(String)
    MCC = Column(Float)
    individual_id = Column(Integer, ForeignKey("individual.individual_id"))


class Grid(Base):
    __tablename__ = "grid"
    analyzer_id = Column(Integer, primary_key=True)
    grid_id = Column(Integer, ForeignKey("grid.grid_id"))
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


class Pipeline(Base):
    __tablename__ = "pipeline"
    pipeline_id = Column(Integer, primary_key=True)
    digraph = Column(String)
    individual_id = Column(Integer, ForeignKey("individual.individual_id"))
    grid_id = Column(Integer, ForeignKey("grid.grid_id"))

    def get_digraph(self):
        raise NotImplementedError

    def to_hdev(self):
        raise NotImplementedError


class Node(Base):
    __tablename__ = "node"
    node_id = Column(Integer, primary_key=True)
    cgp_node_id = Column(Float)
    name = Column(String)
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


class GridNode(Base):
    __tablename__ = "grid_node"
    grid_node_id = Column(Integer, primary_key=True)
    input = Column(Integer)
    name = Column(String)
    grid_id = Column(Integer, ForeignKey("grid.grid_id"))
    input_grid_nodes_id = Column(Integer, ForeignKey("input_grid_nodes.input_grid_nodes_id"), default=None)
    active_grid_nodes_id = Column(Integer, ForeignKey("active_grid_nodes.active_grid_nodes_id"), default=None)


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
    fitness_function = Column(Enum(FitnessFunction))
    excess_region_handling = Column(Boolean)
    region_count_threshold = Column(Boolean)
    execution_time_threshold = Column(Boolean)
    execution_time_fitness_penalty = Column(Boolean)
    execution_time_fuction_time_scale_factor = Column(Float)
    pixel_percentage_threshold = Column(Float)
    filename = Column(String)
