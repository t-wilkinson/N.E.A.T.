'''
Genome represents an organism
Each Genome has a list of Gene objects.
'''
import config
import random
import itertools as it

from copy import deepcopy
from gene import Gene


'''
Class
'''
class Genome:
    ''' . '''
    def __init__(self, inputs: int, outputs: int):
        # create most basic topology
        self.Nodes = {
            'input': list(range(inputs)),
            'output': list(range(inputs, inputs + outputs)),
            'hidden': [],
        }

        self.Genes = [
            Gene(*node) for node in
            it.product(self.Nodes['input'], self.Nodes['output'])
        ]


    ''' Pretty print. '''
    def print_genes(self):
        print('|============================================|' + \
        '\n|                   Genes                    |' + \
        '\n|--------------------------------------------|' + \
        '\n|  IN:OUT |   Weight   | Innovation | Active |\n' + \
        '\n'.join([f'{gene}' for gene in self.Genes]) + \
        '\n|============================================|')

    def print_nodes(self):
        print('|============================================|' + \
        '\n|                   Nodes                    |' + \
        '\n|--------------------------------------------|' + \
        '\n|  ID |      Layer       |        Bias       |\n' + \
        '\n'.join([f'{node}' for node in self.Nodes.values()]) + \
        '\n|============================================|')


    ''' Simple helper functions. '''
    def clone(self):
        return deepcopy(self)


    ''' Mutations. '''
    def mutate(self):
        if random.uniform(0, 1) < config.chance_new_node:
            self.add_node()
        if random.uniform(0, 1) < config.chance_new_link:
            self.add_link()
        if random.uniform(0, 1) < config.chance_mutate_weight:
            for gene in self.Genes:
                gene.mutate()


    def add_node(self):
        '''
        Create new node to add to existing link.
        Set link weight from In node -> new node to 1.0
        and weight from new node -> Out node to original weight.
        Reduce mal-effect of adding new node.
        '''
        gene = random.choice([gene for gene in self.Genes if gene.active])
        gene.active = False
        node = Gene.get_node(gene.nodes)
        if not node in self.Nodes['hidden']:
            self.Nodes['hidden'].append(node)

        # To node -> new node has weight of 1
        self.add_gene(gene.nodes[0], node, 1.0)
        # new node -> OUT has weight of original link
        self.add_gene(node, gene.nodes[1], gene.weight)

    def add_link(self):
        ''' Add link to two unconnected nodes. '''
        if not self.Nodes['hidden']:
            return

        # find all possible links
        all_nodes = sum(self.Nodes.values(), [])

        all_links = ((n0, n1) for n1 in all_nodes for n0 in self.Nodes['hidden'] if n0 != n1)
        current_links = (gene.nodes for gene in self.Genes)
        possible_links = list(set(all_links) - set(current_links))
        print(self.Nodes['hidden'])
        print(possible_links)

        # select a random link and add link
        if possible_links:
            random_link = random.choice(possible_links)
            self.add_gene(*random_link)

    def add_gene(self, IN: int, OUT: int, weight=None):
        ''' Add new conneciton to genome. '''
        self.Genes.append(
            Gene(IN, OUT, weight)
        )


    ''' Mating methods. '''
    def crossover(self, genome):
        ''' Crossover two genomes. '''
        genes = []
        unfitter, fitter = sorted([self, genome], key=lambda x: x.fitness)

        for i, (unfit, fit) in enumerate(zip(unfitter.Genes, fitter.Genes)):
            # if genes are matching
            if fit.innovation == unfit.innovation:
                gene = random.choice((unfit, fit)).clone()
                if not(unfit.active and fit.active):
                    gene.randomize()
                genes.append(gene)
            # if genes are disjoint / excess
            else:
                for gene in fitter.Genes[i:]:
                    gene = gene.clone()
                    if not gene.active:
                        gene.randomize()
                    genes.append(gene)
                break

        kid = self.clone()
        kid.Genes = genes
        return kid

    def compatable(self, genome):
        ''' Quantize compatability of two genomes. '''
        matching = []
        disjoint, excess = 0, 0
        for (gene1, gene2) in it.zip_longest(self.Genes, genome.Genes):
            if gene1 and gene2:
                if gene1 == gene2:
                    matching.append((gene1.weight - gene2.weight))
                else:
                    disjoint += 1
            else:
                excess += 1

        weight_avg = sum(matching) / len(matching)
        normalize = max(len(self.Genes), len(genome.Genes))

        compatability = config.C1 * excess / normalize + \
                        config.C2 * disjoint / normalize + \
                        config.C3 * weight_avg

        return compatability < config.compatability_distance_threshold


