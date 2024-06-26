# CGP Experiments: Parameter Tuning

All CGP experiments provide pipelines that consist of typically HALCON encoded sequences of image filters.
They have already been put through genetic programming optimization. However, due to the complexity of problems, 
the pipelines might basically be good but the suggested parameters may not be.
Therefore, this subproject will perform optimization only on the parameters of nodes, so to say concentrating 
on these degrees of freedom.

The following optimization algorithms are used:
* Simulated Annealing: `simmulated_annealing.py`
* Local search: `local_search.py`
* PSO (NOT IMPLEMENTED): `pso.py`

### Simulated Annealing
Simulated Annealing is a probabilistic technique that explores the search space by allowing occasional uphill moves to escape local minima. It gradually reduces the probability of such moves as the algorithm progresses.

### Local Search
Local Search is a simpler heuristic that iteratively moves to neighboring solutions in the search space to find a better solution.


### PSO (optional)
PSO simulates the social behavior of birds flocking to find optimal regions in the search space. Each particle represents a potential solution and adjusts its position based on its own experience and the experience of neighboring particles.