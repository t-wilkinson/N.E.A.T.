'''
Genome represents an organism
Each Genome has a list of Gene objects.
'''
from gene1 import Gene, Node
# from gene import Gene
import config
import random
from collections import defaultdict
import itertools as it

from copy import deepcopy


'''
Class
'''
class Genome:
	''' . '''

	def __init__(self, inputs, outputs):
		# create list of input and output Nodes
		self.inputs = [Node(i, 'input') for i in range(inputs)]
		self.outputs = [Node(i, 'output') for i in range(inputs, inputs+outputs)]
		Gene.node_counter = inputs + outputs

		# create every possible link from input to output nodes
		self.Genes = defaultdict(list)
		for in_node, out_node in it.product(self.inputs, self.outputs):
			self.Genes[in_node].append(Gene((in_node, out_node)))


	''' Pretty print. '''
	def print_genes(self):
		print('|============================================|' + \
		'\n|                   Genes                    |' + \
		'\n|--------------------------------------------|' + \
		'\n|  IN:OUT |   Weight   | Innovation | Active |')
		for in_node in self.Genes:
			print('\n'.join(f'|{in_node}:{gene}' for gene in self.Genes[in_node]))
		print('|============================================|')

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
		Reduce mal-effect of adding new node.
		'''
		in_node = random.choice(list(self.Genes.keys()))
		out_node = random.choice(self.Genes[in_node])
		out_node.active = False
		new_node = Gene.new_node((in_node, out_node.out))

		# To node -> new node has weight of 1
		self.add_gene(in_node, new_node, 1.0)
		# new node -> OUT has weight of original link
		self.add_gene(new_node, out_node.out, out_node.weight)

	def add_link(self):
		''' Add link to two unconnected nodes. '''
		# find all possible links
		nodes = (gene.out for gene in sum(self.Genes.values(), []))
		hidden_nodes = (node for node in nodes if node == 'hidden')
		all_nodes = it.chain(list(self.Genes.keys()), nodes)
		all_links = (link for link in it.product(all_nodes, hidden_nodes))

		current_links = []
		for in_node in self.Genes:
			for out_node in (gene.out for gene in self.Genes[in_node]):
				current_links.append((in_node, out_node))

		# select a random link and add link
		possible_links = list(set(all_links) - set(current_links))
		if possible_links:
			in_node, out_node = random.choice(possible_links)
			self.add_gene(in_node, out_node)

	def add_gene(self, in_node, out_node, weight=None):
		''' Add new conneciton to genome. '''
		gene = Gene(link=(in_node, out_node), weight=weight)
		self.Genes[in_node].append(gene)


	''' Mating methods. '''
	def crossover(self, genome):
		''' Crossover two genomes. '''
		unfitter, fitter = sorted([self, genome], key=lambda x: x.fitness)
		kid = fitter.clone()

		for (k1, v1), (k2, v2) in zip(unfitter.Genes.items(), kid.Genes.items()):
			for i, (unfit, fit) in enumerate(zip(v1, v2)):
				if unfit.innovation != fit.innovation:
					break
				if random.random() < 0.5:
					unfit = deepcopy(unfit)
					if not(unfit.active and fit.active):
						unfit.randomize()
					kid.Genes[k1] = kid.Genes.pop(k2)
					kid.Genes[k1][i] = unfit

		return kid

	def compatable(self, genome):
		''' Quantize compatability of two genomes. '''
		matching = []
		disjoint, excess = 0, 0
		for (v1, v2) in it.zip_longest(self.Genes.values(), genome.Genes.values(), fillvalue=[]):
			for (gene1, gene2) in it.zip_longest(v1, v2):
				if gene1 and gene2:
					if gene1 == gene2:
						matching.append((gene1.weight - gene2.weight))
					else:
						disjoint += 1
				else:
					excess += 1
		if not matching:
			return False

		weight_avg = sum(matching) / len(matching)
		normalize = max(len(sum(self.Genes.values(), [])), 
						len(sum(genome.Genes.values(), [])))

		compatability = config.C1 * excess / normalize + \
						config.C2 * disjoint / normalize + \
						config.C3 * weight_avg

		return compatability < config.compatability_distance_threshold



