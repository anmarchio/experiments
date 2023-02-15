import datetime
import json
import re
import unittest
import xml.etree.ElementTree as ET

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from env_var import SQLITE_TEST_PATH
from models import Dataset, Experiment, Run, Base, Analyzer, AvgOffspringFit, AvgPopulationFit, BestIndividualFit, \
    Configuration, EvolutionStrategy, HalconFitnessConfiguration, Image, ConfusionMatrix, ExceptionLog, Element, Vector, \
    Grid, ActiveGridNodes, InputGridNodes, OutputGridNodes, GridNode, GridNodeValue, Pipeline, Individual, Node, \
    Parameter, Item
from test_data import AvgOffspringFit_0, AvgPopulationFit_0, BestIndividualFit_0, EVOLUTIONSTRATEGY_TXT, \
    FITNESS_TXT, IMAGES_0, LEGEND_TXT, EXCEPTION_TXT, VECTOR, GRID_TXT, APPEND_PIPELINE_TXT, LOADER_EVALUATION_LOG, \
    INDIVIDUAL_EVALUATION_LOG


class TestModel(unittest.TestCase):
    def setUp(self) -> None:
        engine = create_engine(f"sqlite:///{SQLITE_TEST_PATH}")
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()
        self.create_dataset_experiment_grid_run_analyzer()

    def create_dataset_experiment_grid_run_analyzer(self) -> None:
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
        lines = GRID_TXT.splitlines()
        self.grid = Grid(
            hash_code=int(lines[0][10:19]),
            time=datetime.datetime.strptime(lines[1][6:25], '%m/%d/%Y %I:%M:%S %p'),
            number_of_inputs=int(lines[3][7:-1]),
            run_id=self.run.run_id
        )
        self.analyzer = Analyzer(run_id=self.run.run_id)

        self.session.begin()

        self.session.add(self.dataset)
        self.session.add(self.experiment)
        self.session.add(self.run)
        self.session.add(self.grid)
        self.session.add(self.analyzer)
        # Commit entries
        self.session.commit()

    def test_fitness_analyzers(self):
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

        for entry in avg_offspring_fit_json:
            avg_offspring_fit = AvgOffspringFit(
                generation=int(entry['Generation']),
                average_offspring_fitness=float(entry['AverageOffspringFitness'])
            )
            avg_offspring_fit.analyzer_id = self.analyzer.analyzer_id
            self.session.add(avg_offspring_fit)

        for entry in avg_population_fit_json:
            avg_population_fit = AvgPopulationFit(
                generation=int(avg_population_fit_json[0]['Generation']),
                average_population_fitness=float(entry['AveragePopulationFitness'])
            )
            avg_population_fit.analyzer_id = self.analyzer.analyzer_id
            self.session.add(avg_population_fit)

        for entry in best_individual_fit_json:
            best_individual_fit = BestIndividualFit(
                generation=int(entry['Generation']),
                average_individual_fitness=float(entry['AverageIndividualFitness'])
            )
            best_individual_fit.analyzer_id = self.analyzer.analyzer_id
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

    def test_exception(self):
        # Exception
        #          |_ 9917D8E0-20230202.txt
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

    def test_grid_vector(self):
        # Grid
        #     |_0
        #        |_ append_pipeline.txt
        #        |_ grid.txt
        #        |_ pipeline.txt
        #        |_ vector.txt
        vector = Vector(
            grid_id=self.grid.grid_id
        )
        self.session.add(vector)

        vector_values = VECTOR.split(",")
        for val in vector_values:
            element = Element(
                vector_id=vector.vector_id,
                value=float(val)
            )
            self.session.add(element)

        self.session.commit()

        # Count Grid and Vector Rows
        self.assertEqual(
            [
                self.session.query(Grid).count(),
                self.session.query(Vector).count(),
                self.session.query(Element).count()
            ],
            [
                1,
                1,
                901
            ]
        )

        # Remove from database
        self.session.delete(vector)
        self.session.query(Element).delete()
        self.session.commit()
        self.session.flush()

    def test_grid_nodes(self):
        # Grid
        #     |_0
        #        |_ append_pipeline.txt
        #        |_ grid.txt
        #        |_ pipeline.txt
        #        |_ vector.txt
        active_grid_nodes = ActiveGridNodes(
            grid_id=self.grid.grid_id
        )
        self.session.add(active_grid_nodes)

        input_grid_nodes = InputGridNodes(
            grid_id=self.grid.grid_id
        )
        self.session.add(input_grid_nodes)

        output_grid_nodes = OutputGridNodes(
            grid_id=self.grid.grid_id
        )
        self.session.add(output_grid_nodes)

        lines = GRID_TXT.splitlines()
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
                grid_id=self.grid.grid_id,
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
            self.session.add(grid_node)

            # Add node values
            values_in_brackets = re.search(r"\([0-9.,-]+\)", node.split(":")[2])
            values = values_in_brackets.string[
                     values_in_brackets.regs[0][0] + 1:values_in_brackets.regs[0][1] - 1].split(",")
            for v in values:
                grid_node_value = GridNodeValue(
                    grid_node_id=grid_node.grid_node_id,
                    value=float(v),
                )
                self.session.add(grid_node_value)

        self.session.commit()

        # Count Grid and Vector Rows
        self.assertEqual(
            self.session.query(GridNode).count(),
            100
        )

        # Remove from database
        self.session.delete(active_grid_nodes)
        self.session.delete(input_grid_nodes)
        self.session.delete(output_grid_nodes)
        self.session.query(GridNode).delete()
        self.session.query(GridNodeValue).delete()
        self.session.commit()
        self.session.flush()

    def test_pipeline(self):
        evaluation_loader_json = json.loads(LOADER_EVALUATION_LOG)
        individual = None
        pipeline = Pipeline(
            digraph=APPEND_PIPELINE_TXT,
            grid_id=self.grid.grid_id
        )
        self.session.add(pipeline)

        for i in range(len(evaluation_loader_json)):
            run = evaluation_loader_json[str(i)]
            individual = Individual(
                analyzer_id=self.analyzer.analyzer_id,
                individual_object_id=int(run[0]['IndividualId']),
                pipeline_id=pipeline.pipeline_id,
                fitness=float(run[0]['Fitness']['MCC'])
            )

            pipeline_nodes = run[0]['Pipeline']
            for p_node in pipeline_nodes:
                node = Node(
                    cgp_node_id=float(p_node['NodeID']),
                    name=p_node['Name'],
                    children=str(p_node['Children']),
                    pipeline_id=pipeline.pipeline_id
                )
                self.session.add(node)
                parameters = p_node['Parameters']
                for p in parameters:
                    parameter = Parameter(
                        name=p['Name'],
                        value=p['Value'],
                        node_id=node.node_id
                    )
                    self.session.add(parameter)

        individual_evaluation_json = json.loads(INDIVIDUAL_EVALUATION_LOG)
        for i in range(len(individual_evaluation_json)):
            items = individual_evaluation_json[str(i)]
            for ind_item in items:
                item = Item(
                    MCC=ind_item['FitnessValues']['MCC'],
                    name=ind_item['Item'],
                    individual_id=individual.individual_id
                )
                self.session.add(item)

        self.session.commit()

        # Count Pipeline Rows
        self.assertEqual(
            [
                self.session.query(Pipeline).count(),
                self.session.query(Node).count(),
                self.session.query(Parameter).count(),
                self.session.query(Item).count()
            ],
            [
                1,
                3,
                10,
                3
            ]
        )

        # Empty database
        self.session.query(Pipeline).delete()
        self.session.query(Node).delete()
        self.session.query(Parameter).delete()
        self.session.query(Item).delete()
        self.session.commit()
        self.session.flush()

    def tearDown(self) -> None:
        # Empty database
        self.session.delete(self.dataset)
        self.session.delete(self.experiment)
        self.session.delete(self.run)
        self.session.delete(self.grid)
        self.session.delete(self.analyzer)
        self.session.commit()
        self.session.flush()


if __name__ == '__main__':
    unittest.main()
