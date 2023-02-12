import datetime
import unittest

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from api.models import Dataset, Experiment, Run, Base


class TestModel(unittest.TestCase):
    def setUp(self) -> None:
        # engine = create_engine('sqlite:///school.db', echo=True)
        # with resources.path(
        #        "experiments", "experiments.db"
        # ) as sqlite_filepath:
        #    engine = create_engine(f"sqlite:///{sqlite_filepath}")
        sqlite_filepath = "experiments.db"
        engine = create_engine(f"sqlite:///{sqlite_filepath}")
        # Create the profile table
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()

    def test_analyzer_import(self):
        # Analyzer
        #         |_0
        #            |_ AvgOffspringFit.json
        #            |_ AvgPopulationFit.json
        #            |_ AvgIndividualFit.json
        #            |_ individual_evaluation_log.json
        #            |_ loader_evaluation_log.json
        # Create dataset
        dataset = Dataset(
            name="CF_ReferenceSet_Small_Dark",
            source_directory="C:\\Users\\Public\\evias_expmts\\Aircarbon2\\CF_ReferenceSet_Small_Dark",
            validation_directory="C:\\Users\\Public\\evias_expmts\\\\Aircarbon2\\CF_ReferenceSet_Small_Dark",
            description="",
            url=""
        )
        experiment = Experiment(
            created_at=datetime.datetime.utcnow(),
            seed=1449031162,
            dataset_id=dataset.dataset_id
        )
        run = Run(
            started_at=datetime.datetime.utcnow(),
            number=0,
            experiment_id=experiment.experiment_id
        )
        #analyzer = Analyzer(run_id=run.run_id)

        self.session.begin()

        self.session.add(dataset)
        self.session.add(experiment)
        self.session.add(run)
        #self.session.add(analyzer)
        # Commit entries
        self.session.commit()

        # Count rows
        datasets = self.session.query(Dataset).count()
        self.assertEqual(datasets, 1)
        runs = self.session.query(Run).count()
        self.assertEqual(runs, 1)
        experiments = self.session.query(Experiment).count()
        self.assertEqual(experiments, 1)
        #analyzers = self.session.query(Analyzer).count()
        #self.assertEqual(analyzers, 1)

        # Empty database
        self.session.delete(dataset)
        self.session.delete(experiment)
        self.session.delete(run)
        #self.session.delete(analyzer)
        self.session.commit()
        self.session.flush()


if __name__ == '__main__':
    unittest.main()
