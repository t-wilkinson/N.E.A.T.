import config
from random import uniform


class Gene:
	Genes = {}
	gene_counter = 0
	node_counter = 0

	def __init__(self, link: tuple, weight: float=None, layer: str='hidden'):
		self.link = link
		self.active = True
		self.layer = layer
		self.innovation = Gene.Genes.get(frozenset(link)) or self.new_link(link)
		self.weight = weight if weight else uniform(-2.0, 2.0)

	def new_link(self, link):
		''' Keep track of new links. '''
		Gene.gene_counter += 1
		Gene.Genes[frozenset(link)] = Gene.gene_counter
		return Gene.gene_counter

	def randomize(self):
		self.active = uniform(0, 1) > config.chance_inherit_disabled_gene

	def mutate(self):
		if uniform(0, 1) < config.chance_mutate_weight_adjust:
			self.weight += uniform(0, 1)
		else:
			self.weight = uniform(0, 1)

	def clone(self):
		return deepcopy(self)

	''' Dunders. '''
	def __hash__(self):
		return self.link[0]

	def __eq__(self, gene):
		return self.innovation == gene.innovation
		
	def __str__(self):
		active = 'ON' if self.active else 'OFF'
		return '|' + \
		f'{self.link[0]: >4}:{self.link[1]: <4}|' + \
		f'{self.weight: 9.4f}   |' + \
		f'{self.innovation: ^12}|' + \
		f'{active: ^8}|'

	''' Class method. '''
	@classmethod
	def new_node(cls, link):
		''' Keep track of new nodes. '''
		keys = list(cls.Genes.keys())
		for (i, gene1) in enumerate(keys):
			for gene2 in keys[i+1:]:
				if gene1 ^ gene2 >= set(link):
					if gene1 & gene2:
						return next(iter(gene1 & gene2))

		Gene.node_counter += 1
		return Gene.node_counter - 1

	@classmethod
	def reset(cls):
		cls.Genes.clear()




