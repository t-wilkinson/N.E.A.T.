# NEAT
Neuroevolution of augmenting topologies

To run, run the neat.py file

Each genome has a list of gene objects.
Each gene object is a link between two nodes.
If two different genes in the same genome share a node, I want those two genes to point to the SAME node.

I believe this is the problem:
The problem is when I crossover two genomes.
During crossover, if genes are matching(have the same innovation number), then a gene is randomly selected and passed to the offspring.
If the genes are disjoint/excess (they don't match up), the genes from the more-fit parent are passed over.

During the crossover of two matching genes, if a gene is selected from the less-fit parent, then if any genes in the more fit parent
  connect to the same node id, then the new genome can have two genes that point to DIFFERENT nodes with the SAME id.
  
Is there a way to force all other nodes in the genome that have the same id to point to the same node object?
*Each genome must be seperate from the others
