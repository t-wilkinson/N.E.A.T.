# Neuro Evolution of Augmenting Topologies (NEAT)
An attempt at an implementation of the [NEAT genetic algorithm](https://en.wikipedia.org/wiki/Neuroevolution_of_augmenting_topologies). A genetic algorithm which aims to produce the simplest possible topology of a graph structure for a given problem.
The implementation is not great so I would like to improve it one day.

## Layout
NEAT is a evolutionary algorithm. I have seperated modules to best represent the hierarchy of the algorithm as follows:
- Population
- Species
- Organism
- Link + Node + Activation

## /ball-fall
This is a game I made to test the algorithm (although a hard coded solution would be better in practice). The program slows considerably over time. I'll fix it eventually.
```bash
$ python ball-fall/ball_fall.py
```

## Running
The top topology for each species will be visualized using matplotlib showing weights, biases and activation functions. Pressing q(uit) will go to the next graph.
```bash
$ python neat/main.py
```
