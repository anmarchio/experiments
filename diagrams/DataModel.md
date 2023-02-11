# Experiment Data Model

## Data Objects

```plantuml
class Experiment {}

class Run{
  created_at: DateTime
  number: Int
}

Comfiguration {
  Mu: Int
  Lambda: Int
}

class DataSet {
  name: String
  location: String
}

Experiment "1" -- "*" Run
Experiment "*" -- "*" DataSet
Run "*" -- "*" Configuration
```
