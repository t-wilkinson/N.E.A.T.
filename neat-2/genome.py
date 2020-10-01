'''
Genome represents an organism
Each Genome has a list of Gene objects.
'''
import config
import random
import itertools as it

from copy import deepcopy
from gene import Gene, Node


'''
Class
'''
class Genome:
    ''' . '''

    def __init__(self, inputs, outputs):
        # create list of input and output Nodes
        self.Nodes = [Node('input') for _ in range(inputs)]
        self.Nodes += [Node('output') for _ in range(outputs)]

        # create every possible link from input to output nodes
        self.Genes = [Gene(IN.ID, OUT.ID) for IN, OUT in it.product(self.Nodes[:inputs], self.Nodes[inputs:])]


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
        '\n'.join([f'{node}' for node in self.Nodes]) + \
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
        gene = random.choice(self.Genes)
        gene.activation = False

        ID = Gene.get_node_id(gene.IN, gene.OUT)
        node = Node('hidden', ID)
        self.Nodes.append(node)

        # To node -> new node has weight of 1
        self.add_gene(gene.IN, ID, 1.0)
        # new node -> OUT has weight of original link
        self.add_gene(ID, gene.OUT, gene.weight)

    def add_link(self):
        ''' Add link to two unconnected nodes. '''
        # find all possible links
        hidden_nodes = (node for node in self.Nodes if node.layer == 'hidden')
        all_links = (link for link in it.product(self.Nodes, hidden_nodes) if link[0].ID != link[1].ID)
        current_links = (link for link in self.Genes)
        possible_links = list(set(all_links) - set(current_links))

        # select a random link and add link
        if possible_links:
            (IN, OUT) = random.choice(possible_links)
            self.add_gene(IN.ID, OUT.ID)

    def add_gene(self, IN: int, OUT: int, weight: float=None):
        ''' Add new conneciton to genome. '''
        self.Genes.append(
            Gene(IN, OUT, weight)
        )


    ''' Mating methods. '''
    def crossover(self, genome):
        ''' Crossover two genomes. '''
        genes = []
        kid = self.clone()
        unfitter, fitter = sorted([self, genome], key=lambda x: x.fitness)

        for i, (unfit, fit) in enumerate(zip(unfitter.Genes, fitter.Genes)):
            # if genes are matching
            if fit.innovation == unfit.innovation:
                gene = random.choice((unfit, fit)).clone()
                if not(unfit.activation and fit.activation):
                    gene.randomize()
                genes.append(gene)
            # if genes are disjoint / excess
            else:
                for gene in fitter.Genes[i:]:
                    gene = gene.clone()
                    if not gene.activation:
                        gene.randomize()
                    genes.append(gene)
                break

        node = next((node for node in self.Nodes if node.ID != fit.IN))
        i = self.Nodes.index(node)
        nodes = [node for node in self.Nodes[:i]]

        kid.Genes = genes
        kid.Nodes = nodes + fitter.Nodes[i:]
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


