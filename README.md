# Neuro Evolution of Augmenting Topologies (NEAT)
This was my second python project. It is an attempt at an implementation of the NEAT algorithm. A genetic algorithm which aims to produce the simplest possible topology of a graph structure for a given problem.
`/neat-5` is the 'best' implementation, but still not great. It was ultimately too slow and I had trouble improving hyper-parameters.

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
This is a game I made to test the algorithm. It kind of works, but as the time spent running the program increases, it slows down. I believe this is an issue with the garbage collector not recognizing the previous populations can be removed, resulting in a large buildup of objects.

```bash
$ python ball-fall/ball_fall.py
```

## /neat-5
This is the 'best' version of my implementation of the NEAT algorithm.  Wait a couple seconds and the top topology for each species will be visualized using matplotlib showing weights, biases and activation functions. Pressing q(quit) will go to the next graph.

```bash
$ python neat-5/main.py
```
