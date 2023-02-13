import datetime
import json
import unittest

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import xml.etree.ElementTree as ET

from api.models import Dataset, Experiment, Run, Base, Analyzer, AvgOffspringFit, AvgPopulationFit, BestIndividualFit, \
    Configuration, EvolutionStrategy, HalconFitnessConfiguration, Image, ConfusionMatrix, ExceptionLog
from api.test_data import AvgOffspringFit_0, AvgPopulationFit_0, BestIndividualFit_0, EVOLUTIONSTRATEGY_TXT, \
    FITNESS_TXT, IMAGES_0, LEGEND_TXT, EXCEPTION_TXT

SQLITE_TEST_PATH = "experiments_test.db"


class TestModel(unittest.TestCase):
    def setUp(self) -> None:
        engine = create_engine(f"sqlite:///{SQLITE_TEST_PATH}")
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()
        self.create_dataset_experiment_run()

    def create_dataset_experiment_run(self) -> None:
        # Create dataset
        self.dataset = Dataset(
            name="CF_ReferenceSet_Small_Dark",
            source_directory="C:\\Users\\Public\\evias_expmts\\Aircarbon2\\CF_ReferenceSet_Small_Dark",
            validation_directory="C:\\Users\\Public\\evias_expmts\\\\Aircarbon2\\CF_ReferenceSet_Small_Dark",
            description="",
            url=""
        )
        self.experiment = Experiment(
            created_at=datetime.datetime.utcnow(),
            seed=1449031162,
            dataset_id=self.dataset.dataset_id
        )
        self.run = Run(
            started_at=datetime.datetime.utcnow(),
            number=0,
            legend=LEGEND_TXT,
            experiment_id=self.experiment.experiment_id
        )

        self.session.begin()

        self.session.add(self.dataset)
        self.session.add(self.experiment)
        self.session.add(self.run)
        # Commit entries
        self.session.commit()

    def test_analyzer(self):
        # Analyzer
        #         |_0
        #            |_ AvgOffspringFit.json
        #            |_ AvgPopulationFit.json
        #            |_ AvgIndividualFit.json
        #            |_ individual_evaluation_log.json
        #            |_ loader_evaluation_log.json
        avg_offspring_fit_json = json.loads(AvgOffspringFit_0)
        avg_population_fit_json = json.loads(AvgPopulationFit_0)
        best_individual_fit_json = json.loads(BestIndividualFit_0)

        self.session.begin()
        analyzer = Analyzer(run_id=self.run.run_id)
        self.session.add(analyzer)

        for entry in avg_offspring_fit_json:
            avg_offspring_fit = AvgOffspringFit(
                generation=int(entry['Generation']),
                average_offspring_fitness=float(entry['AverageOffspringFitness'])
            )
            avg_offspring_fit.analyzer_id = analyzer.analyzer_id
            self.session.add(avg_offspring_fit)

        for entry in avg_population_fit_json:
            avg_population_fit = AvgPopulationFit(
                generation=int(avg_population_fit_json[0]['Generation']),
                average_population_fitness=float(entry['AveragePopulationFitness'])
            )
            avg_population_fit.analyzer_id = analyzer.analyzer_id
            self.session.add(avg_population_fit)

        for entry in best_individual_fit_json:
            best_individual_fit = BestIndividualFit(
                generation=int(entry['Generation']),
                average_individual_fitness=float(entry['AverageIndividualFitness'])
            )
            best_individual_fit.analyzer_id = analyzer.analyzer_id
            self.session.add(best_individual_fit)

        self.session.commit()

        # Count default rows
        default_row_count = [
            self.session.query(Dataset).count(),
            self.session.query(Run).count(),
            self.session.query(Experiment).count()
        ]
        self.assertEqual(default_row_count, [1, 1, 1])

        # Count Analyzer Rows
        analyzer_row_count = [
            self.session.query(Analyzer).count(),
            self.session.query(AvgOffspringFit).count(),
            self.session.query(AvgPopulationFit).count(),
            self.session.query(BestIndividualFit).count()
        ]
        self.assertEqual(analyzer_row_count, [1, 3, 3, 3])

        # Remove from database
        self.session.delete(analyzer)
        self.session.query(AvgOffspringFit).delete()
        self.session.query(AvgPopulationFit).delete()
        self.session.query(BestIndividualFit).delete()
        self.session.commit()
        self.session.flush()

    def test_config(self):
        # Config
        #       |_ EvoluationStrategy.txt
        #       |_ Fitness.txt

        # from file
        # tree = ET.parse('country_data.xml')
        # root = tree.getroot()

        configuration = Configuration(
            experiment_id=self.experiment.experiment_id
        )

        evolution_strategy_xml = ET.fromstring(EVOLUTIONSTRATEGY_TXT)
        evolution_strategy = EvolutionStrategy(
            configuration_id=configuration.configuration_id,
            rho=int(evolution_strategy_xml.findall('Rho')[0].text),
            lambda_value=int(evolution_strategy_xml.findall('Lambda')[0].text),
            plus_selection=bool(evolution_strategy_xml.findall('PlusSelection')[0].text),
            mu=int(evolution_strategy_xml.findall('Mu')[0].text)
        )

        fitness_xml = ET.fromstring(FITNESS_TXT)
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

        self.session.add(configuration)
        self.session.add(evolution_strategy)
        self.session.add(halcon_fitness_config)
        # Commit entries
        self.session.commit()

        # Query and check config rows
        es_query = self.session.query(EvolutionStrategy).first()
        self.assertEqual(
            [
                es_query.rho,
                es_query.lambda_value,
                es_query.plus_selection,
                es_query.mu
            ],
            [
                0,
                4,
                True,
                1
            ]
        )
        halcon_fit_config_query = self.session.query(HalconFitnessConfiguration).first()
        self.assertEqual(
            [
                halcon_fit_config_query.fitness_score_weight,
                halcon_fit_config_query.maximization,
                halcon_fit_config_query.pixel_percentage_threshold
            ],
            [
                1,
                True,
                0.699999988079071
            ]
        )

        # Remove from database
        self.session.delete(configuration)
        self.session.delete(evolution_strategy)
        self.session.delete(halcon_fitness_config)
        self.session.commit()
        self.session.flush()

    def test_image(self):
        # Images
        #       |_0
        #          |_ 16.bmp
        #          |_ ...
        #          |_ ...
        #          |_ AppendPipelineConfusionMatrix.json
        #          |_ ConfusionMatrix.json
        #          |_ legend.txt
        images_json = json.loads(IMAGES_0)
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
                run_id=self.run.run_id,
                confusion_matrix_id=confusion_matrix.confusion_matrix_id,
                filename=img
            )
            confusion_matrix.image_id = image.image_id
            self.session.add(image)
            self.session.add(confusion_matrix)

        self.session.commit()

        # Count default rows
        images_confusion_matrix_count = [
            self.session.query(Image).count(),
            self.session.query(ConfusionMatrix).count()
        ]
        self.assertEqual(images_confusion_matrix_count, [3, 3])

        # Remove from database
        self.session.query(Image).delete()
        self.session.query(ConfusionMatrix).delete()
        self.session.commit()
        self.session.flush()

    def test_grid(self):
        # Grid
        #     |_0
        #        |_ append_pipeline.txt
        #        |_ grid.txt
        #        |_ pipeline.txt
        #        |_ vector.txt
        exception_log = ExceptionLog(
            exception_id=self.experiment.experiment_id,
            identifier="A6BBA1CC-20230131",
            content=EXCEPTION_TXT
        )
        self.session.add(exception_log)
        self.session.commit()

        # Count Exception Rows
        self.assertEqual(self.session.query(ExceptionLog).count(), 1)

        # Remove from database
        self.session.delete(exception_log)
        self.session.commit()
        self.session.flush()

    def tearDown(self) -> None:
        # Empty database
        self.session.delete(self.dataset)
        self.session.delete(self.experiment)
        self.session.delete(self.run)
        self.session.commit()
        self.session.flush()


if __name__ == '__main__':
    unittest.main()
