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
  weights: double[]
  fitness_functions: FitnessFunction[]
  excess_region_handling: Object
  region_count_threshold: bool
  execution_time_threshold: bool
  use_execution_time_fitness_penalty: bool
  execution_time_function_scale_factor: float
  pixel_percentage_threshold: float
  filename: String
}

class FitnessFunction {
  label: String
}

class DataSet {
  name: String
  location: String
}

class Analyzer

class FitnessList {
  values: float[] 
}
class AvgOffspringFit

class AvgPopulationFit

class AvgIndividualFit

class Individual {
  id: Int
  generation_number: Int
}

class Item {
  name: String
  MCC: float
}

class Grid
class GridNodes {
  hash_code: Int
  time: DateTime
  inputs: Int[]
  number_of_outputs: Int
  active_nodes: Int[]
}
class GridNode {
  in: Int
  name: String
  values: Float[]
}
class Pipeline {
  digraph: String
  + string get_digraph()
  + string to_hdev()
}

class Node {
  node_id: float
  children: Node[]
  name: String
}

class Parameter {
  name: String
  value: abstract
}

class Vector {
  values: Float[]
}

class Images
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
FitnessList <|- AvgOffspringFit
FitnessList <|- AvgPopulationFit
FitnessList <|- AvgIndividualFit

Configuration "1" -- "1" HalconFitnessConfiguration
Configuration "1" -- "1" EvolutionStrategy

Analyzer "1" -- "1" AvgOffspringFit 
Analyzer "1" -- "1" AvgPopulationFit
Analyzer "1" -- "1" AvgIndividualFit
Analyzer "1" -- "*" Individual
Individual "1" -- "*" Item
Individual "1" -- "1" Pipeline

Run "1" -- "1" Grid
Grid "1" -- "1" GridNodes
GridNodes "1" -- "*" GridNode
Grid "1" -- "1" Pipeline
Grid "1" -- "1" Vector
Pipeline "1" -- "*" Node
Node "1" -- "*" Parameter

Run "1" -- "1" Images
Images "1" -- "*" Image
Image "1" -- "1" ConfusionMatrix
```

