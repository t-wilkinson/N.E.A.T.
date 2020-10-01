# Neuro Evolution of Augmenting Topologies (N.E.A.T.)
This was my second python project. It is an attempt at an implementation of the NEAT algorithm. A genetic algorithm which aims to produce the simplest possible topology of a graph structure for a given problem.
`/neat-5` is the 'best' implementation, but still not great. It was ultimately too slow and I had trouble improving hyper-parameters.

## Hierarchy
NEAT is a evolutionary algorithm. I have seperated modules to best represent the hierarchy of the algorithm as follows:
- Population
- Species
- Organism
- Link + Node + Activation

## Running
> python neat-5/main.py
Wait a couple seconds and the top topology for each species will be visualized using matplotlib showing weights, biases and activation functions. Pressing q(quit) will go to the next graph.
