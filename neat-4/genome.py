'''
Genome represents an organism
Each Genome has a list of Gene objects.
'''
from gene import Gene
import config
import random
from collections import defaultdict
import itertools as it

from copy import deepcopy

#hey
'''
Class
'''
class Genome:
	''' . '''

	def __init__(self, inputs, outputs):
		# create list of input and output Nodes
		self.topology = (
			tuple(range(inputs)),
			tuple(range(inputs, inputs+outputs))
		)
		Gene.node_counter = inputs + outputs

		# create every possible link from input to output nodes
		self.Genes = defaultdict(list)
		for link in it.product(*self.topology):
			gene = Gene(link)
			self.Genes[gene].append(gene)


	''' Pretty print. '''
	def print_genes(self):
		print('|============================================|' + \
		'\n|                   Genes                    |' + \
		'\n|--------------------------------------------|' + \
		'\n|  IN:OUT |   Weight   | Innovation | Active |\n' + \
		'\n'.join([f'{gene}' for gene in sum(self.Genes.values(), [])]) + \
		'\n|============================================|')

	''' Simple helper functions. '''
	def clone(self):
		return deepcopy(self)


	''' Mutations. '''
	def mutate(self):
		if random.uniform(0, 1) < config.chance_mutate_weight:
			for gene in sum(self.Genes.values(), []):
				gene.mutate()
		if random.uniform(0, 1) < config.chance_new_link:
			self.add_link()
		if random.uniform(0, 1) < config.chance_new_node:
			self.add_node()


	def add_node(self):
		'''
		Create new node to add to existing link.
		Set link weight from In node -> new node to 1.0
		and weight from new node -> Out node to original weight.
		Reduce mal-effect of adding new node.
		'''
		gene = random.choice(sum(self.Genes.values(), []))
		gene.active = False
		node = Gene.new_node(gene.link)

		# To node -> new node has weight of 1
		self.add_gene(gene.link[0], node, 1.0)
		# new node -> OUT has weight of original link
		self.add_gene(node, gene.link[1], gene.weight)

	def add_link(self):
		''' Add link to two unconnected nodes. '''
		genes = sum(self.Genes.values(), [])
		# find all possible links
		all_nodes = (gene.link[0] for gene in genes)
		hidden_nodes = (gene.link[1] for gene in genes if gene.layer == 'hidden')

		all_links = (link for link in it.product(all_nodes, hidden_nodes))
		current_links = (link for link in genes)

		possible_links = list(frozenset(all_links) - frozenset(current_links))

		# select a random link and add link
		if possible_links:
			in_node, out_node = random.choice(possible_links)
			self.add_gene(in_node, out_node)

	def add_gene(self, in_node, out_node, weight=None):
		''' Add new conneciton to genome. '''
		gene = Gene(link=(in_node, out_node), weight=weight)
		self.Genes[gene].append(gene)


	''' Mating methods. '''
	def crossover(self, genome):
		''' Crossover two genomes. '''
		unfitter, fitter = sorted([self, genome], key=lambda x: x.fitness)
		kid = fitter.clone()

		for (unfit_val, fit_val) in zip(unfitter.Genes.values(), fitter.Genes.values()):
			for i, (unfit, fit) in enumerate(zip(unfit_val, fit_val)):
				if unfit.innovation != fit.innovation:
					break
				if random.random() < 0.5:
					unfit = deepcopy(unfit)
					if not(unfit.active and fit.active):
						unfit.randomize()
					kid.Genes[fit][i] = unfit

		return kid

	def compatable(self, genome):
		''' Quantize compatability of two genomes. '''
		matching = []
		disjoint, excess = 0, 0
		for (gene1_val, gene2_val) in it.zip_longest(self.Genes.values(), genome.Genes.values(), fillvalue=[]):
			for (gene1, gene2) in it.zip_longest(gene1_val, gene2_val):
				if gene1 and gene2:
					if gene1 == gene2:
						matching.append((gene1.weight - gene2.weight))
					else:
						disjoint += 1
				else:
					excess += 1

		weight_avg = sum(matching) / len(matching)
		normalize = max(len(sum(self.Genes.values(), [])),
						len(sum(genome.Genes.values(), [])))

		compatability = config.C1 * excess / normalize + \
						config.C2 * disjoint / normalize + \
						config.C3 * weight_avg

		return compatability < config.compatability_distance_threshold



