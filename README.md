# Neuro Evolution of Augmenting Topologies (NEAT)
This was my second python project. It is an attempt at an implementation of the NEAT algorithm. A genetic algorithm which aims to produce the simplest possible topology of a graph structure for a given problem.

* [Layout](#layout)
* [/ball-fall](#/ball-fall)
* [/neat-5](#/neat-5)

## Layout
NEAT is a evolutionary algorithm. I have seperated modules to best represent the hierarchy of the algorithm as follows:
- Population
- Species
- Organism
- Link + Node + Activation

## /ball-fall
This is a game I made to test the algorithm. It kind of works, but as the time spent running the program increases, it slows down considerably. This is largely due to a non-ideal implementation of the genome structure which has poor time complexity.

```bash
$ python ball-fall/ball_fall.py
```

## /neat-5
This is my favorite implementation of the NEAT algorithm. The top topology for each species will be visualized using matplotlib showing weights, biases and activation functions. Pressing q(quit) will go to the next graph.

```bash
$ python neat-5/main.py
```
