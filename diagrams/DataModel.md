# Experiment Data Model

## Data Objects

```plantuml
class Experiment {
  created_at: DateTime
  seed: Int
  source_directory: String
  validation_directory: String
}

class Run {
  started_at: DateTime
  number: Int
}

class Configuration 

class EvolutionStrategy {
  rho: Int
  lambda: Int
  plus_selection: bool
  mu: Int
}

class HalconFitnessConfiguration {
  region_score_weight: float
  artifact_score_weight: float
  fitness_score_weight: float
  maximization: bool
  fitness_functions: FitnessFunction[]
  excess_region_handling: Object
  region_count_threshold: bool
  execution_time_threshold: bool
  use_execution_time_fitness_penalty: bool
  execution_time_function_scale_factor: float
  pixel_percentage_threshold: float
  filename: String
}

class Weight{
  value: Int
}

enum FitnessFunction {
  MCC
  F-Score
  RegionScore
  Accuracy
  Precision
  Recall
}

class DataSet {
  name: String
  location: String
  url: String
}

class Analyzer

class AvgOffspringFit {
  generation: Int
  average_offspring_fitness: Float
}

class AvgPopulationFit {
  generation: Int
  average_population_fitness: Float
}

class BestIndividualFit {
  generation: Int
  best_individiual_fitness: Float
}

class Individual {
  id: Int
  generation_number: Int
}

class Item {
  name: String
  MCC: float
}

class Grid {
  hash_code: Int
  time: DateTime
  number_of_outputs: Int
}

class ActiveGridNodes
class InputGridNodes

class GridNode {
  in: Int
  name: String
}

class GridNodeValue {
  value: Float
}

class Pipeline {
  digraph: String
  + string get_digraph()
  + string to_hdev()
}

class Node {
  node_id: float
  name: String
}

class Parameter {
  name: String
  value: String
}

class Vector

class Element {
  value: Float
}

class Image {
  filename: String
}

class ConfusionMatrix {
    true_positives: Int
    true_negatives: Int
    false_positives: Int
    false_negatives: Int
    MCC: Float
    height: Int
    width: Int
    size_total: Int
}

Experiment "1" -- "*" Run
Experiment "*" -- "1" DataSet
Experiment "*" -- "1" Configuration

Run "1" -- "1" Analyzer

Configuration "1" -- "1" HalconFitnessConfiguration
Configuration "1" -- "1" EvolutionStrategy
HalconFitnessConfiguration "1" -- "*" Weight

Analyzer "1" -- "*" AvgOffspringFit 
Analyzer "1" -- "*" AvgPopulationFit
Analyzer "1" -- "*" BestIndividualFit
Analyzer "1" -- "*" Individual
Individual "1" -- "*" Item
Individual "1" -- "1" Pipeline

Run "1" -- "1" Grid
Grid "1" -- "1"  ActiveGridNodes
Grid "1" -- "1"  InputGridNodes
ActiveGridNodes "1" -- "*" GridNode
InputGridNodes "1" -- "*" GridNode
Grid "1" -- "*" GridNode
GridNode "1" -- "*" GridNodeValue
Grid "1" -- "1" Pipeline
Grid "1" -- "1" Vector
Vector "1" -- "*" Element
Pipeline "1" -- "*" Node
Node "1" -- "*" Parameter
Node "1" -- "0..*" Node

Run "1" -- "*" Image
Image "1" -- "1" ConfusionMatrix
```

