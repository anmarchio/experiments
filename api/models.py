import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

dataset_experiment = Table(
    "dataset_experiment",
    Base.metadata,
    Column(
        "experiment_id",
        Integer,
        ForeignKey("experiment.experiment_id")
    )
)

individual_analyzer = Table(
    "individual_analyzer",
    Base.metadata,
    Column(
        "analyzer_id",
        Integer,
        ForeignKey("analyzer.analyzer_id")
    )
)
# book_publisher = Table(
#    "book_publisher",
#    Base.metadata,
#    Column("book_id", Integer, ForeignKey("book.book_id")),
#    Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),
# )


class Experiment(Base):
    __tablename__ = "experiment"
    experiment_id = Column(Integer, primary_key=True)
    created_at = Column(datetime)
    seed = Column(Integer)
    source_directory = Column(String)
    validation_directory = Column(String)
    runs = relationship(
        "Run",
        backref=backref("experiment")
    )
    configurations = relationship(
        "Configuration",
        backref=backref("experiment")
    )
    dataset = relationship(
        "Dataset",
        backref=backref("experiment")
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
    images_id = Column(
        Integer,
        ForeignKey("images.images_id")
    )
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
    location = Column(String)
    url = Column(String)
    experiments = relationship(
        "Experiment",
        secondary=dataset_experiment,
        back_populates="Datasets"
    )


class Analyzer(Base):
    __tablename__ = "analyzer"
    analyzer_id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("run.run_id"))
    avg_individual_fit = Column(
        Integer,
        ForeignKey("avg_individual_fit.avg_individual_fit_id")
    )
    avg_population_fit = Column(
        Integer,
        ForeignKey("avg_population_fit.avg_population_fit_id")
    )
    avg_offspring_fit = Column(
        Integer,
        ForeignKey("avg_offspring_fit.avg_offspring_fit_id")
    )
    individuals = relationship(
        "Individual",
        secondary=individual_analyzer,
        back_populates="Analyzers"
    )


class Grid(Base):
    __tablename__ = "grid"
    analyzer_id = Column(Integer, primary_key=True)
    grid_id = Column(Integer, ForeignKey("grid.grid_id"))
    pipeline_id = Column(
        Integer,
        ForeignKey("pipeline.pipeline_id")
    )
    grid_nodes_id = Column(
        Integer,
        ForeignKey("grid_nodes.grid_nodes_id")
    )
    vector_id = Column(
        Integer,
        ForeignKey("vector.vector_id")
    )


class Image(Base):
    __tablename__ = "image"
    image_id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("run.run_id"))
    confusion_matrix_id = Column(Integer, ForeignKey("confusion_matrix.confusion_matrix_id"))
    filename = Column(String)


class ConfusionMatrix(Base):
    __tablename__ = "confusion_matrix"
    confusion_matrix_id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("image.image_id"))
    true_positives = Column(Integer)
    true_negatives = Column(Integer)
    false_positives = Column(Integer)
    false_negatives = Column(Integer)
    MCC = Column(float)
    height = Column(Integer)
    width = Column(Integer)
    size_total = Column(Integer)
